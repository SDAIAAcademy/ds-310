# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 2.2 · Stress-test the metric tree
#
# Day 2 · Session 2 (Metrics and proxies) · 25 min.
#
# Ghadeer manages water loss and customer service through a metric tree. Two of its leaves became targets in month 13:
# repair time and first-contact resolution. You measure what happened to each target and to the outcome it stands for,
# label how each proxy failed, and add two guardrail metrics, each with the behaviour it exposes.
#
# **AI policy: AI-tutor.** A tutor may question your labels and guardrails; it does not choose them.
#
# **Reference state.** `data/metric_tree.json`, `data/repairs.csv`, `data/contacts.csv`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Read the tree and the date the targets started (3')
# - [ ] 2 · Repair time before and after the target (6')
# - [ ] 3 · First-contact resolution and repeat contacts (6')
# - [ ] 4 · Label each gamed metric with its mechanism (4')
# - [ ] 5 · Two guardrails and the behaviour each prevents (6')
# - [ ] ✱ Stretch · A guardrail for estimated reads inside non-revenue water

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
# ## 1 · The tree (3')

# %%
tree = U.js("metric_tree")
print("goal:", tree["goal"])
for n in tree["nodes"]:
    print(f"  {n['id']:16} {n['kind']:9} {n['name']}" + (f"   [target: {n['target']}]" if n.get("target") else ""))

# %% [markdown]
# ## 2 · Repair time (6')
#
# ✏️ **Exercise** · For months 1 to 12 and months 13 to 24 return: the median days from job creation to job closed (the
# target), the share of jobs reopened in percent, the mean days from the customer's report to job creation, and the mean
# days from report to the final fix (what the customer lives with).

# %%
rep = U.csv("repairs")


def repair_metrics(df: pd.DataFrame) -> pd.DataFrame:
    # BEGIN SOLUTION
    d = df.assign(period=(df.month >= U.TARGET_MONTH).map({False: "before", True: "after"}),
                  close=df.closed_day - df.job_created_day, lag=df.job_created_day - df.reported_day,
                  fix=df.final_fix_day - df.reported_day)
    out = d.groupby("period").agg(median_close_days=("close", "median"), reopened_pct=("reopened", "mean"),
                                  report_to_job_days=("lag", "mean"), report_to_fix_days=("fix", "mean"))
    out["reopened_pct"] *= 100
    return out.loc[["before", "after"]].round(2)
    # END SOLUTION


# %%
try:
    rm = repair_metrics(rep)
except NotImplementedError:
    R = U.reference("numbers")["repair"]
    rm = pd.DataFrame({"median_close_days": [R["median_close_before"], R["median_close_after"]],
                       "reopened_pct": [R["reopen_before"], R["reopen_after"]],
                       "report_to_job_days": [0.25, 1.81], "report_to_fix_days": [4.85, 5.17]}, index=["before", "after"])
print(rm)
U.check(rm.loc["after", "median_close_days"] < rm.loc["before", "median_close_days"], "the target metric improved")
U.check(rm.loc["after", "reopened_pct"] > 3 * rm.loc["before", "reopened_pct"], "reopenings more than tripled")
U.check(rm.loc["after", "report_to_fix_days"] >= rm.loc["before", "report_to_fix_days"], "the customer waits no less for a fix")

# %% [markdown]
# 🔍 The clock starts at job creation. Look at `report_to_job_days`: who controls when a job is created?

# %% [markdown]
# ## 3 · First-contact resolution (6')
#
# ✏️ **Exercise** · Before and after month 13: the share of contacts marked resolved, and the share of contacts followed by
# another contact from the same account within seven days (sort by `day`, look at the next contact of each account).

# %%
con = U.csv("contacts")


def contact_metrics(df: pd.DataFrame) -> pd.DataFrame:
    # BEGIN SOLUTION
    d = df.sort_values(["account_id", "day"]).copy()
    d["next_day"] = d.groupby("account_id").day.shift(-1)
    d["repeat7"] = (d.next_day - d.day) <= 7
    d["period"] = (d.month >= U.TARGET_MONTH).map({False: "before", True: "after"})
    out = d.groupby("period").agg(marked_resolved_pct=("marked_resolved", "mean"), repeat7_pct=("repeat7", "mean"),
                                  handle_min=("handle_min", "mean"))
    out[["marked_resolved_pct", "repeat7_pct"]] *= 100
    return out.loc[["before", "after"]].round(1)
    # END SOLUTION


# %%
try:
    cm = contact_metrics(con)
except NotImplementedError:
    cm = pd.DataFrame({"marked_resolved_pct": [73.5, 85.9], "repeat7_pct": [22.7, 26.6], "handle_min": [7.7, 6.6]},
                      index=["before", "after"])
print(cm)
U.check(cm.loc["after", "marked_resolved_pct"] > cm.loc["before", "marked_resolved_pct"] + 8, "first-contact resolution rose")
U.check(cm.loc["after", "repeat7_pct"] > cm.loc["before", "repeat7_pct"], "but repeat contacts rose too")

