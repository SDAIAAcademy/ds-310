# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 3.3 · Verify the assistant's analysis
#
# Day 3 · Session 3 (Reviewing assistant-generated analysis) · 25 min.
#
# Sabah asked the assistant Sareea whether the smart meters in Al-Nakheel changed consumption. Sareea returned a notebook
# and a confident summary for Nadia. You rerun the notebook, run four checks, and write a verification note: what may be
# used, what may not, and why. The note labels the work as assistant-generated, as the Generative AI Guidelines for
# Government ask of users: identify such content and verify it, code included, before it is used.
#
# **AI policy: AI-tutor.** A tutor may question your note. The stretch asks a hosted model for the same analysis.
#
# **Reference state.** `data/review/sareea/` (prompt, notebook, summary), `data/reads.csv`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Read the prompt and the summary the assistant gave (3')
# - [ ] 2 · Rerun the notebook (5')
# - [ ] 3 · Where it fails: four checks (9')
# - [ ] 4 · Write the verification note (6')
# - [ ] 5 · Label the assistant's part (2')
# - [ ] ✱ Stretch · Ask a free hosted model for the same analysis and verify its answer

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

import re
import ghadeer as U

# %% [markdown]
# ## 1 · The prompt and the summary (3')

# %%
prompt = U.text("review/sareea/prompt.md")
summary = U.text("review/sareea/summary.md")
notebook = U.text("review/sareea/notebook.py")
print(prompt, "\n", summary, "\n", notebook)

# %% [markdown]
# ## 2 · Rerun (5')

# %%
res = U.run_cells(notebook)
for cid, r in res.items():
    if cid != "_env":
        print(f"cell {cid}: {r['status']}  {r['out'].strip()}")
reruns = all(r["status"] == "ok" for k, r in res.items() if k != "_env")
print("reruns as delivered:", reruns)

# %% [markdown]
# ## 3 · Four checks (9')
#
# ✏️ **3a · Repair and recompute.** The notebook names a column that does not exist. Recompute what it meant to compute,
# with the real column (`billed_m3`), and return before, after and the change in percent.

# %%
reads = U.csv("reads")


def recompute() -> dict:
    # BEGIN SOLUTION
    d3 = reads[reads.district == "D3"]
    before, after = d3[d3.month <= 12].billed_m3.mean(), d3[d3.month >= 13].billed_m3.mean()
    return {"before": round(float(before), 1), "after": round(float(after), 1),
            "change_pct": round(float(100 * (after - before) / before), 1)}
    # END SOLUTION


# %%
try:
    rc = recompute()
except NotImplementedError:
    d3 = reads[reads.district == "D3"]
    b, a = d3[d3.month <= 12].billed_m3.mean(), d3[d3.month >= 13].billed_m3.mean()
    rc = {"before": round(float(b), 1), "after": round(float(a), 1), "change_pct": round(float(100 * (a - b) / b), 1)}
print(rc)

# %% [markdown]
# ✏️ **3b to 3d** · Return the four checks as `{check: (passed, evidence)}`:
# - `reruns`: does the notebook run as delivered?
# - `numbers_traced`: is every number of the summary in the recomputed output?
# - `outside_numbers_sourced`: does every number from outside the data carry a source?
# - `method_fits_question`: does the method answer the question asked (consumption), given how smart meters measure?

# %%
summary_numbers = re.findall(r"\d+(?:\.\d+)?", summary)
print("numbers in the summary:", summary_numbers)


def four_checks() -> dict:
    # BEGIN SOLUTION
    traced = {str(rc["before"]), str(rc["after"]), str(abs(rc["change_pct"]))}
    return {
        "reruns": (reruns, "Cell s2 raises KeyError: 'consumption' is not a column of reads.csv"),
        "numbers_traced": (set(summary_numbers) <= traced,
                           f"Summary says 21.4 to 19.6 m3 (-8.2%); the recomputed means are {rc['before']} to {rc['after']} "
                           f"m3 ({rc['change_pct']:+.1f}%): the direction is reversed"),
        "outside_numbers_sourced": (False, "The 'industry benchmark of 15%' has no source and is not in any Ghadeer data"),
        "method_fits_question": (False, "Billed m3 measures what the meters register: new meters bill water the old ones "
                                        "missed, so a change in bills is not a change in consumption"),
    }
    # END SOLUTION


