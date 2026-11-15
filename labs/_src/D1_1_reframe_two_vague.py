# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 1.1 · Two framing cards (AI-off)
#
# Day 1 · Session 1 (Requests are not questions) · 25 min.
#
# Two managers of Ghadeer Water Company sent vague requests. You turn each into a framing card: who decides, between
# which options, the estimand (population, variable, contrast, intercurrent events, summary), the decision rule, who is
# affected and whether personal data are needed at all. A peer must be able to plan from the card without asking you.
#
# **AI policy: AI-off.** Do this lab without an assistant. The supervised framing check of the assessment is AI-off too.
#
# **Reference state.** `data/requests.json`, `data/reads.csv`, `data/supply.csv`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Read the two requests and the baseline numbers (4')
# - [ ] 2 · Card 1: decision maker, decision and options (6')
# - [ ] 3 · Card 1: estimand and decision rule (6')
# - [ ] 4 · Card 2: the same, faster (6')
# - [ ] 5 · Peer test: what a planner would still ask (3')
# - [ ] ✱ Stretch · Frame a third request and swap it with a neighbour

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
# ## 1 · The two requests and the baseline numbers (4')
#
# Read both requests. Then compute two baseline numbers per district: non-revenue water for the last 12 months (13 to 24)
# in percent (`U.nrw()` gives it per district and month), and the share of bills estimated over the two years
# (`read_type == "estimated"` in `reads.csv`).
#
# ✏️ **Exercise** · Return a DataFrame indexed by district with the columns `nrw_pct` and `estimated_pct`, one decimal.

# %%
req = {r["id"]: r for r in U.js("requests")["framing"]}
for rid in ("R4", "R2"):
    print(f"{rid} · {req[rid]['from']}\n   \"{req[rid]['text']}\"\n")


def baseline() -> pd.DataFrame:
    # BEGIN SOLUTION
    n = U.nrw()
    last = n[n.month >= 13].groupby("district").nrw_pct.mean()
    reads = U.csv("reads")
    est = reads.groupby("district").read_type.apply(lambda s: 100 * (s == "estimated").mean())
    return pd.DataFrame({"nrw_pct": last.round(1), "estimated_pct": est.round(1)})
    # END SOLUTION


# %%
try:
    base = baseline()
except NotImplementedError:
    R = U.reference("numbers")
    base = pd.DataFrame({"nrw_pct": R["nrw_last12"], "estimated_pct": R["estimated_share"]})
print(base)
U.check(abs(base.loc["D1", "nrw_pct"] - U.reference("numbers")["nrw_last12"]["D1"]) < 0.05, "non-revenue water matches")
U.check(base.estimated_pct.idxmax() == "D4", "Al-Hamra (D4) has the most estimated bills")

# %% [markdown]
# 🔍 Request R4 says the pilot "found lots of leaks". Is the number of leaks found the thing the company wants, or a
# step towards it? Keep the answer in mind for the estimand.

# %% [markdown]
# ## 2 · Card 1, from R4: decision maker, decision, options (6')
#
# ✏️ **Exercise** · The decision is a question that ends in a choice ("Should ...?", "Which ...?"), not a topic. Give
# at least three options and keep "do nothing" among them.

# %%
def card1_part_one() -> dict:
    # BEGIN SOLUTION
    return {
        "decision_maker": "Nadia Al-Rubaie, director of non-revenue water, with the capital committee",
        "decision": "Should Ghadeer buy acoustic loggers for active leak detection in Al-Rawdah and Al-Hamra next year?",
        "options": ["Buy loggers for both districts", "Buy loggers for Al-Rawdah only",
                    "Do not buy: keep repairing leaks on customer reports, as now"],
    }
    # END SOLUTION


# %%
try:
    c1a = card1_part_one()
except NotImplementedError:
    c1a = {k: U.reference("card_2_3")[k] for k in ("decision_maker", "decision", "options")}
U.check(c1a["decision"].strip().endswith("?"), "the decision is a question")
U.check(len(c1a["options"]) >= 3, "three or more options")
U.check(any("not" in o.lower() or "as now" in o.lower() for o in c1a["options"]), "doing nothing is an option")

# %% [markdown]
# ## 3 · Card 1: estimand, decision rule, affected, personal data (6')
#
# ✏️ **Exercise** · The estimand has five parts: the **population** (which units, which period), the **variable** (what
# is measured on each unit), the **contrast** (with what against without what), the **intercurrent** events (what
# happens along the way that changes the meaning, and how you treat it) and the **summary** (the one number). The
# decision rule says at what value of that number the choice changes. Use the baseline numbers.

# %%
def card1_part_two() -> dict:
    # BEGIN SOLUTION
    return {
        "estimand": {
            "population": "District-months of the six districts, months 1 to 24",
            "variable": "Non-revenue water in percent of system input, bills rescaled to 30 days",
            "contrast": "Al-Wurud with active detection (from month 13) against the five districts without it",
            "intercurrent": "The Al-Wurud bulk meter was recalibrated in month 13: compare from month 13 on, not with months 10 to 12",
            "summary": "Difference in differences of mean non-revenue water, in percentage points",
        },
        "decision_rule": "Buy loggers for a district if detection cut non-revenue water by at least 3 points in Al-Wurud "
                         "and the district's own non-revenue water is above 25%",
        "affected": ["Customers in the districts, who face interruptions during repairs", "Repair crews",
                     "The capital budget, which funds either loggers or mains renewal"],
        "personal_data_needed": False,
        "personal_data_note": "District totals answer the question; no names, mobiles or national IDs are needed",
    }
    # END SOLUTION


