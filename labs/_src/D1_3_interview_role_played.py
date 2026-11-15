# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas>=2.2"]
# ///

# %% [markdown]
# # Lab 1.3 · Interview the operations manager
#
# Day 1 · Session 3 (Interviewing a stakeholder) · 25 min.
#
# Sultana Al-Kanaan, customer service operations manager, sent request R3: "Repeat complaints are too high. Find out
# what is going on." Before anyone touches the data, you interview her: who decides and who is affected, what
# constrains the answer, and what evidence she would accept. You leave with an interview record.
#
# **Role-play.** The trainer, or a neighbour holding the role card, plays Sultana. Working alone, use the scripted
# stand-in `U.interview("sultana", question)`: it answers by topic and rewards open questions, like a real interview.
#
# **AI policy: AI-tutor.** A tutor may question your questions; it does not write them.
#
# **Reference state.** `data/requests.json`, `data/roles.json`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Read the request and the stakeholder map (3')
# - [ ] 2 · Write six open questions (6')
# - [ ] 3 · Interview: a role-play or the stand-in (8')
# - [ ] 4 · Record constraints and acceptable evidence (6')
# - [ ] 5 · List what you did not ask (2')
# - [ ] ✱ Stretch · Interview the data protection officer about the same request

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
# ## 1 · The request and the stakeholder map (3')
#
# ✏️ **Exercise** · Fill the map before the interview: who **decides**, who **uses** the answer, who is **affected** by the
# decision. Guess now; the interview will correct you.

# %%
r3 = next(r for r in U.js("requests")["framing"] if r["id"] == "R3")
print(r3["from"], "\n ", r3["text"])


def stakeholder_map() -> dict:
    # BEGIN SOLUTION
    return {"decides": ["Sultana Al-Kanaan, with Nadia Al-Rubaie for the call-centre contract"],
            "uses": ["Contact-centre team leaders", "The outsourced call-centre supplier"],
            "affected": ["Customers who call again", "Agents whose bonus depends on the target",
                         "Older customers in Al-Hamra who call about estimated bills"]}
    # END SOLUTION


# %%
try:
    smap = stakeholder_map()
except NotImplementedError:
    smap = U.reference("interview")["map"]
U.check(all(smap.get(k) for k in ("decides", "uses", "affected")), "the map has deciders, users and affected people")

# %% [markdown]
# ## 2 · Six open questions (6')
#
# ✏️ **Exercise** · Open questions start with what, how, when, who, which or tell me. A closed question ("Is it the
# agents?") gets yes or no; a leading one ("Don't you think it's the agents?") gets agreement. Ask about the decision,
# the deadline, how a repeat is counted, what she would believe, what was tried, and what limits the data.

# %%
def my_questions() -> list[str]:
    # BEGIN SOLUTION
    return [
        "What decision do you need to take about repeat complaints, and by when?",
        "How do you count a repeat contact today: how do you know it is the same customer?",
        "What evidence would convince you that a change worked, and what would you not trust?",
        "Which targets or incentives do the agents work under at the moment?",
        "What has changed in the contact centre in the last year that might matter?",
        "Which data about calls can we use, and what about the call recordings and personal data?",
    ]
    # END SOLUTION


# %%
try:
    questions = my_questions()
except NotImplementedError:
    questions = U.reference("interview")["questions"]
kinds = {q: U.question_kind(q) for q in questions}
for q, k in kinds.items():
    print(f"[{k:7}] {q}")
U.check(len(questions) >= 6, "six questions")
U.check(all(k == "open" for k in kinds.values()), "every question is open")

# %% [markdown]
# ## 3 · The interview (8')
#
# With a role-player: ask your questions in order, take notes, and follow up on surprises. With the stand-in: run the
# cell, read each answer, then add follow-ups to `follow_ups` and run again.

# %%
U.reset_interview("sultana")
follow_ups = [
    # ✏️ add follow-up questions here after reading the answers
    "Who is affected most by the repeat contacts?",
]
transcript = []
for q in questions + follow_ups:
    a = U.interview("sultana", q)
    transcript.append((q, a))
    print("Q:", q, "\n ", a, "\n")