# %%
try:
    checks = four_checks()
except NotImplementedError:
    checks = {"reruns": (reruns, "(reference)"), "numbers_traced": (False, "(reference)"),
              "outside_numbers_sourced": (False, "(reference)"), "method_fits_question": (False, "(reference)")}
for k, (ok, why) in checks.items():
    print(f"{'pass' if ok else 'FAIL'}  {k}: {why}")
U.check(not checks["reruns"][0], "the rerun failure is recorded")
U.check(rc["change_pct"] > 0, "the recomputed change is a rise, not a fall")
U.check(sum(not ok for ok, _ in checks.values()) == 4, "all four checks fail, each with its evidence")

# %% [markdown]
# ## 4 · The verification note (6')
#
# ✏️ **Exercise** · A note Nadia can act on: the status, what may be used, what may not, and what to do next.

# %%
def verification_note() -> dict:
    # BEGIN SOLUTION
    return {
        "status": "Not verified: do not use the summary",
        "may_use": f"Billed m3 per account in Al-Nakheel rose from {rc['before']} to {rc['after']} ({rc['change_pct']:+.1f}%) after the smart meters",
        "may_not_use": "The claim that consumption fell 8.2%, the 15% benchmark and the advice to roll out to other districts",
        "next": "Measure consumption another way (night flow at the district meter) and compare with districts without smart meters",
    }
    # END SOLUTION


# %%
try:
    note = verification_note()
except NotImplementedError:
    note = {"status": "Not verified", "may_use": "(reference)", "may_not_use": "(reference)", "next": "(reference)"}
U.check(note["status"].lower().startswith("not verified"), "the status is stated first")

# %% [markdown]
# ## 5 · Label the assistant's part (2')
#
# Whatever is reused from Sareea's work is labelled as assistant-generated, with who verified it and how.

# %%
label = ("Assistant-generated: notebook and summary by Sareea from Sabah Al-Huwaidi's prompt. Rerun and checked by the reviewer; "
         "the summary failed verification and is withdrawn.")
md = ["# Verification note: Sareea's smart-meter analysis", "", f"**Status.** {note['status']}", "",
      f"**May be used.** {note['may_use']}", "", f"**May not be used.** {note['may_not_use']}", "",
      f"**Next.** {note['next']}", "", "**Checks**"] + [f"- {'pass' if ok else 'fail'}: {k}: {why}" for k, (ok, why) in checks.items()]
md += ["", f"*{label}*"]
U.save("verification_note.md", "\n".join(md) + "\n")
print(U.tutor("\n".join(md), "would Nadia know what she may use from this note?"))

# %% [markdown]
# ## ✱ Stretch · A hosted model
#
# Send the same prompt to a free hosted model and verify what comes back with the same four checks. Without a key, or
# when the free model does not answer, the recorded answer of Sareea is returned and says so.

# %%
source, answer = U.assistant(prompt + "\nThe columns of reads.csv are: " + ", ".join(reads.columns))
print("source:", source)
print(answer[:1500])

# %% [markdown]
# ## Checkpoint
#
# 1. The summary was fluent and gave three precise numbers. What did the rerun show?
#    <details><summary>Answer</summary>The notebook does not run, and the corrected computation shows a rise of about 11%,
#    not a fall of 8.2%: none of the three numbers came from the data.</details>
# 2. Why is the 15% benchmark a finding in itself?
#    <details><summary>Answer</summary>A number from outside the data with no source cannot be verified; an assistant can
#    produce one that sounds right. It is withdrawn until someone finds a source.</details>
# 3. Even with the right column, why does the method not answer the question?
#    <details><summary>Answer</summary>The meters changed how water is measured. Bills rose because the new meters register
#    more, not because people used more: a measurement change, as on Day 2.</details>
#
# **Carry forward.** `out/verification_note.md`. Lab 3.4 starts from `data/weak_notes.json`.
