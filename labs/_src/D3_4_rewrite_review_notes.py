# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 3.4 · Notes that get acted on
#
# Day 3 · Session 4 (Review notes people act on) · 25 min.
#
# A colleague left eight review notes on Sabah's leak-detection analysis (variant 0 of Lab 3.2) and on Sareea's
# smart-meter summary (Lab 3.3). Each is too short to act on. You rewrite each as a problem, its consequence and a fix,
# rank them by consequence, ask the tutor to question two of them, and open the capstone brief.
#
# **AI policy: AI-tutor.** The tutor asks questions about your notes; it does not rewrite them.
#
# **Reference state.** `data/weak_notes.json`, `capstone/BRIEF.md`. The notes are about the variant-0 analysis and Sareea's
# summary, both supplied; nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Read the eight weak notes (3')
# - [ ] 2 · Rewrite each: problem, consequence, fix (12')
# - [ ] 3 · Rank by consequence (4')
# - [ ] 4 · Tutor feedback and one revision (4')
# - [ ] 5 · Open the capstone brief (2')
# - [ ] ✱ Stretch · Write the summary paragraph a manager reads first

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

import ghadeer as U

# %% [markdown]
# ## 1 · The weak notes (3')

# %%
weak = U.js("weak_notes")
for n in weak:
    print(n["id"], n["text"])

# %% [markdown]
# ## 2 · Rewrite each note (12')
#
# ✏️ **Exercise** · For every note: the **problem** (where, what exactly), the **consequence** (what it does to the number or
# the decision), and the **fix** (an action the author can take). `U.note_problems(note)` lists what a reader would
# still miss. The numbers you need are from Labs 3.2 and 3.3: the clean effect is 2.3 points (do not buy); the
# before-after alone gives 4.1 (buy); Sareea's -8.2% is +11.5% when recomputed.

# %%
def rewrite() -> list[dict]:
    # BEGIN SOLUTION
    return [
        {"id": "N8", "problem": "Cell c4 measures success as leaks found, which rose 3.4 times, not as water lost",
         "consequence": "The recommendation to buy loggers rests on activity; measured on water, the effect is 2.3 points and the decision is not to buy",
         "fix": "Report the change in non-revenue water against the other districts as the headline, and leaks found as context"},
        {"id": "N4", "problem": "Cell c3 compares Al-Wurud's months 10 to 12 with 13 to 15, with no comparison districts",
         "consequence": "The bulk-meter drift and regression to the mean add about 1.8 points, enough to cross the 3-point rule and reverse the decision",
         "fix": "Use months 1 to 9 against 15 to 24, bills rescaled to 30 days, against the other districts without Al-Nakheel"},
        {"id": "N6", "problem": "Sareea's summary cites an industry benchmark of 15% with no source",
         "consequence": "A number nobody can verify becomes the reason to roll out meters; the decision would rest on it",
         "fix": "Remove the benchmark, or replace it with a sourced figure and its reference"},
        {"id": "N7", "problem": "Sareea's analysis treats estimated bills in Al-Nakheel as actual reads",
         "consequence": "Estimates repeat past reads, so the before-after mixes billing timing with metering and the 11.5% rise is overstated or understated",
         "fix": "Recompute on actual reads only and report the share of estimates beside the result"},
        {"id": "N1", "problem": "Cell c2 joins repairs on the district name, and rows spelt 'Al Wurud' are dropped",
         "consequence": "About a third of Al-Wurud's repairs vanish from the leaks-found count, so any count-based claim is wrong",
         "fix": "Normalise the spelling or join on a district code, and assert the row count before and after the join"},
        {"id": "N3", "problem": "Sareea's summary states the fall as a fact with no interval or check of noise",
         "consequence": "The reader cannot tell a real change from month-to-month swing, so the claim looks more certain than it is",
         "fix": "Report an interval, as the corrected analysis does (1.4 to 3.3 points), and say what it means for the rule"},
        {"id": "N2", "problem": "The chart in cell c6 starts its axis at 20%, which makes a small fall look steep",
         "consequence": "The picture overstates the change for readers who look at the chart rather than the number in the text",
         "fix": "Start the axis at zero, or mark the axis break clearly and print the change on the chart"},
        {"id": "N5", "problem": "The repairs export spells the district as both 'Al Wurud' and 'Al-Wurud'",
         "consequence": "Cosmetic in the report itself, but it is the cause of the dropped rows of note N1",
         "fix": "Ask the export owner to use one spelling, and keep the join on the district code"},
    ]
    # END SOLUTION


