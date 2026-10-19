"""Print the Section 7.2 table from results.csv (run after compare.py and after filling 'correct')."""
import csv
print("| Task | System | Correct (y/n) | Steps | Seconds | In tokens | Out tokens |")
print("|---|---|---|---|---|---|---|")
for r in csv.DictReader(open("results.csv", encoding="utf-8")):
    print(f"| {r['task_id']} | {r['system']} | {r['correct']} | {r['steps']} | {r['seconds']} | {r['in_tokens']} | {r['out_tokens']} |")
