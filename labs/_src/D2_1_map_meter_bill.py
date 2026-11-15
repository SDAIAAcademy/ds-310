# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 2.1 · The meter-to-bill map
#
# Day 2 · Session 1 (How the data are made) · 25 min.
#
# Non-revenue water is system input minus billed consumption. Before you plan any analysis of it, you learn how a meter
# read becomes a bill: from the briefing pack and from the metering engineer, Mamdouh Al-Qarawi. You draw the process as
# a Mermaid diagram and mark three points where the data mislead, each with a number from the data.
#
# **Role-play.** The trainer plays Mamdouh from the role card; alone, use `U.interview("mamdouh", question)`.
#
# **AI policy: AI-tutor.** A tutor may question your map; it does not draw it.
#
# **Reference state.** `data/briefing/`, `data/reads.csv`, `data/supply.csv`, `data/accounts.csv`. Nothing from Day 1.
#
# **Tasks**
# - [ ] 1 · Read the briefing pack (5')
# - [ ] 2 · Ask the metering engineer three questions (5')
# - [ ] 3 · The process as a Mermaid map (5')
# - [ ] 4 · Three points where the data mislead, with numbers (8')
# - [ ] 5 · Save the map (2')
# - [ ] ✱ Stretch · Add a fourth mark on the leak-repair work order

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
# ## 1 · The briefing pack (5')

# %%
for name in ("metering.md", "billing_cycles.md", "leak_repair.md"):
    print(U.text(f"briefing/{name}"))

# %% [markdown]
# ## 2 · Ask the engineer (5')
#
# ✏️ **Exercise** · Three open questions about what the briefing leaves vague: when a bill is an estimate, how long a
# "monthly" bill is, what changed with the meters. Then read the answers.

# %%
def my_questions() -> list[str]:
    # BEGIN SOLUTION
    return ["What happens to a bill when the reader cannot reach the meter?",
            "How many days does one billing period cover, and why does it vary?",
            "How accurate are the old meters compared with the smart meters in Al-Nakheel?"]
    # END SOLUTION


# %%
try:
    qs = my_questions()
except NotImplementedError:
    qs = ["What happens when the reader cannot reach the meter and the bill is estimated?",
          "How many days does a billing cycle cover?", "How accurate are old meters compared with smart ones?"]
U.reset_interview("mamdouh")
for q in qs:
    print("Q:", q, "\n ", U.interview("mamdouh", q), "\n")
found, total, missed = U.interview_coverage("mamdouh")
U.check(found >= 3, f"your questions reached three of the engineer's {total} topics")

# %% [markdown]
# ## 3 · The process (5')
#
# ✏️ **Exercise** · List the steps from the water at the meter to the number in the non-revenue water report, in order. Six to
# eight short steps.

# %%
def process_steps() -> list[str]:
    # BEGIN SOLUTION
    return ["Water passes the customer meter", "Reader visits on a route (27 to 35 days)",
            "Read taken, or estimate from the last three reads", "Bill issued for the period ending this month",
            "Bills summed by district and month", "Bulk meter gives district input for the calendar month",
            "Non-revenue water = input minus billed"]
    # END SOLUTION


# %%
try:
    steps = process_steps()
except NotImplementedError:
    steps = ["Customer meter", "Reader visit", "Read or estimate", "Bill for the period", "Billed by district-month",
             "Bulk-meter input", "Non-revenue water"]
U.check(6 <= len(steps) <= 8, "six to eight steps")
print(U.mermaid_flow(steps))

# %% [markdown]
# ## 4 · Three points where the data mislead (8')
#
# Each mark needs a number from the data. Three exercises, one per mark.
#
# ✏️ **4a · Estimates.** The share of bills estimated, by district, in percent.

# %%
reads = U.csv("reads")


def estimated_share(df: pd.DataFrame) -> pd.Series:
    # BEGIN SOLUTION
    return (100 * (df.read_type == "estimated").groupby(df.district).mean()).round(1)
    # END SOLUTION


# %%
try:
    est = estimated_share(reads)
except NotImplementedError:
    est = pd.Series(U.reference("numbers")["estimated_share"])
print(est)
U.check(est.idxmax() == "D4" and est["D4"] > 3 * est.drop("D4").mean(), "Al-Hamra estimates far more bills than the rest")

# %% [markdown]
# ✏️ **4b · Billing cycles.** Monthly non-revenue water swings because a bill covers 27 to 35 days while the bulk meter
# covers a calendar month. Return the standard deviation of monthly non-revenue water in Al-Salam (D5), months 1 to 12,
# raw and with bills rescaled to 30 days (`U.nrw(normalise_cycle=True)`).