# %% [markdown]
# ## 4 · How each proxy failed (4')
#
# ✏️ **Exercise** · Label three leaves with one of the four ways a proxy fails under pressure (Manheim and Garrabrant):
# `regressional` (selecting on a noisy proxy also selects the noise), `extremal` (pushed into a range where the old relation
# fails), `causal` (the action taken on the proxy breaks its link to the goal) or `adversarial` (people with other goals
# game it). Add one sentence of behaviour each.

# %%
MECHANISMS = ["regressional", "extremal", "causal", "adversarial"]


def labels() -> dict:
    # BEGIN SOLUTION
    return {
        "repair_time": ("adversarial", "Crews close at the first visit and dispatchers create jobs later: the clock is gamed"),
        "fcr": ("adversarial", "Agents mark calls resolved that are not, because the target counts in their bonus"),
        "leaks_found": ("causal", "Searching harder raises leaks found without less water being lost: effort moves the count"),
    }
    # END SOLUTION


# %%
try:
    lab = labels()
except NotImplementedError:
    lab = {"repair_time": ("adversarial", "(reference)"), "fcr": ("adversarial", "(reference)"),
           "leaks_found": ("causal", "(reference)")}
U.check(all(m in MECHANISMS for m, _ in lab.values()), "every label is one of the four mechanisms")
U.check(lab["repair_time"][0] == "adversarial" and lab["fcr"][0] == "adversarial", "the two targets are gamed by people")

# %% [markdown]
# ## 5 · Two guardrails (6')
#
# ✏️ **Exercise** · A guardrail is a second metric that gets worse when the first is gamed. For each: the metric, the leaf
# it guards, the behaviour it exposes, and its values before and after from your tables.

# %%
def guardrails() -> list[dict]:
    # BEGIN SOLUTION
    return [
        {"metric": "Jobs reopened after closure, %", "guards": "repair_time",
         "behaviour": "Closing a job before the leak is fixed", "before": float(rm.loc["before", "reopened_pct"]),
         "after": float(rm.loc["after", "reopened_pct"])},
        {"metric": "Contacts followed by another within 7 days, %", "guards": "fcr",
         "behaviour": "Marking a call resolved when the customer must call again", "before": float(cm.loc["before", "repeat7_pct"]),
         "after": float(cm.loc["after", "repeat7_pct"])},
    ]
    # END SOLUTION


# %%
try:
    gr = guardrails()
except NotImplementedError:
    gr = [{"metric": "Jobs reopened, %", "guards": "repair_time", "behaviour": "closing before the fix",
           "before": float(rm.loc["before", "reopened_pct"]), "after": float(rm.loc["after", "reopened_pct"])},
          {"metric": "Repeat within 7 days, %", "guards": "fcr", "behaviour": "marking unresolved calls resolved",
           "before": float(cm.loc["before", "repeat7_pct"]), "after": float(cm.loc["after", "repeat7_pct"])}]
U.check(len(gr) >= 2 and len({g["guards"] for g in gr}) >= 2, "two guardrails on two different leaves")
U.check(all(g["after"] > g["before"] for g in gr), "each guardrail shows the gaming in the data")
notes = {k: f"{m}: {b}" for k, (m, b) in lab.items()}
mmd = U.mermaid_tree(tree, notes, gr)
U.save("metric_tree_annotated.mmd", mmd)
print(mmd)
print(U.tutor("\n".join(f"{g['metric']} guards {g['guards']}: {g['behaviour']}" for g in gr),
              "would these guardrails themselves be easy to game?"))

# %% [markdown]
# ## ✱ Stretch · Estimates inside non-revenue water
#
# Al-Hamra could lower its non-revenue water on paper by estimating generously. Which guardrail would show it?

# %%
def estimate_guardrail() -> dict:
    # BEGIN SOLUTION
    r = U.csv("reads")
    share = 100 * (r.read_type == "estimated").groupby([r.district, r.month > 12]).mean().unstack()
    return {"metric": "Share of bills estimated, by district, %", "guards": "nrw",
            "al_hamra_year1": round(float(share.loc["D4", False]), 1), "al_hamra_year2": round(float(share.loc["D4", True]), 1)}
    # END SOLUTION


try:
    print(estimate_guardrail())
except NotImplementedError:
    print("stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Repair time halved. Why is that not good news yet?
#    <details><summary>Answer</summary>Reopenings rose more than fourfold and the customer's wait from report to fix did
#    not fall: the clock was moved, not the work.</details>
# 2. What makes a guardrail useful?
#    <details><summary>Answer</summary>It moves the opposite way when the target is gamed, and it is hard to game in the same
#    move.</details>
# 3. Why is "leaks found" a causal failure rather than an adversarial one?
#    <details><summary>Answer</summary>Nobody cheats: the decision to search harder itself raises the count, so the count
#    stops tracking water lost.</details>
#
# **Carry forward.** `out/metric_tree_annotated.mmd`. Lab 2.3 starts from the supplied card `data/card_2_3.json`.
