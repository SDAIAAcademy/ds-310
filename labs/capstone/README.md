# Capstone: the permits backlog of Hima Municipality

Copy this file into your own public repository as `README.md` and fill in every section. Read `BRIEF.md` first. All data
here is synthetic.

## What is in this folder

| File | What it holds |
|---|---|
| `BRIEF.md` | The request of Fahda Al-Bishr, director of permits, and what you hand in |
| `data/permits.csv` | 3,600 applications of one year: week, kind, channel (counter or online), whether complete on submission, returns for missing documents, submitted and decided day, status |
| `data/inventory.json` | The data that exist, who holds them, their classification and how long they take to obtain |
| `data/review/backlog_analysis.py` | An analysis drafted with an assistant by a colleague: the practice version to review |
| `data/practice_constraint_change.md` | A practice change of constraint (the defence uses another, unseen) |

## What you do

1. Frame the decision: who decides, between which options (doing nothing among them), the estimand, the metric with
   one guardrail, and the decision rule.
2. Check feasibility against `inventory.json`: what can you have, by when, and under which classification?
3. Write the analysis plan, at most two pages: data, method, threats to validity, the result that would change the
   decision, and what you leave out.
4. Rerun and review your variant of the backlog analysis (the trainer gives it to you on the capstone day): notes with
   problem, consequence and fix, ranked by consequence.
5. Say which kind of analysis the request needs: description, an experiment, a causal analysis, a predictive model or no
   analysis yet.
6. Rehearse the eight-minute talk, and one answer to the practice constraint change.

## What you submit

A link to a public GitHub repository holding:

- `framing_card.md`
- `analysis_plan.md` (two pages at most)
- `review_notes.md`
- this README, filled in.

## Your README

### The decision and the recommendation

*One paragraph: the decision, the kind of analysis you recommend, and why.*

### Assistant use

*Which parts an assistant drafted or checked, which model, and how you verified each part. Write "none" if none.*

### What you could not settle

*What would need data you do not have, or more time.*

## Rules

- Individual work. Assistants are allowed (AI-full); label what they produced and verify it. The supervised framing
  check and the defence are unaided.
- Synthetic data only; no personal data, no real municipal data.
- Passing the course needs 70% overall and at least 60% on the live defence. The rubric is on the capstone slides and
  the course page.
