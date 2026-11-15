# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 2.4 · Three threats each
#
# Day 2 · Session 4 (Threats to validity) · 25 min.
#
# Two colleagues wrote plans. You list the three threats most likely to change each plan's answer, from a catalogue of
# ten, with one sentence each. You show one threat at work in the data: regression to the mean. Then you swap your own
# plan from Lab 2.3 with a neighbour and list theirs.
#
# **AI policy: AI-tutor.** A tutor may question your choice of threats; it does not choose them.
#
# **Reference state.** `data/threats.json`, `data/plans/plan_A.md`, `data/plans/plan_B.md`, `data/supply.csv`,
# `data/reads.csv`. Your neighbour's plan is on paper or in their `out/analysis_plan.md`; if they have none, swap the
# supplied plan of `data/card_2_3.json`.
#
# **Tasks**
# - [ ] 1 · Read the threat catalogue (3')
# - [ ] 2 · Plan A: its three main threats (7')
# - [ ] 3 · Regression to the mean in the data (5')
# - [ ] 4 · Plan B: its three main threats (5')
# - [ ] 5 · Swap with your neighbour and list theirs (5')
# - [ ] ✱ Stretch · Rewrite one plan so that its worst threat is answered

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
# ## 1 · The catalogue (3')

# %%
catalogue = {t["id"]: t for t in U.js("threats")}
for t in catalogue.values():
    print(f"{t['id']:20} {t['name']:32} {t['question']}")

# %% [markdown]
# ## 2 · Plan A (7')
#
# ✏️ **Exercise** · Read Plan A. Return its three main threats as `{threat id: one sentence}`, the most dangerous first. A
# main threat is one that could change the decision, not one that only adds noise.

# %%
print(U.text("plans/plan_A.md"))


def plan_a_threats() -> dict:
    # BEGIN SOLUTION
    return {
        "regression_to_mean": "Al-Wurud was picked for its highest month: it would fall back next months with no detection at all",
        "measurement_change": "The bulk meter over-read in months 10 to 12 and was recalibrated in month 13: the 'before' is inflated",
        "history": "Smart meters and both targets started in month 13; with no comparison district, all of it lands on detection",
    }
    # END SOLUTION


# %%
try:
    ta = plan_a_threats()
except NotImplementedError:
    ta = {k: "(reference)" for k in U.reference("plan_threats")["A"]}
U.check(all(k in catalogue for k in ta), "every threat is from the catalogue")
U.check(len(ta) == 3, "three threats")
hit_a = len(set(ta) & set(U.reference("plan_threats")["A"]))
print(f"Plan A: {hit_a} of 3 match the reviewers' key")
U.check(hit_a >= 2, "at least two of your three are the key's")

# %% [markdown]
# ## 3 · Regression to the mean, in the data (5')
#
# Plan A chose Al-Wurud because it had the highest non-revenue water in month 12. What happens next month to whichever
# district is highest, when nothing is done? Use months 1 to 12, before any change, and raw bills as Plan A does.
#
# ✏️ **Exercise** · For each month 1 to 11, take the district with the highest non-revenue water, and its change in the
# next month. Return the mean change for those top districts and for all districts.

# %%
def rtm() -> tuple[float, float]:
    # BEGIN SOLUTION
    n = U.nrw().pivot(index="month", columns="district", values="nrw_pct").loc[1:12]
    nxt = n.shift(-1) - n
    top = [nxt.loc[m, n.loc[m].idxmax()] for m in range(1, 12)]
    return round(float(pd.Series(top).mean()), 2), round(float(nxt.loc[1:11].stack().mean()), 2)
    # END SOLUTION


# %%
try:
    top_change, all_change = rtm()
except NotImplementedError:
    n = U.nrw().pivot(index="month", columns="district", values="nrw_pct").loc[1:12]
    nxt = n.shift(-1) - n
    top_change = round(float(pd.Series([nxt.loc[m, n.loc[m].idxmax()] for m in range(1, 12)]).mean()), 2)
    all_change = round(float(nxt.loc[1:11].stack().mean()), 2)
print(f"next-month change: the top district {top_change:+.2f} points, all districts {all_change:+.2f} points")
U.check(top_change < all_change - 2, "the district picked for being highest falls back by itself")

