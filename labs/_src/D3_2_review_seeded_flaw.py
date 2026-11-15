# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2", "matplotlib>=3.9"]
# ///

# %% [markdown]
# # Lab 3.2 · Rank the flaws of your variant
#
# Day 3 · Session 2 (Finding the flaws that matter) · 25 min.
#
# Sabah analysed whether active leak detection in Al-Wurud cut water loss, and recommends buying loggers. Each
# participant gets a variant of that notebook with four seeded flaws of its own, chosen from seven kinds. You rerun it,
# find the flaws cell by cell, measure what each does to the answer, and rank them by consequence.
#
# **Your variant.** Set `MY_NUMBER` to the participant number the trainer gives you (1 to 40). Variant 0 is the one the
# trainer demonstrates; its solution is shown.
#
# **AI policy: AI-tutor.** A tutor may question your ranking; it does not find flaws for you.
#
# **Reference state.** `U.seeded_analysis(MY_NUMBER)` builds the notebook from `data/`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Load your variant and rerun it (5')
# - [ ] 2 · Find the flaws, cell by cell (9')
# - [ ] 3 · Consequence of each, with a recomputed number (6')
# - [ ] 4 · Rank by consequence (3')
# - [ ] 5 · Check your flags (2')
# - [ ] ✱ Stretch · Fix the top flaw and rerun the analysis

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

MY_NUMBER = int(os.getenv("GHADEER_PARTICIPANT", "0"))  # ✏️ your participant number

# %% [markdown]
# ## 1 · Load and rerun (5')

# %%
src = U.seeded_analysis(MY_NUMBER)
print(src)
run = U.run_seeded(MY_NUMBER)
print("=== output ===\n" + run["output"])

# %% [markdown]
# ## 2 · Find the flaws (9')
#
# The seven kinds of flaw in the pool are below; your variant holds four of them. Read each cell against the checklist
# of Lab 3.1 and against what you know of the data (Day 2).
#
# ✏️ **Exercise** · Return `{flaw id: cell id}` for the four flaws you find.

# %%
for k, v in U.FLAW_CATALOGUE.items():
    print(k, v)


def my_flags() -> dict:
    # BEGIN SOLUTION
    return {"F1": "c4", "F2": "c2", "F3": "c3", "F6": "c6"}
    # END SOLUTION


# %%
try:
    flags = my_flags()
except NotImplementedError:
    flags = {f: "?" for f in U.variant_flaws(MY_NUMBER)}  # safety net: the variant's own flaws, so later cells run
U.check(len(flags) == 4 and set(flags) <= set(U.FLAW_CATALOGUE), "four flags from the pool")

# %% [markdown]
# ## 3 · Consequence of each (6')
#
# `U.consequence(MY_NUMBER, flaw)` runs the analysis with only that flaw and with none, and reports the effect in points and
# the decision for each. A flaw that changes no number may still mislead the reader (a chart, a claim of certainty).

# %%
cons = pd.DataFrame([U.consequence(MY_NUMBER, f) for f in flags]).set_index("flaw")
print(cons[["clean_effect", "flawed_effect", "change_points", "flips_decision", "flawed_decision"]].to_string())
print("\nthe analysis with no flaw:", U.run_seeded(MY_NUMBER, fix=list(U.FLAW_CATALOGUE))["output"].strip().splitlines()[-2:])

# %% [markdown]
# ## 4 · Rank by consequence (3')
#
# ✏️ **Exercise** · Order your flags from the most to the least consequential. A flaw that flips the decision comes
# first; then the size of the change in points; then flaws that mislead without moving a number.

# %%
def my_ranking() -> list[str]:
    # BEGIN SOLUTION
    c = cons.assign(size=cons.change_points.abs().fillna(99))
    return c.sort_values(["flips_decision", "size"], ascending=[False, False]).index.tolist()
    # END SOLUTION


# %%
try:
    ranking = my_ranking()
except NotImplementedError:
    c = cons.assign(size=cons.change_points.abs().fillna(99))
    ranking = c.sort_values(["flips_decision", "size"], ascending=[False, False]).index.tolist()
print("ranking:", ranking)
U.check(set(ranking) == set(flags), "every flag is ranked")
U.check(bool(cons.loc[ranking[0], "flips_decision"]) or not cons.flips_decision.any(),
        "a flaw that flips the decision comes first")
flips = [f for f in ranking if cons.loc[f, "flips_decision"]]
U.check(ranking[:len(flips)] == flips, "every decision-flipping flaw is above every other")

# %% [markdown]
# ## 5 · Check your flags (2')
#
# The check compares a hash of your four flags with the hash of your variant: it says right or wrong without revealing
# the key. In the capstone, review notes are matched against your own seeded flaws in the same way.

# %%
ok = U.flags_correct(MY_NUMBER, list(flags))
print("flags correct" if ok else "not all flags are right: look again at the cells the checklist points to")
U.check(ok, "your four flags are the seeded ones")
md = [f"# Review of variant {MY_NUMBER}: leak detection in Al-Wurud", "", "| Rank | Flaw | Cell | Consequence |", "|---|---|---|---|"]
for i, f in enumerate(ranking, 1):
    r = cons.loc[f]
    what = ("flips the decision to " + str(r.flawed_decision)) if r.flips_decision else (
        f"moves the effect by {r.change_points} points" if r.change_points else "misleads without changing the number")
    md.append(f"| {i} | {U.FLAW_CATALOGUE[f]} | {flags[f]} | {what} |")
U.save(f"review_variant_{MY_NUMBER}.md", "\n".join(md) + "\n")

# %% [markdown]
# ## ✱ Stretch · Fix the top flaw
#
# Rerun with your top flaw fixed. Does the recommendation change? With all four fixed?

# %%
for fix in ([ranking[0]], list(flags)):
    r = U.run_seeded(MY_NUMBER, fix=fix)
    print(f"fixed {fix}: effect {r['effect_points']} points, decision: {r['decision']}")

# %% [markdown]
# ## Checkpoint
#
# 1. Why rank a flaw that changes no number below one that flips the decision?
#    <details><summary>Answer</summary>The reader acts on the decision. A flaw that flips it costs a wrong purchase; a
#    misleading axis costs a misread chart, which the right number can correct.</details>
# 2. In variant 0, the join drops a third of Al-Wurud's repair rows, yet changes the effect by 0 points. Why?
#    <details><summary>Answer</summary>The effect is computed from the water balance, not from repairs; the join only
#    feeds the leaks-found count, which matters through the question-fit flaw.</details>
# 3. Why check flags by hash rather than against a visible key?
#    <details><summary>Answer</summary>Each participant's flaws differ and the key stays unseen: the same design makes the
#    capstone review notes authentic.</details>
#
# **Carry forward.** `out/review_variant_<n>.md`. Lab 3.3 starts from `data/review/sareea/`.
