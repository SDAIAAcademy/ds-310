---
course: "Problem Framing and Analytical Review"
code: "DS-310"
version: "2027.1.0"
deck: "capstone"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-310/slides/capstone.html"
---

# Problem Framing and Analytical Review

## Capstone: Capstone: the permits backlog, framed and defended

An 8-minute talk while the sponsor changes a constraint, then 10 minutes of defence

#### [capstone#title] Capstone: the permits backlog, framed and defended

*SDAIA Academy · Problem Framing and Analytical Review*

Capstone: An 8-minute talk while the sponsor changes a constraint, then 10 minutes of defence

Data Science Track · 3 teaching days + capstone day · 8 min talk and demo · 10 min Q&A · DS-310

#### [capstone#agenda] Frame alone, finish, then present and defend

*Capstone day*

- **Supervised framing check**: three requests framed without AI assistance, on paper or offline
- **Finish and publish**: framing card, plan and ranked review notes, in a public repository by the deadline
- **Present and defend**: the talk, during which the sponsor changes a constraint, then the defence
- **Review and closing**: what the room learned, the follow-up task

#### [capstone#framing-check] The supervised framing check: three requests, 40 minutes, no AI

*20% of the result*

- Three short requests you have not seen, from three managers
- One framing card each: decision, estimand (population, variable, comparison, summary), metric, decision rule, what would change it
- Marked on whether a peer could plan from it without further questions

#### [capstone#the-brief] Hima Municipality: the permits backlog doubled after applications moved online

*The case*

**Fahda Al-Bishr, director of permits:** Should we hire six more plan reviewers? Tell me what to do.

**Daifallah Al-Juaid, head of plan review:** Many online applications arrive without the documents we need, and files go back to applicants, sometimes twice.

- `permits.csv`: 3,600 synthetic applications of one year
- `inventory.json`: what data exist, who holds them, how long they take
- `review/backlog_analysis.py`: an analysis drafted with an assistant, to review

#### [capstone#hand-in] Three files and a README, in a public repository

*The repository*

- **framing_card.md.** The decision, the estimand, the metric, the rule, and the guardrail you watch
- **analysis_plan.md.** At most two pages: data, method, threats, the result that would change the decision, feasibility by the date
- **review_notes.md.** Notes on your variant of the backlog analysis: problem, consequence, fix, ranked by consequence

> **Start from** `labs/capstone/README.md`: copy it to your repository and fill it in. No personal data, and the synthetic data only.

#### [capstone#own-variant] Each participant reviews a variant of the backlog analysis of their own

*Authenticity*

- The repository holds one version, for practice
- The trainer gives you your own variant this morning, with its seeded flaws
- Your review notes are matched against your variant's flaws

- **As in Lab 3.2.** The same pool of kinds of flaw, the same ranking rule: what the flaw does to the decision comes first.

#### [capstone#rubric] Five criteria, 100 points

*The capstone and its defence*

| Item | Value |
| --- | --- |
| Framing card a peer can plan from | 20% |
| Analysis plan, threats and the deciding result | 20% |
| Review notes ranked by consequence | 20% |
| The kind of analysis recommended | 10% |
| Defence under the changed constraint | 30% |

#### [capstone#weights] Three parts make the result; the defence has its own floor

*The result*

| Part | Weight |
| --- | --- |
| Supervised framing check, without AI | 20% |
| Framing card, plan and review notes, on the rubric | 50% |
| Live defence with an unseen change of constraint | 30% |

> **To pass:** 70% overall, and at least 60% on the live defence.

#### [capstone#format] The talk, the changed constraint, the defence

*Eight minutes, then ten*

- **3 min · the question.** The framing card: the decision, the estimand, the rule
- **3 min · the plan.** Method, the main threat, the result that would change the decision
- **2 min · the review.** The top note of your variant and its consequence

> **During the talk** the sponsor changes one constraint. The ten-minute defence starts from it: what changes in your recommendation, and what does not?

#### [capstone#practice-change] A practice constraint change: what happens to your plan?

*Practise it now*

**Fahda Al-Bishr:** The council has frozen hiring for this year. Whatever you recommend must work with the reviewers we have.

- Does the decision still exist? Which options are left?
- Does the kind of analysis change: from a causal question about staff to a description of where time is lost?
- What stays the same in your plan, and why?

#### [capstone#running-order] Who presents when

*Running order*

| # | Participant | Repository |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |

#### [capstone#final-prep] Fifteen minutes: open your repository as a stranger would

*Before the first talk*

Open the public link in a private window. Are the three files there, and could a peer plan from your card alone?

#### [capstone#now-presenting] Talk

*Now presenting*

##### Defence

#### [capstone#review] What the room learned

*After the defences*

- **The best framing.** Which card could the room plan from without a single question?
- **The flaw most missed.** Which seeded flaw went unranked or ranked low most often?
- **The best defence.** Who moved exactly the part of the plan the constraint touched?

#### [capstone#what-next] The follow-up task, and what comes next

*After the course*

- **Follow-up task.** Within four weeks, write one framing card for a real request at work and have a colleague plan from it; keep personal and Restricted data out of anything you share.
- **Keep the repository.** It is evidence for the DS Associate badge.
- **Next.** Metric definition in depth is DS-307; team review standards are DS-407.

#### [capstone#thanks] Thank you

*SDAIA Academy*

Problem Framing and Analytical Review
