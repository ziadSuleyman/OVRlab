"""Per-layer profile of the concise/extended contrast, to choose an edit layer with evidence.

Same prompts, chat template and measurement point as calibrate.py: the last prompt token at the
input residual of each decoder block. Forward passes only, no gradients, nothing is edited.

The edit removes the direction only from what ONE layer's attention writes (its o_proj output);
it does not touch the signal earlier layers already put in the residual stream. So two columns
measure that write directly, in units of the concise/extended gap at that layer's input:

  attn_write_gap      how much this layer's attention widens the gap between the two styles.
                      0.10 = it adds 10% of the existing gap toward "extended".
  attn_write_default  how far this layer's attention pushes the unprompted model (dev questions)
                      toward "extended". Strength 1 removes about this much before the row-norm
                      restoration. Near 0: nothing to remove. Negative: it pushes toward
                      "concise", so removing it could make answers longer.

The other columns describe the residual stream itself (block 0 is excluded, as in calibrate.py):

  relative_contrast   |mean_extended - mean_concise| / typical state norm at that layer
  separation_d        gap between the two styles along the direction, in pooled standard
                      deviations. In-sample: the direction comes from these same prompts.
  cos_prev, cos_next  cosine with the neighbouring layers' directions (stability)
  default_position    where the unprompted model sits on the dev questions along the direction:
                      0 = like "concise", 1 = like "extended". Other questions, so only a hint.
  matches_saved       cosine with artifacts/style-directions.safetensors; should be ~1.0000

All of this is measured at the last prompt token. The edit acts on every generated token too,
and later layers can amplify or cancel it, so these are guides, not predictions.
"""

import argparse
import csv
import json

import torch
from common import CONFIG, ROOT, baseline
from safetensors.torch import load_file
from transformers import AutoModelForCausalLM, AutoTokenizer


def capture_attention_writes(model):
    """Keep each layer's attention output (o_proj) at the last token of the latest forward pass."""
    store = {}

    def keep(index):
        def hook(module, inputs, output):
            store[index] = output[0, -1].float()

        return hook

    for index, layer in enumerate(model.model.layers):
        layer.self_attn.o_proj.register_forward_hook(keep(index))
    return store


def last_token_states(model, tokenizer, system, question, store):
    tokens = tokenizer.apply_chat_template(
        [{"role": "system", "content": system}, {"role": "user", "content": question}],
        add_generation_prompt=True,
        return_tensors="pt",
    )
    output = model.model(tokens, output_hidden_states=True, use_cache=False)
    # hidden_states[i] is the input to block i; omit the final normalized state.
    states = torch.stack([s[0, -1].float() for s in output.hidden_states[:-1]])
    writes = torch.stack([store[i] for i in range(len(states))])
    return states, writes


def profile_rows(concise, verbose, default, saved, writes=None, residual_multiplier=1.0):
    """States are [questions, layers, hidden]; writes holds o_proj outputs of the same shapes."""
    mean_c, mean_v = concise.mean(0), verbose.mean(0)
    diff = mean_v - mean_c
    direction = torch.nn.functional.normalize(diff, dim=1)
    typical = torch.cat([concise, verbose]).norm(dim=2).mean(0)
    proj_c = (concise * direction).sum(2)
    proj_v = (verbose * direction).sum(2)
    proj_d = (default * direction).sum(2)
    if writes is not None:
        # What each layer's attention adds to the residual along that layer's direction.
        add = {k: residual_multiplier * (w * direction).sum(2) for k, w in writes.items()}
    layers = direction.shape[0]

    def cos(a, b):
        return round(torch.dot(direction[a], direction[b]).item(), 3)

    rows = []
    for layer in range(1, layers):
        start = proj_c[:, layer].mean()
        gap = proj_v[:, layer].mean() - start
        pooled = ((proj_c[:, layer].var() + proj_v[:, layer].var()) / 2).sqrt()
        row = {"layer": layer}
        if writes is not None:
            widen = add["verbose"][:, layer].mean() - add["concise"][:, layer].mean()
            row["attn_write_gap"] = round((widen / gap).item(), 3)
            row["attn_write_default"] = round((add["default"][:, layer].mean() / gap).item(), 3)
        row.update(
            {
                "relative_contrast": round((diff[layer].norm() / typical[layer]).item(), 4),
                "separation_d": round((gap / pooled).item(), 2),
                "cos_prev": cos(layer, layer - 1) if layer > 1 else "",
                "cos_next": cos(layer, layer + 1) if layer + 1 < layers else "",
                "default_position": round(((proj_d[:, layer].mean() - start) / gap).item(), 2),
                "matches_saved": round(torch.dot(direction[layer], saved[layer].float()).item(), 4),
            }
        )
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description="Per-layer profile of the style contrast")
    parser.add_argument("--output", default="notes/layer-profile.csv")
    args = parser.parse_args()
    torch.manual_seed(CONFIG["seed"])
    source = baseline()
    tokenizer = AutoTokenizer.from_pretrained(source, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        source, dtype=torch.float32, local_files_only=True, attn_implementation="eager"
    ).eval()
    store = capture_attention_writes(model)
    calibration = (ROOT / "data/calibration.txt").read_text().strip().splitlines()
    dev = [item["prompt"] for item in json.loads((ROOT / "data/dev.json").read_text())]

    def collect(system, questions):
        pairs = [last_token_states(model, tokenizer, system, q, store) for q in questions]
        return torch.stack([p[0] for p in pairs]), torch.stack([p[1] for p in pairs])

    with torch.inference_mode():
        concise, w_concise = collect(CONFIG["calibration_concise"], calibration)
        verbose, w_verbose = collect(CONFIG["calibration_verbose"], calibration)
        default, w_default = collect(CONFIG["system"], dev)
    saved = load_file(ROOT / "artifacts/style-directions.safetensors")["verbosity"]
    writes = {"concise": w_concise, "verbose": w_verbose, "default": w_default}
    multiplier = getattr(model.config, "residual_multiplier", 1.0)
    rows = profile_rows(concise, verbose, default, saved, writes, multiplier)
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"residual_multiplier = {multiplier}")
    print(" ".join(f"{k:>18}" for k in rows[0]))
    for row in rows:
        print(" ".join(f"{str(v):>18}" for v in row.values()))
    print(f"\nSaved {args.output}")


if __name__ == "__main__":
    main()
