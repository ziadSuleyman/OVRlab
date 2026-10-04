# Granite experiment — Your name

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

Which layer/tensors and strength did you choose? What stayed fixed? What did you observe on development questions before freezing the edit?

## Results

| Evaluation | Original | Edited | Difference |
| --- | --- | --- | --- |
| GSM8K, 50-question subset | correct / 50 | correct / 50 | percentage points |
| ARC-Challenge, 50-question subset | correct / 50 | correct / 50 | percentage points |
| Behavior: correctness and completeness | reviewed count / 20 | reviewed count / 20 | |
| Behavior: response length | | | |

How did the prompt-only control compare? What happened on questions requesting detail? Include representative outputs and at least one failure, regression, or unchanged case. Link full outputs.

## Interpretation

What does the evidence support? What remains uncertain? Which confound matters most? What single experiment would you run next?