# %%
try:
    notes = rewrite()
except NotImplementedError:
    notes = U.reference("review_notes")
gaps = [p for n in notes for p in U.note_problems(n)]
print("\n".join(gaps) or "every note has a full problem, consequence and fix")
U.check({n["id"] for n in notes} == {n["id"] for n in weak}, "all eight notes rewritten")
U.check(not gaps, "no note leaves the reader guessing")

# %% [markdown]
# ## 3 · Rank by consequence (4')
#
# ✏️ **Exercise** · Order the notes from the one that matters most to the decision to the one that matters least. The list
# order in your rewrite can already be the ranking.

# %%
def ranking() -> list[str]:
    # BEGIN SOLUTION
    return [n["id"] for n in notes]
    # END SOLUTION


# %%
try:
    order = ranking()
except NotImplementedError:
    sev = U.reference("note_severity")
    order = sorted(sev, key=lambda k: U.SEVERITY_ORDER[sev[k]])
sev = U.reference("note_severity")
levels = [U.SEVERITY_ORDER[sev[k]] for k in order]
print([f"{k} ({sev[k]})" for k in order])
U.check(set(order[:2]) == {k for k, v in sev.items() if v == "critical"}, "the two decision-changing notes come first")
U.check(set(order[-2:]) == {k for k, v in sev.items() if v == "minor"}, "the two cosmetic notes come last")
U.check(levels == sorted(levels), "no note sits above a more consequential one")

# %% [markdown]
# ## 4 · Tutor feedback and one revision (4')
#
# Ask the tutor about your top two notes. Revise one if a question exposes a gap.

# %%
by_id = {n["id"]: n for n in notes}
for k in order[:2]:
    n = by_id[k]
    print(k, U.tutor(f"{n['problem']}. {n['consequence']}. Fix: {n['fix']}", "would the author know exactly what to change?"), "\n")
md = ["# Review notes: leak detection (variant 0) and Sareea's smart-meter summary", "",
      "Ranked by consequence for the decision.", ""]
for i, k in enumerate(order, 1):
    n = by_id[k]
    md += [f"{i}. **{n['problem']}.** {n['consequence']}. *Fix:* {n['fix']}."]
U.save("review_notes.md", "\n".join(md) + "\n")

# %% [markdown]
# ## 5 · The capstone brief (2')
#
# The capstone uses the same three skills on a new case. Read the brief now; tomorrow you choose your analysis plan.

# %%
print((Path("capstone") / "BRIEF.md").read_text(encoding="utf-8"))

# %% [markdown]
# ## ✱ Stretch · The paragraph a manager reads first
#
# Three sentences for Nadia, before the numbered notes: the verdict, the main reason, what happens next.

# %%
def manager_summary() -> str:
    # BEGIN SOLUTION
    return ("The recommendation to buy loggers does not hold. Measured on water lost against the other districts, detection "
            "cut non-revenue water by 2.3 points, below the 3-point rule; the analysis counted leaks found and compared the "
            "wrong months. Sabah will rerun it with the fixes below before the capital committee meets.")
    # END SOLUTION


try:
    print(manager_summary())
except NotImplementedError:
    print("stretch not done")

# %% [markdown]
# ## Checkpoint
#
# 1. "The join looks off" names a real flaw. Why will it probably not be fixed?
#    <details><summary>Answer</summary>The author cannot tell where, how much it matters or what to do. A note gets acted
#    on when it names the cell, the consequence and the fix.</details>
# 2. Why is N5 (the spelling) ranked last although it causes N1?
#    <details><summary>Answer</summary>The note on the cause in the report changes nothing a reader decides; the
#    consequence lives in N1, which carries the fix that matters.</details>
# 3. What does the first line of a review owe its reader?
#    <details><summary>Answer</summary>The verdict on the decision: does the recommendation stand? Then the reasons, by
#    consequence.</details>
#
# **Carry forward.** `out/review_notes.md`, and the capstone brief in `labs/capstone/BRIEF.md`.
