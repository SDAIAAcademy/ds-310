# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 1.4 · Check and cut one question
#
# Day 1 · Session 4 (Feasibility and scope) · 25 min.
#
# Nadia wants to know whether road works explain the bursts in Al-Rawdah and whether the renewal budget should go to the
# oldest mains there. The board meets in ten business days. You check each dataset the question needs: when it can be
# ready, how it is classified, whether it holds personal data the question does not need. Then you cut the scope until
# the question is answerable in time, and say what the cut costs.
#
# **AI policy: AI-tutor.** A tutor may question your scope; it does not choose it.
#
# **Reference state.** `data/card_1_4.json`, `data/inventory.json`, `data/repairs.csv`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Read the card and the data inventory (3')
# - [ ] 2 · Days until each dataset is ready (7')
# - [ ] 3 · Classification and personal data per dataset (5')
# - [ ] 4 · Cut the scope to fit ten business days (7')
# - [ ] 5 · Write the scoped card (3')
# - [ ] ✱ Stretch · The sponsor moves the deadline to five business days: cut again

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
# ## 1 · The card and the inventory (3')

# %%
card = U.js("card_1_4")
inv = U.js("inventory")
print(card["question"], "\nwants:", card["datasets_wanted"], "\ndeadline:", inv["deadline_business_days"],
      "business days, of which the analysis itself needs", inv["analysis_days_needed"])
pd.DataFrame(inv["datasets"]).drop(columns=["file"]).set_index("id")

# %% [markdown]
# ## 2 · Days until each dataset is ready (7')
#
# ✏️ **Exercise** · For a dataset Ghadeer holds, the wait is `access_business_days`. For one held by another government
# entity, the National Data Management Office's Data Sharing Policy gives the sharing entity up to 10 business days to
# assess a request and, once approved, 5 more to share the data (`sharing_assess_business_days`,
# `sharing_deliver_business_days`). Public open data needs no request. Return a dict: dataset id → business days.

# %%
wanted = [d for d in inv["datasets"] if d["id"] in card["datasets_wanted"]]


def days_ready(datasets: list[dict]) -> dict:
    # BEGIN SOLUTION
    out = {}
    for d in datasets:
        if d.get("external") and d["classification"] != "Public":
            out[d["id"]] = d["sharing_assess_business_days"] + d["sharing_deliver_business_days"]
        else:
            out[d["id"]] = d.get("access_business_days", 0)
    return out
    # END SOLUTION


# %%
try:
    ready = days_ready(wanted)
except NotImplementedError:
    ready = {d["id"]: U.ready_in_business_days(d) for d in wanted}
latest_start = inv["deadline_business_days"] - inv["analysis_days_needed"]
print(pd.Series(ready, name="business days").to_string(), f"\nmust be ready by day {latest_start}")
U.check(ready == {d["id"]: U.ready_in_business_days(d) for d in wanted}, "the waiting times are right")
U.check(ready["roadworks"] > inv["deadline_business_days"], "the road-works data cannot arrive before the deadline")

# %% [markdown]
# ## 3 · Classification and personal data (5')
#
# ✏️ **Exercise** · For each wanted dataset decide `keep` or `drop`, with a reason. Drop what cannot be ready by the day the
# analysis must start, and drop personal data the question does not need (the Personal Data Protection Law limits
# collection to the minimum the purpose needs). A Secret dataset also needs a security approval the deadline may not
# allow.

# %%
def decide() -> dict:
    # BEGIN SOLUTION
    return {
        "repair_orders": ("keep", "Ready in 1 day; it records every burst and repair; no personal data"),
        "weather": ("keep", "Public open data, ready now; tests the summer pattern"),
        "pipe_network": ("drop", "Secret, 8 business days: ready after the analysis must start; request it for phase two"),
        "roadworks": ("drop", "Held by the Roads Office: up to 15 business days under the sharing timeframe; request it now for phase two"),
        "billing_reads": ("drop", "Holds names, mobiles and national IDs that a burst question does not need"),
    }
    # END SOLUTION


# %%
try:
    decision = decide()
except NotImplementedError:
    decision = {d: ("keep" if ready[d] <= latest_start and not next(x for x in wanted if x["id"] == d)["personal_data"] else "drop", "(reference)")
                for d in ready}
