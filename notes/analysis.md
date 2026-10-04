# Analysis tables (generated)

Review: single reviewer, shuffled, condition hidden — partially blind.

## Behavior, test questions

| condition | n | mean words | median words | mean tokens | cut off | correct & complete |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| original | 20 | 185.7 | 185.5 | 256.9 | 0 | 2/6 |
| edited | 20 | 196.1 | 197.0 | 277.1 | 0 | 3/9 |
| prompt_only | 20 | 133.1 | 145.0 | 184.2 | 0 | 3/5 |

### Ordinary questions

| condition | n | mean words | correct & complete |
| --- | ---: | ---: | ---: |
| original | 15 | 172.6 | 2/5 |
| edited | 15 | 172.8 | 1/6 |
| prompt_only | 15 | 117.1 | 2/3 |

### Detail requested

| condition | n | mean words | correct & complete |
| --- | ---: | ---: | ---: |
| original | 5 | 224.8 | 0/1 |
| edited | 5 | 265.8 | 2/3 |
| prompt_only | 5 | 180.8 | 1/2 |

## Paired change against the original, per question

Mean change = mean of per-question relative changes in words. Changed = text differs. Lost / gained = correct & complete in one and not the other.

| condition | questions | changed | shorter | same length | longer | mean change | lost c&c | gained c&c |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| edited | all (20) | 19 | 8 | 1 | 11 | +10.1% | 0 | 0 |
| edited | ordinary (15) | 14 | 7 | 1 | 7 | +5.2% | 0 | 0 |
| edited | detail (5) | 5 | 1 | 0 | 4 | +24.9% | 0 | 0 |
| prompt_only | all (20) | 19 | 15 | 1 | 4 | -23.9% | 0 | 0 |
| prompt_only | ordinary (15) | 14 | 12 | 1 | 2 | -27.2% | 0 | 0 |
| prompt_only | detail (5) | 5 | 3 | 0 | 2 | -14.0% | 0 | 0 |

## Per question (original / edited / prompt-only)

| id | detail | words | correct & complete |
| --- | --- | --- | --- |
| test-01 |  | 127 / 181 / 154 | ✗ ✗ ✗ |
| test-02 |  | 216 / 204 / 154 | · ✓ · |
| test-03 |  | 282 / 217 / 141 | ✗ ✗ · |
| test-04 |  | 56 / 61 / 49 | · · · |
| test-05 |  | 78 / 67 / 38 | · ✗ · |
| test-06 |  | 303 / 312 / 241 | ✓ · · |
| test-07 |  | 151 / 193 / 140 | · · · |
| test-08 |  | 171 / 241 / 82 | · · · |
| test-09 |  | 182 / 137 / 64 | · ✗ · |
| test-10 |  | 236 / 217 / 88 | · · · |
| test-11 |  | 150 / 187 / 169 | ✓ · · |
| test-12 |  | 147 / 281 / 128 | · · ✓ |
| test-13 |  | 212 / 160 / 184 | · ✗ · |
| test-14 |  | 44 / 44 / 44 | · · ✓ |
| test-15 |  | 234 / 90 / 81 | ✗ · · |
| test-16 | yes | 134 / 201 / 149 | · ✓ · |
| test-17 | yes | 294 / 328 / 175 | · ✗ ✓ |
| test-18 | yes | 189 / 193 / 169 | · ✓ · |
| test-19 | yes | 308 / 249 / 205 | ✗ · ✗ |
| test-20 | yes | 199 / 358 / 206 | · · · |

## Capability subsets (paired, same questions)

| subset | original | edited | change (pp) | gains | regressions |
| --- | ---: | ---: | ---: | --- | --- |
| gsm8k | 22/50 | 19/50 | -6.0 | 1 (IDs gsm8k_7105004c) | 4 (IDs gsm8k_1821fbe3, gsm8k_3379ef4b, gsm8k_51c7db74, gsm8k_a962d6e4) |
| arc_challenge | 11/50 | 11/50 | +0.0 | 0 | 0 |

Small screening subsets: one question is 2 percentage points. Not leaderboard scores.
