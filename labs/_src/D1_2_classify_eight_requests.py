# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 1.2 · Eight requests classified
#
# Day 1 · Session 2 (Question types) · 25 min.
#
# Eight requests reached the analytics team this month. You label each one descriptive, predictive, causal or
# unanswerable, then name the analysis it needs: a description, an experiment, a causal analysis of existing data, a
# predictive model, or no analysis. Then the sponsor changes a constraint and you revise.
#
# **AI policy: AI-tutor.** You may ask a tutor to question your reasoning (`U.tutor`), not to label for you.
#
# **Reference state.** `data/requests.json`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Read the four labels and the eight requests (3')
# - [ ] 2 · Classify each request (8')
# - [ ] 3 · Name the analysis each one needs (6')
# - [ ] 4 · The sponsor changes a constraint: revise (5')
# - [ ] 5 · Compare with the key and explain one disagreement (3')
# - [ ] ✱ Stretch · Rewrite the unanswerable request so that data could answer it

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
# ## 1 · The labels and the requests (3')
#
# | Label | The request asks | It needs |
# |---|---|---|
# | descriptive | what happened, how much, where | a description |
# | predictive | what will happen to a unit, who is likely to | a predictive model |
# | causal | what a change did, or would do | an experiment when one can run; otherwise a causal analysis of existing data |
# | unanswerable | something the data cannot reach, or no decision at all | no analysis (yet): reframe, or collect other data |

# %%
reqs = U.js("requests")
for r in reqs["classify"]:
    print(f"{r['id']}  {r['text']}")

# %% [markdown]
# ## 2 · Classify each request (8')
#
# ✏️ **Exercise** · One label each. The words of a request mislead: "which" can be descriptive or predictive; "did ... improve"
# is causal even when nobody says "cause".

# %%
LABELS = ["descriptive", "predictive", "causal", "unanswerable"]


def classify() -> dict:
    # BEGIN SOLUTION
    return {"C1": "descriptive", "C2": "predictive", "C3": "causal", "C4": "causal",
            "C5": "predictive", "C6": "unanswerable", "C7": "descriptive", "C8": "causal"}
    # END SOLUTION


# %%
try:
    labels = classify()
except NotImplementedError:
    labels = {k: v[0] for k, v in U.reference("classify")["key"].items()}
U.check(set(labels) == {r["id"] for r in reqs["classify"]}, "every request has a label")
U.check(set(labels.values()) <= set(LABELS), "only the four labels are used")

# %% [markdown]
# ## 3 · The analysis each one needs (6')
#
# ✏️ **Exercise** · Choose from: `description`, `experiment`, `causal analysis`, `predictive model`, `no analysis`. A causal
# request gets an experiment only when you can still assign the change at random; a change already made everywhere
# (C3) or in one district (C8) leaves a causal analysis of existing data.

# %%
ANALYSES = ["description", "experiment", "causal analysis", "predictive model", "no analysis"]


def analysis_needed() -> dict:
    # BEGIN SOLUTION
    return {"C1": "description", "C2": "predictive model", "C3": "causal analysis", "C4": "experiment",
            "C5": "predictive model", "C6": "no analysis", "C7": "description", "C8": "causal analysis"}
    # END SOLUTION


# %%
try:
    needs = analysis_needed()
except NotImplementedError:
    needs = {k: v[1] for k, v in U.reference("classify")["key"].items()}
U.check(set(needs.values()) <= set(ANALYSES), "only the five kinds of analysis are used")
table = pd.DataFrame({"request": [r["text"] for r in reqs["classify"]], "label": labels.values(), "needs": needs.values()},
                     index=list(labels))
print(table.to_string())

# %% [markdown]
# ## 4 · The sponsor changes a constraint (5')
#
# Nadia Al-Rubaie has just written. Read it, then decide which recommendation changes and to what.
#
# ✏️ **Exercise** · Return the requests whose recommendation changes, with the new one, and one sentence on why.

# %%
change = reqs["constraint_change"]
print(f"{change['from']}: \"{change['text']}\"")


def revise() -> dict:
    # BEGIN SOLUTION
    return {"C4": {"needs": "no analysis",
                   "why": "No trial can run before the decision and no existing data hold text reminders: decide the meter-reading "
                          "question on cost and practicality now, and test reminders when the budget returns"}}
    # END SOLUTION


# %%
try:
    revised = revise()
except NotImplementedError:
    revised = {k: {"needs": v, "why": "(reference)"} for k, v in U.reference("classify")["after_change"].items()}
U.check(set(revised) == {"C4"}, "only C4 is affected by the change")
U.check(revised["C4"]["needs"] in ANALYSES, "the new recommendation is one of the five")
needs_after = needs | {k: v["needs"] for k, v in revised.items()}

# %% [markdown]
# ## 5 · Compare with the key (3')
#
# The key is one defensible reading. Where you differ, write one sentence that would convince the trainer, or change
# your answer. Ask the tutor to question one of your labels.

# %%
key = U.reference("classify")
diff = [(k, labels[k], key["key"][k][0]) for k in labels if labels[k] != key["key"][k][0]]
diff += [(k, needs_after[k], (key["after_change"].get(k) or key["key"][k][1])) for k in needs_after
         if needs_after[k] != (key["after_change"].get(k) or key["key"][k][1])]
print("agreements:", 16 - len(diff), "of 16")
for k, mine, theirs in diff:
    print(f"  {k}: yours {mine!r}, key {theirs!r}")
print(U.tutor(f"I labelled C8 '{labels['C8']}' and said it needs '{needs['C8']}'.", "is my label of C8 right?"))
U.check(len(diff) <= 2, "at most two disagreements with the key, each one argued")
U.save("classification.csv", table.assign(after_change=[needs_after[k] for k in table.index]).to_csv())

# %% [markdown]
# ## ✱ Stretch · Make C6 answerable
#
# "Why do customers distrust us?" has no decision and no data. Rewrite it as a question the contact log could answer
# and that would change something the company does.

# %%
def c6_rewritten() -> str:
    # BEGIN SOLUTION
    return ("Which contact reasons are followed by a repeat contact within seven days most often, so that we know which "
            "two to fix first?")
    # END SOLUTION


try:
    print(c6_rewritten())
except NotImplementedError:
    print("stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. C3 says "did the target improve service". Why is it causal, and why can it not be an experiment now?
#    <details><summary>Answer</summary>It asks what the target did. The target started in every team at once, so no
#    group was left without it at random: only a causal analysis of existing data remains.</details>
# 2. Why is C2 predictive and not descriptive, although it starts with "which"?
#    <details><summary>Answer</summary>It asks about next month, for each account: a forecast for units, not a summary of
#    the past.</details>
# 3. After the constraint changed, why is "no analysis" a professional answer for C4?
#    <details><summary>Answer</summary>No data can answer it in time and no trial can run: an analysis would only dress
#    up a guess. Say so, and say what would make it answerable.</details>
#
# **Carry forward.** `out/classification.csv`. Lab 1.3 starts from `data/roles.json`.
