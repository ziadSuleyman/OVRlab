# Frozen edit — variant a

Frozen 2026-10-04 22:44:09 +0300, before `data/test.json` was opened.

- Tensor: `model.layers.23.self_attn.o_proj.weight` (the only one changed)
- Layer 23, strength 1.0
- Edit manifest sha256: `f131747931fe1315c7d5096c1d9f605c93a217404061bceb2560a66bb8ea1576`
- GGUF sha256: `8bbe34ff4cb808d3dd9008539b3dd2ea1489cd689f8e7cd77619a9b0b3ace020`
- Converter: llama.cpp `4260903678a7525f43419dc234a942b551a8951e`

## Why this variant

A is the strongest edit the method allows, so it tests the weak-effect hypothesis as planned. Every dev answer stayed fluent and none was cut off, although dev-04 became 52% longer and less accurate. I did not make a variant B: my rule allows one only after no effect (A changed every answer) or broken answers (none were broken), and strength is already at its maximum.

## Development answers (words)

| id | original | edited | prompt-only | detail requested |
| --- | ---: | ---: | ---: | --- |
| dev-01 | 70 | 67 | 57 |  |
| dev-02 | 172 | 187 | 165 |  |
| dev-03 | 72 | 78 | 70 |  |
| dev-04 | 162 | 247 | 219 |  |
| dev-05 | 265 | 225 | 195 | yes |
| dev-06 | 156 | 156 | 147 | yes |