# %%
try:
    c1b = card1_part_two()
except NotImplementedError:
    ref = U.reference("card_2_3")
    c1b = {k: ref[k] for k in ("estimand", "decision_rule", "affected", "personal_data_needed")}
card1 = {**c1a, **c1b}
U.check(all(str(card1["estimand"].get(k, "")).strip() for k in U.ESTIMAND_FIELDS), "the estimand has its five parts")
U.check(any(ch.isdigit() for ch in card1["decision_rule"]), "the decision rule has a number")
U.check(card1["personal_data_needed"] in (True, False), "personal data: a yes or a no")

# %% [markdown]
# ## 4 · Card 2, from R2: the whole card, faster (6')
#
# ✏️ **Exercise** · Khalil's request is descriptive: the contrast can be between groups (accounts with and without a
# meter-access problem) rather than between treatments. A descriptive card still has a decision.

# %%
def card2() -> dict:
    # BEGIN SOLUTION
    return {
        "decision_maker": "Khalil Al-Sabhi, billing manager",
        "decision": "Should Ghadeer book a second reading visit for Al-Hamra accounts whose meters the reader cannot reach?",
        "options": ["Book a second visit for every account with an estimated bill",
                    "Move hard-to-reach meters to the property boundary", "Do nothing: keep estimating, as now"],
        "estimand": {
            "population": "Al-Hamra accounts billed in months 13 to 24",
            "variable": "Whether a bill is estimated, and the correction at the next actual read in m3",
            "contrast": "Accounts with a meter-access problem against accounts without one",
            "intercurrent": "Accounts that closed or changed meter in the period are left out and counted",
            "summary": "Share of bills estimated, in percent, and the mean correction per estimated bill",
        },
        "decision_rule": "Book second visits if more than 10% of Al-Hamra bills are estimated",
        "affected": ["Customers who receive estimated bills, often older residents", "Meter readers", "The billing team"],
        "personal_data_needed": False,
        "personal_data_note": "Account IDs and read types are enough; names, mobiles and national IDs are not needed",
    }
    # END SOLUTION


# %%
try:
    card2_ = card2()
except NotImplementedError:
    card2_ = None
    print("card 2 not done yet: the peer test below uses card 1 only")

# %% [markdown]
# ## 5 · Peer test (3')
#
# `U.card_gaps(card)` lists the questions a planner would still have to ask: missing parts, a decision that is not a
# choice, a rule without a number, vague words. Aim for none. Then give the saved cards to your neighbour and ask them
# to say, without asking you, what data they would fetch first.

# %%
cards = {"card_1_R4": card1} | ({"card_2_R2": card2_} if card2_ else {})
for name, c in cards.items():
    gaps = U.card_gaps(c)
    print(name, "→", gaps or "no questions left")
    U.save(f"{name}.md", U.card_markdown(c, name))
U.check(not U.card_gaps(card1), "card 1 leaves a planner no questions")
if card2_:
    U.check(not U.card_gaps(card2_), "card 2 leaves a planner no questions")
print("Al-Hamra estimated share:", base.loc["D4", "estimated_pct"], "% → rule threshold 10%")

# %% [markdown]
# ## ✱ Stretch · R5, the smart meters
#
# Frame request R5. Careful: "consumption went up" after the new meters. Is that more water used, or more water
# measured? Your estimand decides which question you answer.

# %%
def card3() -> dict:
    # BEGIN SOLUTION
    return {
        "decision_maker": "Nadia Al-Rubaie", "decision": "Should Ghadeer replace mechanical meters with smart meters in Al-Hamra next year?",
        "options": ["Replace all meters", "Replace meters older than eight years", "Do not replace"],
        "estimand": {"population": "Al-Nakheel accounts, months 1 to 24, against accounts of the other districts",
                     "variable": "Billed m3 per account rescaled to 30 days, and district non-revenue water",
                     "contrast": "With smart meters (Al-Nakheel from month 13) against mechanical meters",
                     "intercurrent": "Seasonal rise in summer: compare the same months of the two years",
                     "summary": "Difference in differences of billed m3 per account and of non-revenue water, in percent and points"},
        "decision_rule": "Replace if billed water rises by at least 5% at the same real use, which pays for the meters",
        "affected": ["Customers whose bills rise", "Meter readers"], "personal_data_needed": False,
    }
    # END SOLUTION


try:
    print(U.card_gaps(card3()) or "card 3: no questions left")
except NotImplementedError:
    print("stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. Why is "find out why water loss is high" not yet a question you can plan from?
#    <details><summary>Answer</summary>It names a topic, not a decision: no options, no population, no number at which
#    anyone would act differently.</details>
# 2. In card 1, why is "leaks found" a poor variable?
#    <details><summary>Answer</summary>Active detection finds more leaks by design. The company wants less water lost:
#    leaks found is an activity, non-revenue water is the outcome.</details>
# 3. Why does the card say whether personal data are needed?
#    <details><summary>Answer</summary>The Personal Data Protection Law limits collection to the minimum the purpose
#    needs. Deciding it on the card stops a plan from asking for names and national IDs "just in case".</details>
#
# **Carry forward.** `out/card_1_R4.md`, `out/card_2_R2.md`. Lab 1.2 starts from `data/requests.json` only.