found, total, missed = U.interview_coverage("sultana")
print(f"constraints reached: {found} of {total}")

# %% [markdown]
# ## 4 · The interview record (6')
#
# ✏️ **Exercise** · Write what you **heard**, apart from what you **assume**. Constraints limit the analysis (a deadline, a
# rule on data, a flaw in how something is counted). Acceptable evidence is what the decision maker will believe.

# %%
def interview_record() -> dict:
    # BEGIN SOLUTION
    return {
        "decision": "Whether to change the terms of the outsourced call-centre contract, renewed in four weeks",
        "constraints": [
            "Decision needed within four weeks, before the contract renewal",
            "The first-contact target counts towards agents' bonuses since month 13",
            "Contacts are linked by mobile number: a repeat from another phone is counted as a new customer",
            "Call recordings may not be analysed without the data protection officer's review",
        ],
        "acceptable_evidence": ["Repeat contacts within seven days", "Not the satisfaction survey: too few answers"],
        "heard": ["The call script was shortened in month 13 and handling time fell",
                  "Billing callers make most repeats; older customers in Al-Hamra call most about estimated bills"],
        "assumed": ["That repeat contacts rose after month 13: not yet checked in the data"],
    }
    # END SOLUTION


# %%
try:
    record = interview_record()
except NotImplementedError:
    record = U.reference("interview")["record"]
U.check(found >= 4, f"your questions reached at least four of the {total} constraints")
U.check(len(record["constraints"]) >= 3, "three or more constraints recorded")
U.check(len(record["acceptable_evidence"]) >= 1, "the evidence she would accept is recorded")
U.check(len(record["assumed"]) >= 1, "at least one assumption is written down as an assumption")
md = ["# Interview record: Sultana Al-Kanaan (request R3)", "", f"**Decision.** {record['decision']}", ""]
for k in ("constraints", "acceptable_evidence", "heard", "assumed"):
    md += [f"**{k.replace('_', ' ').capitalize()}**"] + [f"- {x}" for x in record[k]] + [""]
md += ["**Transcript**"] + [f"- Q: {q}\n  A: {a}" for q, a in transcript]
U.save("interview_sultana.md", "\n".join(md) + "\n")

# %% [markdown]
# ## 5 · What you did not ask (2')
#
# The stand-in tells you which constraint topics your questions never reached. With a live role-player, ask the
# trainer for the role card after the interview and compare.

# %%
print("not reached:", missed or "none")
print(U.tutor("\n".join(questions), "are my interview questions open and do they find the constraints?"))

# %% [markdown]
# ## ✱ Stretch · The data protection officer
#
# Interview Azizah Al-Matrood about R3: what may you use, for what purpose, and where may it be processed?

# %%
U.reset_interview("azizah")
for q in ["What personal data do we need for counting repeat contacts?",
          "How may we use the call recordings?",
          "Where may the contact-centre extract be processed, given its classification?"]:
    print("Q:", q, "\n ", U.interview("azizah", q), "\n")
print("constraints reached:", U.interview_coverage("azizah")[:2])

# %% [markdown]
# ## Checkpoint
#
# 1. Why did "Is it the agents' fault?" add nothing, even when the answer was yes?
#    <details><summary>Answer</summary>A closed or leading question gets agreement. It cannot surface the bonus target
#    or the mobile-number matching, which nobody would volunteer.</details>
# 2. Which constraint most changes the analysis of repeat contacts?
#    <details><summary>Answer</summary>Matching by mobile number: repeats from another phone are invisible, so the
#    repeat rate is a lower bound.</details>
# 3. Why record acceptable evidence before the analysis?
#    <details><summary>Answer</summary>So the analysis produces the evidence the decision maker will believe (repeats in
#    seven days), not a number she has already said she distrusts (survey scores).</details>
#
# **Carry forward.** `out/interview_sultana.md`. Lab 1.4 starts from `data/card_1_4.json` and `data/inventory.json`.