# %%
def cycle_noise() -> tuple[float, float]:
    # BEGIN SOLUTION
    raw, norm = U.nrw(), U.nrw(normalise_cycle=True)
    sel = lambda d: d[(d.district == "D5") & (d.month <= 12)].nrw_pct.std()
    return round(float(sel(raw)), 2), round(float(sel(norm)), 2)
    # END SOLUTION


# %%
try:
    sd_raw, sd_norm = cycle_noise()
except NotImplementedError:
    raw, norm = U.nrw(), U.nrw(normalise_cycle=True)
    sd_raw = round(float(raw[(raw.district == "D5") & (raw.month <= 12)].nrw_pct.std()), 2)
    sd_norm = round(float(norm[(norm.district == "D5") & (norm.month <= 12)].nrw_pct.std()), 2)
print(f"Al-Salam monthly non-revenue water, sd: raw {sd_raw} points, rescaled {sd_norm} points")
U.check(sd_raw > 2.5 * sd_norm, "rescaling to 30 days removes most of the monthly swing")

# %% [markdown]
# ✏️ **4c · Meter swap.** Billed m3 per account per 30 days in Al-Nakheel (D3), year 2 against year 1, in percent; and the
# same change in the other five districts. The difference is what the smart meters measure that the old ones missed.

# %%
def meter_step() -> tuple[float, float]:
    # BEGIN SOLUTION
    r = reads.assign(per30=reads.billed_m3 / reads.cycle_days * 30, year=(reads.month > 12).astype(int) + 1)
    r = r[r.read_type == "actual"]
    g = r.groupby([r.district == "D3", "year"]).per30.mean()
    d3 = 100 * (g[(True, 2)] / g[(True, 1)] - 1)
    rest = 100 * (g[(False, 2)] / g[(False, 1)] - 1)
    return round(float(d3), 1), round(float(rest), 1)
    # END SOLUTION


# %%
try:
    d3_change, rest_change = meter_step()
except NotImplementedError:
    d3_change, rest_change = 12.1, -1.6  # the reference run
print(f"billed per account per 30 days, year 2 against year 1: Al-Nakheel {d3_change:+.1f}%, other districts {rest_change:+.1f}%")
U.check(d3_change - rest_change > 8, "Al-Nakheel's bills jump with the smart meters while use elsewhere is flat")
nr = U.nrw(normalise_cycle=True)
print(f"Al-Nakheel non-revenue water, bills rescaled: year 1 {U.period_mean(nr, 'D3', range(1, 13)):.1f}%, "
      f"year 2 {U.period_mean(nr, 'D3', range(13, 25)):.1f}%")

# %% [markdown]
# ## 5 · The map with its marks (2')
#
# ✏️ Attach each mark to the step where the data are made wrong. Paste the saved `.mmd` text into a Mermaid viewer or
# draw.io (Arrange, Insert, Mermaid) to see the picture.

# %%
marks = {
    3: f"Estimates: {est['D4']}% of Al-Hamra bills, average of past reads, miss the summer rise",
    2: f"Cycle 27 to 35 days: monthly NRW sd {sd_raw} points raw, {sd_norm} rescaled",
    1: f"Smart meters in Al-Nakheel: billed per account {d3_change:+.1f}% against {rest_change:+.1f}% elsewhere",
}
mmd = U.mermaid_flow(steps, marks)
U.save("meter_to_bill.mmd", mmd)
print(mmd)
U.check(len(marks) >= 3 and all(any(ch.isdigit() for ch in m) for m in marks.values()), "three marks, each with a number")

# %% [markdown]
# ## ✱ Stretch · The repair work order
#
# Add a fourth mark: since the three-day target, how is "job closed" recorded, and what does that do to repair time?
# Ask Mamdouh, then read `briefing/leak_repair.md` again. Lab 2.2 measures it.

# %%
print(U.interview("mamdouh", "When is a repair job closed, and what happens if the leak returns?"))

# %% [markdown]
# ## Checkpoint
#
# 1. Al-Nakheel's non-revenue water fell after the smart meters. Did it lose less water?
#    <details><summary>Answer</summary>Not necessarily: the new meters bill water the old ones missed, so apparent losses
#    fell. Real losses (leaks) may be unchanged.</details>
# 2. Why does a "monthly" non-revenue water figure swing even when nothing changes?
#    <details><summary>Answer</summary>The bill covers 27 to 35 days and the bulk meter a calendar month; a long billing
#    period inflates billed volume and deflates non-revenue water.</details>
# 3. Why do estimated bills hurt most in summer?
#    <details><summary>Answer</summary>They average past reads and miss the seasonal rise; the next actual read catches
#    up, so the error moves between months.</details>
#
# **Carry forward.** `out/meter_to_bill.mmd`. Lab 2.2 starts from `data/metric_tree.json`.
