# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 2.3 · A plan for a framed question
#
# Day 2 · Session 3 (Analysis plans) · 25 min.
#
# You receive a framed question (the logger decision of Day 1), the data inventory and a two-week deadline. You write
# the analysis plan before looking at any result: the data, the method with its comparison, the change the data can
# detect, the threats, and the result that would change the decision. Then you score it against the rubric.
#
# **AI policy: AI-tutor.** A tutor may question your plan; it does not write it.
#
# **Reference state.** `data/card_2_3.json`, `data/inventory.json`, `data/supply.csv`, `data/reads.csv`. Nothing from
# another lab: the card is supplied, even if your Day 1 card differs.
#
# **Tasks**
# - [ ] 1 · Read the card, the inventory and the deadline (3')
# - [ ] 2 · Data and method (7')
# - [ ] 3 · What change the data can detect (5')
# - [ ] 4 · Threats and the result that changes the decision (7')
# - [ ] 5 · Score the plan against the rubric (3')
# - [ ] ✱ Stretch · Plan B, if the meter data arrive a week late

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

import json
import ghadeer as U

# %% [markdown]
# ## 1 · The card, the inventory, the deadline (3')

# %%
card = U.js("card_2_3")
inv = U.js("inventory")
print(json.dumps(card, indent=1, ensure_ascii=False))
for d in inv["datasets"]:
    print(f"  {d['id']:15} {d['classification']:10} ready in {U.ready_in_business_days(d):2} business days   {d['name']}")
print("deadline:", inv["deadline_business_days"], "business days; the analysis itself needs", inv["analysis_days_needed"])

# %% [markdown]
# ## 2 · Data and method (7')
#
# ✏️ **Exercise** · Name the datasets by their inventory id, say which fields and at what grain (district-month totals need
# no personal data), and describe the method with its comparison. Do not look at the post-detection numbers: a plan is
# fixed before the outcome is seen.

# %%
def data_and_method() -> dict:
    # BEGIN SOLUTION
    return {
        "question": card["decision"],
        "data": ["bulk_supply", "billing_reads"],
        "data_note": "Bulk-meter input by district and month; billed m3 and billing-period days as district-month totals from "
                     "the billing team, so no names, mobiles or national IDs leave the billing system",
        "method": "Difference in differences: mean non-revenue water in Al-Wurud against the mean of the other five districts, "
                  "months 1 to 9 before against months 15 to 24 after, bills rescaled to 30 days; months 10 to 14 left out "
                  "(bulk-meter drift and its correction, and the start of detection)",
    }
    # END SOLUTION


# %%
try:
    dm = data_and_method()
except NotImplementedError:
    dm = {"question": card["decision"], "data": ["bulk_supply", "billing_reads"], "data_note": "district-month totals",
          "method": "Difference in differences against the other five districts, months 1 to 9 against 15 to 24"}
U.check(all(d in {x["id"] for x in inv["datasets"]} for d in dm["data"]), "every dataset is in the inventory")
U.check("compar" in dm["method"].lower() or "difference in differences" in dm["method"].lower() or "other" in dm["method"].lower(),
        "the method has a comparison")

# %% [markdown]
# ## 3 · What change the data can detect (5')
#
# The decision rule needs a fall of 3 points. Can 9 months before and 10 after tell 3 points from noise? Use the noise of
# the comparison districts in months 1 to 12, which are before any change.
#
# ✏️ **Exercise** · Return the pooled within-district standard deviation of monthly non-revenue water in the five comparison
# districts, months 1 to 12, for raw bills and for bills rescaled to 30 days. `U.detectable_change(sd, 9, 10)` turns
# each into the smallest difference the comparison can detect.

# %%
def noise() -> dict:
    # BEGIN SOLUTION
    out = {}
    for label, norm in (("raw", False), ("rescaled", True)):
        n = U.nrw(normalise_cycle=norm)
        n = n[(n.district != "D2") & (n.month <= 12)]
        out[label] = round(float(n.groupby("district").nrw_pct.std().pow(2).mean() ** 0.5), 2)
    return out
    # END SOLUTION


# %%
try:
    sd = noise()
except NotImplementedError:
    sd = {"raw": 5.01, "rescaled": 0.99}  # the reference run