# %% [markdown]
# 🔍 Plan A's "before" is months 10 to 12. Look at Al-Wurud with bills rescaled to 30 days: the bulk-meter drift is
# visible, and so is how much of Plan A's "fall" it explains.

# %%
nr = U.nrw(normalise_cycle=True)
for label, months in (("months 1 to 9", range(1, 10)), ("months 10 to 12 (drift)", range(10, 13)),
                      ("months 13 to 15", range(13, 16)), ("months 15 to 24", range(15, 25))):
    print(f"Al-Wurud {label:24} {U.period_mean(nr, 'D2', months):5.1f}%   others "
          f"{nr[(nr.district != 'D2') & nr.month.isin(list(months))].nrw_pct.mean():5.1f}%")

# %% [markdown]
# ## 4 · Plan B (5')
#
# ✏️ **Exercise** · The same for Plan B.

# %%
print(U.text("plans/plan_B.md"))


def plan_b_threats() -> dict:
    # BEGIN SOLUTION
    return {
        "construct_proxy": "'Marked resolved' is set by agents whose bonus depends on it: the metric no longer measures resolution",
        "history": "The call script was shortened in the same month: any change mixes the target with the script",
        "missing_data": "Repeats are linked by mobile number, so a customer calling from another phone is missed",
    }
    # END SOLUTION


# %%
try:
    tb = plan_b_threats()
except NotImplementedError:
    tb = {k: "(reference)" for k in U.reference("plan_threats")["B"]}
hit_b = len(set(tb) & set(U.reference("plan_threats")["B"]))
print(f"Plan B: {hit_b} of 3 match the reviewers' key")
U.check(len(tb) == 3 and hit_b >= 2, "three threats, at least two of them the key's")

# %% [markdown]
# ## 5 · Your neighbour's plan (5')
#
# Swap plans from Lab 2.3. Write their three main threats, most dangerous first, and give them the list. They do the same
# for yours. Disagree about the order out loud: that conversation is the point.

# %%
neighbour = {
    # ✏️ replace with your neighbour's three threats
    "measurement_change": "Uses months 10 to 12 as 'before': the bulk-meter drift inflates them",
    "history": "Smart meters in Al-Nakheel change one comparison district in the same month",
    "seasonality": "Before and after periods hold different months",
}
U.check(len(neighbour) == 3 and all(k in catalogue for k in neighbour), "three threats from the catalogue for your neighbour")
lines = ["# Threats to validity", ""]
for name, d in (("Plan A", ta), ("Plan B", tb), ("Neighbour's plan", neighbour)):
    lines += [f"## {name}"] + [f"{i}. **{catalogue[k]['name']}.** {v}" for i, (k, v) in enumerate(d.items(), 1)] + [""]
lines += [f"Regression to the mean, months 1 to 12: the top district moved {top_change:+.2f} points the next month, "
          f"all districts {all_change:+.2f}."]
U.save("threats.md", "\n".join(lines) + "\n")

# %% [markdown]
# ## ✱ Stretch · Answer the worst threat
#
# Rewrite the method of Plan A so that regression to the mean no longer drives its answer.

# %%
def plan_a_fixed() -> str:
    # BEGIN SOLUTION
    return ("Compare Al-Wurud with the other five districts over the whole year before (months 1 to 9) and months 15 to 24 "
            "after, bills rescaled to 30 days; a district picked for one high month is judged on its long-run level.")
    # END SOLUTION


try:
    print(plan_a_fixed())
except NotImplementedError:
    print("stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why does a district chosen for its worst month look better next month without any action?
#    <details><summary>Answer</summary>Part of an extreme value is noise; the noise does not repeat, so the next value is
#    closer to the district's usual level.</details>
# 2. Which threat would a comparison district answer in Plan A, and which would it not?
#    <details><summary>Answer</summary>It answers history shared by all districts (the targets); it does not answer the
#    Al-Wurud bulk-meter drift, which only that district had.</details>
# 3. Why rank threats instead of listing them all?
#    <details><summary>Answer</summary>Every plan has ten possible threats; a reader acts on the two or three that could
#    change the decision.</details>
#
# **Carry forward.** `out/threats.md`. Day 3 starts from the supplied notebooks in `data/review/`.