keep = [d for d, (k, _) in decision.items() if k == "keep"]
by_id = {d["id"]: d for d in wanted}
U.check(all(ready[d] <= latest_start for d in keep), "every kept dataset is ready before the analysis must start")
U.check(not any(by_id[d]["personal_data"] for d in keep), "no kept dataset brings personal data the question does not need")
U.check(set(keep) == {"repair_orders", "weather"}, "two datasets survive: repairs and weather")

# %% [markdown]
# ## 4 · Cut the scope (7')
#
# What can repairs and temperature answer in time? Look at Al-Rawdah's bursts first.

# %%
rep = U.csv("repairs")
d1 = rep[rep.district_name == "Al-Rawdah"]
per_month = d1.groupby("month").size()
print("Al-Rawdah repairs per month, year 1:", round(per_month[per_month.index <= 12].mean(), 1),
      " year 2:", round(per_month[per_month.index > 12].mean(), 1))
print("summer months (6 to 9) against the rest:", round(per_month[per_month.index.map(lambda m: (m - 1) % 12 + 1 in (6, 7, 8, 9))].mean(), 1),
      "against", round(per_month[~per_month.index.map(lambda m: (m - 1) % 12 + 1 in (6, 7, 8, 9))].mean(), 1))

# %% [markdown]
# ✏️ **Exercise** · Write the scoped question, the kind of question it now is, what the cut leaves unanswered, and what you
# will request today for a second phase.

# %%
def scoped() -> dict:
    # BEGIN SOLUTION
    return {
        "question": "Have bursts in Al-Rawdah become more frequent over 24 months, and do they follow summer temperatures, "
                    "enough to justify a mains-renewal study next year?",
        "kind": "descriptive",
        "datasets": ["repair_orders", "weather"],
        "left_unanswered": "Whether road works or pipe age cause the bursts: that needs the road-works and pipe-network data",
        "request_now": ["Road-works permits from the Roads Office, through a data-sharing request",
                        "Pipe-network extract, through the security approval"],
    }
    # END SOLUTION


# %%
try:
    sc = scoped()
except NotImplementedError:
    sc = U.reference("scoped")
U.check(sc["question"].strip().endswith("?"), "the scoped question is a question")
U.check(set(sc["datasets"]) <= set(keep), "the scoped question uses only data that will be ready")
U.check(sc["kind"] in ("descriptive", "predictive", "causal"), "the question type is stated")
U.check(bool(sc["left_unanswered"]), "the card says what the cut leaves unanswered")

# %% [markdown]
# ## 5 · The scoped card (3')

# %%
lines = ["# Scoped card: bursts in Al-Rawdah", "", f"**Original question.** {card['question']}", "",
         f"**Scoped question ({sc['kind']}).** {sc['question']}", "", "**Data and when each is ready**"]
lines += [f"- {d}: {decision[d][0]}, {ready[d]} business days. {decision[d][1]}" for d in ready]
lines += ["", f"**Left unanswered.** {sc['left_unanswered']}", "", "**Requested today for phase two**"]
lines += [f"- {r}" for r in sc["request_now"]]
U.save("scoped_card_1_4.md", "\n".join(lines) + "\n")
print(U.tutor(sc["question"], "is my scoped question still worth answering for the board?"))

# %% [markdown]
# ## ✱ Stretch · Five business days
#
# The board meeting moves forward: five business days, still four of them for the analysis. Which data remain?

# %%
def five_days() -> list[str]:
    # BEGIN SOLUTION
    return [d for d in keep if ready[d] <= 5 - inv["analysis_days_needed"]]
    # END SOLUTION


try:
    print("still usable:", five_days())
except NotImplementedError:
    print("stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why can a perfectly framed question still be the wrong question for this board meeting?
#    <details><summary>Answer</summary>Its data cannot arrive in time: the road-works data need a sharing request that can
#    take 15 business days. A question that cannot be answered by the decision date does not inform the decision.</details>
# 2. Why drop the billing reads, although they are ready in two days?
#    <details><summary>Answer</summary>The question is about bursts. The billing extract brings names, mobiles and
#    national IDs the purpose does not need; minimisation says leave them.</details>
# 3. What does a good scope cut say besides the new question?
#    <details><summary>Answer</summary>What it leaves unanswered and what is requested now so that phase two can answer
#    it.</details>
#
# **Carry forward.** `out/scoped_card_1_4.md`. Day 2 starts from the briefing pack in `data/briefing/`.