mde = {k: round(U.detectable_change(v, 9, 10), 2) for k, v in sd.items()}
print("sd:", sd, "  smallest detectable change (points):", mde)
U.check(mde["raw"] > 3 > mde["rescaled"], "only the rescaled bills can detect a 3-point fall")

# %% [markdown]
# ## 4 · Threats, and the result that changes the decision (7')
#
# ✏️ **Exercise** · At least three threats, each with what the plan does about it. Then the result that would change the
# decision, in numbers, and a timeline in business days.

# %%
def threats_and_result() -> dict:
    # BEGIN SOLUTION
    return {
        "detectable_change": f"About {mde['rescaled']} points with bills rescaled to 30 days ({mde['raw']} raw): rescale, or the "
                             "3-point rule cannot be tested",
        "threats": [
            "Measurement change: the Al-Wurud bulk meter over-read in months 10 to 12; those months are left out",
            "History: smart meters reached Al-Nakheel in month 13; run the comparison with and without Al-Nakheel",
            "Selection: Al-Wurud was chosen for a high month; use the full pre-period, not the months just before",
            "Seasonality: the periods cover different months; compare against districts measured in the same months",
        ],
        "would_change": "If the difference in differences is below 3 points, or its interval reaches 0, do not buy loggers; "
                        "if it is 3 points or more, buy for Al-Rawdah (39.3%) and consider Al-Hamra",
        "timeline": "Days 1 to 2 data (bulk 1 day, billing totals 2 days); days 3 to 6 analysis; day 7 review; day 8 note to Nadia",
    }
    # END SOLUTION


# %%
try:
    tr = threats_and_result()
except NotImplementedError:
    tr = {"detectable_change": f"{mde['rescaled']} points rescaled", "threats": ["measurement change", "history", "selection"],
          "would_change": "If the difference is below 3 points, do not buy", "timeline": "8 business days"}
plan = {**dm, **tr}
U.check(len(plan["threats"]) >= 3, "three or more threats")
U.check(any(ch.isdigit() for ch in plan["would_change"]), "the deciding result is a number")

# %% [markdown]
# ## 5 · Score against the rubric (3')
#
# `U.score_plan` checks by rule what a reviewer checks first: complete sections, data ready in time, a comparison, three
# threats, a numeric deciding result, two pages at most. A person still reads the plan; a high score is necessary, not
# sufficient.

# %%
score = U.score_plan(plan, inv["deadline_business_days"])
print(score)
U.check(score["total"] >= 10, f"the plan scores {score['total']} of {score['max']}")
md = [f"# Analysis plan: {plan['question']}", ""] + [f"**{k.replace('_', ' ').capitalize()}.** "
      + (", ".join(plan[k]) if isinstance(plan[k], list) else str(plan[k])) + "\n" for k in
      ("data", "data_note", "method", "detectable_change", "would_change", "timeline")]
md += ["**Threats**"] + [f"- {t}" for t in plan["threats"]]
U.save("analysis_plan.md", "\n".join(md) + "\n")
print(U.tutor(plan["would_change"], "is my deciding result fixed before the outcome, and is it the right threshold?"))

# %% [markdown]
# ## ✱ Stretch · Plan B
#
# The billing totals arrive a week late. What does the plan still deliver on day 8, and what does it say about it?

# %%
def plan_b() -> str:
    # BEGIN SOLUTION
    return ("Without billed totals there is no non-revenue water. Deliver on day 8 the leak counts and repair times of Al-Wurud "
            "as context, labelled as activity, not outcome, and move the decision note to when the totals arrive.")
    # END SOLUTION


try:
    print(plan_b())
except NotImplementedError:
    print("stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why compute the detectable change before the analysis?
#    <details><summary>Answer</summary>If the data cannot tell 3 points from noise, the rule cannot be tested as planned:
#    better to know (and rescale the bills) before anyone sees a result.</details>
# 2. Why leave months 10 to 14 out?
#    <details><summary>Answer</summary>A measurement change (the bulk meter over-read, then its correction) and the start
#    of detection overlap there; including them mixes three effects.</details>
# 3. Why is the deciding result written before the outcome is seen?
#    <details><summary>Answer</summary>A threshold chosen after seeing the data bends to it: the garden of forking paths.</details>
#
# **Carry forward.** `out/analysis_plan.md`. Lab 2.4 starts from two supplied peer plans in `data/plans/`.
