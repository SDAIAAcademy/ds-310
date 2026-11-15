# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 3.1 · Score a short notebook
#
# Day 3 · Session 1 (A review checklist) · 25 min.
#
# Sabah Al-Huwaidi wrote a three-cell analysis: "Where is customer service worst?". You rerun it, then score it with the
# review checklist in five areas (question fit, data handling, method, inference, communication), 0 to 2 each, with one
# sentence per score. Then you compare with the reference score: two reviewers should land within a point per area.
#
# **AI policy: AI-tutor.** A tutor may question a score; it does not score.
#
# **Reference state.** `data/review/short_complaints.py`, `data/contacts.csv`, `data/accounts.csv`. Nothing from Day 2.
#
# **Tasks**
# - [ ] 1 · Rerun the short notebook (5')
# - [ ] 2 · Score question fit and data handling (6')
# - [ ] 3 · Score method and inference (6')
# - [ ] 4 · Score communication and the total (4')
# - [ ] 5 · Compare with the reference score (4')
# - [ ] ✱ Stretch · Name the one change that would raise the score most

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-310.git"
    if not Path("/content/ds-310").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-310"], check=True)
    os.chdir("/content/ds-310/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("ghadeer.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import pandas as pd
import ghadeer as U

# %% [markdown]
# ## 1 · Rerun first (5')
#
# A review starts by running the analysis yourself: does it run, and does it print what the author says it prints?

# %%
src = U.text("review/short_complaints.py")
print(src)
res = U.run_cells(src)
for cid, r in res.items():
    if cid != "_env":
        print(f"--- cell {cid}: {r['status']}\n{r['out']}")
U.check(all(r["status"] == "ok" for k, r in res.items() if k != "_env"), "the notebook reruns")

# %% [markdown]
# ## The checklist
#
# | Area | 2 | 1 | 0 |
# |---|---|---|---|
# | Question fit | Answers the decision asked | Answers a nearby question | Answers another question |
# | Data handling | Right rows, right denominators, checked | One unchecked step | A step that changes the answer |
# | Method | Fits the question type, with a comparison | Fits, but weak | Does not fit the question |
# | Inference | Claims match the evidence, uncertainty stated | Some overreach | Claims what the data cannot show |
# | Communication | The reader can act on it correctly | Clear but misleading in part | Misleads |

# %% [markdown]
# ## 2 · Question fit and data handling (6')
#
# ✏️ **Exercise** · Score each area 0, 1 or 2 with one sentence. Look at what "worst service" would need, and at the
# denominator: does every district have the same number of accounts, and the same reasons to call?

# %%
acc = U.csv("accounts")
print(acc.groupby("district").agg(accounts=("account_id", "size"), access_issue_pct=("access_issue", "mean")).round(2))


def score_part_one() -> dict:
    # BEGIN SOLUTION
    return {"question_fit": (1, "It answers 'where are the most contacts', a nearby question, not 'where is service worst'"),
            "data_handling": (1, "Raw counts with no rate per account; Al-Hamra's meter-access problems drive billing calls")}
    # END SOLUTION


# %%
try:
    s1 = score_part_one()
except NotImplementedError:
    ref = U.reference("short_scores")
    s1 = {k: (ref[k], ref["notes"][k]) for k in ("question_fit", "data_handling")}
U.check(all(v[0] in (0, 1, 2) and U.words(v[1]) >= 6 for v in s1.values()), "two scores, each with a sentence")

# %% [markdown]
# ## 3 · Method and inference (6')
#
# ✏️ **Exercise** · Same for method and inference. Run one check of your own first: the share of contacts followed by
# another within seven days, by district, is closer to "service".

# %%
con = U.csv("contacts").sort_values(["account_id", "day"])
con["repeat7"] = (con.groupby("account_id").day.shift(-1) - con.day) <= 7
year2 = con[con.month >= 13]
print((100 * year2.groupby("district").repeat7.mean()).round(1).sort_values(ascending=False))


def score_part_two() -> dict:
    # BEGIN SOLUTION
    return {"method": (0, "A count of contacts does not measure service; no rate and no measure such as repeat contacts"),
            "inference": (0, "It reads the volume of contacts as the quality of service and recommends staff on that")}
    # END SOLUTION


# %%
try:
    s2 = score_part_two()
except NotImplementedError:
    ref = U.reference("short_scores")
    s2 = {k: (ref[k], ref["notes"][k]) for k in ("method", "inference")}
U.check(all(v[0] in (0, 1, 2) for v in s2.values()), "two more scores")

# %% [markdown]
# ## 4 · Communication and the total (4')
#
# ✏️ **Exercise** · Compare each sentence the notebook prints with the table it printed just before.

# %%
def score_part_three() -> dict:
    # BEGIN SOLUTION
    return {"communication": (0, "The text says Al-Hamra has the most contacts; the rerun shows Al-Salam 707, Al-Hamra 705")}
    # END SOLUTION


# %%
try:
    s3 = score_part_three()
except NotImplementedError:
    ref = U.reference("short_scores")
    s3 = {"communication": (ref["communication"], ref["notes"]["communication"])}
scores = {**s1, **s2, **s3}
total = sum(v[0] for v in scores.values())
print(pd.DataFrame(scores, index=["score", "why"]).T.to_string(), f"\ntotal: {total} of 10")
U.check(set(scores) == set(U.AREAS), "all five areas scored")

# %% [markdown]
# ## 5 · Compare with the reference (4')
#
# A checklist is useful when two reviewers agree. Where you differ by two points, one of you missed something: find out
# which.

# %%
ref = U.reference("short_scores")
diffs = {a: scores[a][0] - ref[a] for a in U.AREAS}
print("difference from the reference by area:", diffs)
U.check(all(abs(d) <= 1 for d in diffs.values()), "within one point of the reference in every area")
md = ["# Review: 'Where is customer service worst?' (short notebook)", "", "| Area | Score | Why |", "|---|---|---|"]
md += [f"| {a} | {scores[a][0]} | {scores[a][1]} |" for a in U.AREAS] + ["", f"Total: {total} of 10"]
U.save("review_short.md", "\n".join(md) + "\n")

# %% [markdown]
# ## ✱ Stretch · The change that raises the score most
#
# One sentence: what single change to the notebook would raise its score the most, and by how many points?

# %%
def best_change() -> str:
    # BEGIN SOLUTION
    return ("Measure service by the share of contacts followed by another within seven days, per district, and write the "
            "sentence from that output: it lifts question fit, method, inference and communication, about five points.")
    # END SOLUTION


try:
    print(best_change())
except NotImplementedError:
    print("stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why rerun before reading the prose?
#    <details><summary>Answer</summary>Prose tells you what the author believes; a rerun tells you what the code does. Many
#    flaws only show in the output.</details>
# 2. Why does a count of contacts score 0 on method here, and what did the rerun catch that reading would not?
#    <details><summary>Answer</summary>The question is about service; volume depends on district size and on reasons to call
#    (estimated bills), not on how well calls are handled. The rerun shows Al-Salam above Al-Hamra: the sentence was not
#    written from the output.</details>
# 3. What makes two reviewers agree?
#    <details><summary>Answer</summary>Anchored levels (what a 2, a 1 and a 0 look like) and a sentence of evidence per
#    score.</details>
#
# **Carry forward.** `out/review_short.md`. Lab 3.2 starts from `U.seeded_analysis` and your participant number.
