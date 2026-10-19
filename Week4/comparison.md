# COS30018 Week 4 - Comparison: single agent vs manager + sub-agents

> **Status (19 Oct 2026): not run yet.** Every model call fails with a 401 authentication error (Gemini `AQ.` key, then the Hugging Face token), so there are no measured results. Fill every `TBD` from `results.csv` once `python compare.py` runs. `python make_table.py` prints the table ready to paste.

## 7.2 Results table

| Task | System | Correct (y/n) | Steps | Seconds | In tokens | Out tokens |
|---|---|---|---|---|---|---|
| T1 | single | TBD | TBD | TBD | TBD | TBD |
| T1 | multi  | TBD | TBD | TBD | TBD | TBD |
| T2 | single | TBD | TBD | TBD | TBD | TBD |
| T2 | multi  | TBD | TBD | TBD | TBD | TBD |
| T3 | single | TBD | TBD | TBD | TBD | TBD |
| T3 | multi  | TBD | TBD | TBD | TBD | TBD |

Answer key: T1 = P-200 Riverbend Kayak, 688. T2 = P-100 29, P-300 26, no data for P-200. T3 = P-300 +15.1%, P-100 +10.7%, P-200 +6.8%.

## 7.3 Analysis (about 150 words)

Write one paragraph that answers all five questions using numbers from the table. Use this skeleton:

- Token ratio: multi used TBD times the tokens of single (total in + out across all four agents). Compare with 1.5x / 3x / 10x.
- T1 (simple lookup): delegation bought TBD. State plainly if the answer is "nothing".
- T2 (missing data): the more honest system was TBD, because TBD (did it say P-200 has no data, or invent a number?).
- T3 (compound): single got growth numbers TBD / wrote the file TBD. Multi got growth numbers TBD / wrote the file TBD.
- Decision: I would ship TBD. I would change my mind if TBD (for example single failing on long tasks, or cost not mattering).

## 7.4 Required experiment: change the worker model

Changed `WORKER_MODEL_ID` from `gemini-3.5-flash-lite` to `gemini-3.7-flash` and re-ran T2 and T3 only.

Write 3-4 sentences: was it more reliable or only more expensive (cite the token and seconds change)? Did the arithmetic improve? Should it have, given that `analyst_agent` executes real Python, so the sums come from the interpreter and not from the model's prediction? TBD.
