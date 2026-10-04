# Granite experiment — Ziad Suleyman

Hugging Face model and revision:
Code repository and commit:
Hardware / OS:
Active time / unattended time:
AI assistance used:

## Hypothesis

**Main (H0, weak effect).** The edit removes the style direction from a single attention output
projection, one of about 48 components that write to the residual stream (24 attention and 24
expert blocks). The verbosity signal that earlier layers already wrote remains in the stream.
I therefore expect a small, unsystematic change on the 15 ordinary test questions: the mean
per-question change in word count against the original stays within ±10%, and the answers that
change move in both directions. The prompt-only control should shorten the same questions far
more (over 20%). On GSM8K and ARC, the net change should be at most 2 questions (4 percentage
points) per subset, and any correctness flips should not all go one way.

**Competing (H1).** The direction was measured under explicit length instructions, so it may
encode a *request* for length rather than the model's default style. If so, the edit will mainly
affect the 5 detail-request questions: their relative shortening will be at least twice that of
the ordinary questions, and at least 2 of them will lose required information that the original
included. With only 5 such questions, this is a weak test.

**What would count against them.** H0 fails if the mean change on ordinary questions is 10% or
more in either direction, or if at least three quarters of the changed answers (with at least 8
changed) move the same way. H1 fails if the detail-request questions shorten less than twice as
much as the ordinary ones, or lose no required information. Answers cut off at the token limit
are reported separately.

**Layer-level prediction.** If a layer's attention writes strongly along the measured direction
(`|attn_write_default| ≥ 0.1`), I predict a larger effect at that layer, in the direction of its
sign: positive should shorten answers, negative could lengthen them. If all layers have weak
writes, I predict smaller effects overall, but I will treat this only as a prior expectation
rather than evidence for H0 by itself.


## Intervention


**Edit.** Only `model.layers.23.self_attn.o_proj.weight` changed (zero-based layer 23), at strength 1.0, using the starter's norm-preserving directional edit and the calibrated direction (`style-directions.safetensors`, sha256 `c480b933…`). Expert, router and all other weights are unchanged; routing in later layers can still change.

**Why layer 23.** `notes/layer-profile.csv` measures each layer's attention write along its style direction, in units of the concise/extended gap. Layers 1–6 show large ratios, but their gap is tiny (relative contrast ≤ 0.11) and the direction is unstable (cos_prev down to −0.04), so I discount them. Layers 8–22 have `|attn_write_default| ≤ 0.051`. Layer 23 has the largest stable positive write (`attn_write_default` = 0.194, above my 0.1 threshold), a large gap (0.313), and a direction that agrees with layer 22 (cosine 0.924). Layer 7 also passes (0.125) but is less stable (0.54 / 0.44) and has 16 later blocks that could cancel it. Caveat: layer 23 is the last block, so nothing downstream can dilute or repair the edit, which raises the risk to GSM8K and ARC. Its `attn_write_gap` is near zero (0.010): it pushes default answers toward "extended" more than it separates the two instructed styles.

**Why strength 1.0.** I predicted a weak effect, so the fairest test is the strongest edit the method allows; a null result then cannot be blamed on under-dosing. Dev questions check for broken answers first.

**Held fixed.** Original checkpoint, matched F16 export, Ollama 0.35.1, template and generation settings (temperature 0, seed 42, 512 tokens, context 4096). A null edit reproduced the original's words and token counts, so differences are caused by the edit.

**Development observations.** On the 6 dev questions the edit changed every answer's text but not in one direction: 3 longer, 2 shorter, 1 the same length (ordinary questions: −4%, +9%, +8%, +52%;
detail questions: −15%, 0%). No answer hit the 512-token limit and none was broken or off-topic.
Content shifted rather than shrank: dev-02 gained the correct "we hear thunder after we see lightning", while dev-04 grew longer with more geometry errors. The prompt-only control shortened 5 of 6 answers. Six questions are a sanity check, not evidence for either hypothesis.

## Results

| Evaluation | Original | Edited | Difference |
| --- | --- | --- | --- |
| GSM8K, 50-question subset | 22/50 | 19/50 | −6.0 pp (1 gain, 4 regressions) |
| ARC-Challenge, 50-question subset | 11/50 | 11/50 | 0 pp (no flips) |
| Behavior: correct and complete | 2/6 reviewed | 3/9 reviewed | review incomplete: 20/60 answers marked (prompt-only 3/5) |
| Behavior: response length (20 questions) | 185.7 words | 196.1 words | +10.1% mean per-question change; 8 shorter, 1 same, 11 longer |

On the 15 ordinary questions the edit changed length by +5.2% (7 shorter, 7 longer of 14 changed);
the prompt-only control changed it by −27.2% (12 of 14 shorter). On the 5 detail requests the edit
lengthened answers by +24.9% (4 of 5 longer), while prompt-only shortened them by 14.0%. No answer
hit the 512-token limit. Examples: test-20 (detail) grew from 199 to 358 words, test-15 shrank from
234 to 90, and test-14 stayed at 44 words. Edited GSM8K outputs used slightly more tokens
(8,884 vs 8,609). Full outputs: `results/behavior.json`, `results/behavior.annotated.json`,
`results/capability/logs/`.

## Interpretation

H0 holds on its length criteria (ordinary questions +5.2%, changes split 7/7), and H1 is rejected:
detail answers lengthened by 25% instead of shortening twice as much. My layer-level prediction
failed: layer 23 had the largest positive default write, yet removing it lengthened answers on
average, so the sign of `attn_write_default` did not predict the behaviour. H0's capability
prediction also failed: GSM8K fell by 3 questions (4 regressions, 1 gain). That fits my caveat that
editing the last block leaves nothing downstream to repair damage, but 3 of 50 is within about one
standard error (0.07), so it is a signal to check, not established harm. Both models score 22% on
ARC, below the 25% chance level, which suggests an answer-extraction problem; I did not verify this
in the logs. The prompt-only control shortened answers far more than the edit, so in this setup a
prompt beats this single-matrix edit. The confound that matters most is that the direction was
measured at the last prompt token under explicit instructions, while the edit acts on every
generated token in the final block. The review is incomplete and n = 20, so a systematic
lengthening is not established. Next experiment: the same edit at layer 7, with a random-direction
edit of equal strength as a control, to separate a direction-specific effect from generic perturbation.