---
course: "Problem Framing and Analytical Review"
code: "DS-310"
version: "2027.1.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-310/slides/day1.html"
---

# Problem Framing and Analytical Review

## Day 1: From request to question

A request names a worry; a question names a decision, an estimand and a rule

#### [day1#title] From request to question

*SDAIA Academy · Problem Framing and Analytical Review*

Day 1: A request names a worry; a question names a decision, an estimand and a rule

Data Science Track · 3 teaching days + capstone day · 4 sessions · 4 labs · DS-310

#### [day1#agenda] From request to question

*Today*

- **Session 1 · Requests are not questions**: From a manager's worry to a decision question with an estimand, a metric and a decision rule
- **Session 2 · Question types**: Descriptive, predictive, causal or unanswerable, and the kind of analysis each one needs
- **Session 3 · Interviewing a stakeholder**: Find the constraints, the acceptable evidence and the people affected before any analysis
- **Session 4 · Feasibility and scope**: Test a question against the data, their classification, the time to get them and the deadline

#### [day1#ghadeer-case] Ghadeer Water Company has six districts and many vague requests

*The case for three days*

- **2,400 accounts**, 24 months of bills, district bulk meters, leak repairs and a contact-centre log
- Managers ask about **water loss**, estimated bills, repeat complaints, loggers and smart meters
- Every number has a story of how it was made: **meters, billing cycles, repair jobs**
- All data is synthetic, from a fixed seed

- **Nadia Al-Rubaie.** Director of non-revenue water and customer operations: the sponsor
- **Sultana Al-Kanaan · Mamdouh Al-Qarawi.** Customer service manager and metering engineer, role-played in Labs 1.3 and 2.1
- **You: Ghala Al-Muwallad.** Senior analyst who frames, plans and reviews

#### [day1#setup-check] One notebook proves your setup

*Before the first lab*

- **Colab:** open `00_setup_check` from the course page; it clones the repository
- **Laptop:** from `labs/`, run `uv sync`, then `uv run jupyter lab`
- Nothing downloads a model; everything runs on a laptop processor
- A free hosted model key is optional: without it, tutor and assistant cells use a stand-in and say so

```text
# file: 00_setup_check
missing libraries: none
reads.csv: 57,600 bills, 2,400 accounts, 6 districts
hosted model: none; labs use stand-ins
setup complete
```

### Session 1: Requests are not questions

#### [day1#s1] Requests are not questions

*Session 1*

- Separate the decision behind a request from the topic it names
- State an estimand with population, variable, contrast and summary
- Write a decision rule a peer can apply without asking you

#### [day1#worry-not-question] A request names a worry; a question names a decision

*The request*

**Mamdouh, request R4:** The acoustic-logger pilot in Al-Wurud found lots of leaks. Should we buy loggers for more districts?

**Analyst, first reflex (weak example):** I will count the leaks the loggers found and compare districts.

**Analyst, framed (good example):** Should Ghadeer buy loggers for Al-Rawdah and Al-Hamra next year? Buy if detection cut non-revenue water by at least 3 points in Al-Wurud, relative to the other districts.

#### [day1#five-requests] Five requests, five missing decisions

*The given*

| Request | From | What is missing |
| --- | --- | --- |
| R1 "Water loss in Al-Rawdah is out of control" | Nadia | The choice the board faces |
| R2 "Look into the estimated bills" | Khalil | A threshold for acting |
| R3 "Find out what is going on" with repeats | Sultana | Everything but the topic |
| R4 "Should we buy loggers for more districts?" | Mamdouh | The outcome: water, not leaks found |
| R5 "Do the smart meters work?" | Nadia | Work at what: saving water or measuring it? |

#### [day1#decision-first] The decision comes first: who chooses, between what

*Before the data*

- **Decision maker.** A person with the authority and the budget: Nadia, with the capital committee
- **The decision.** A question that ends in a choice: "Should ...?", "Which ...?"
- **Options.** At least two, and "do nothing" among them: every option is judged against it

> **Recap.** DS-308 Day 1 frames a decision for a memo; DS-204 Day 1 frames a prediction for a decision. Here the frame goes further: an estimand and a rule.

#### [day1#estimand-parts] An estimand states exactly which number answers the question

*The estimand*

| Part | Question it answers | R4, framed |
| --- | --- | --- |
| **Population** | Which units, which period? | District-months of six districts, months 1 to 24 |
| **Variable** | What is measured on each unit? | Non-revenue water, % of system input |
| **Contrast** | With what, against what? | Al-Wurud with detection against five districts without |
| **Intercurrent events** | What happens on the way that changes the meaning? | The bulk meter was recalibrated in month 13 |
| **Summary** | Which one number? | Difference in differences, in points |

#### [day1#leaks-found-trap] Leaks found is an activity; water lost is the outcome

*The variable*

| Item | Value |
| --- | --- |
| Al-Rawdah | 39.3% |
| Al-Wurud | 28.0% |
| Al-Hamra | 27.7% |
| Al-Shifa | 26.9% |
| Al-Salam | 22.3% |
| Al-Nakheel | 16.5% |

- Non-revenue water, months 13 to 24, from Lab 1.1
- Active detection **finds more leaks by design**: a rise in leaks found says the crews searched
- The company pays for water lost, so the variable is **non-revenue water**

#### [day1#decision-rule] A decision rule names the number at which the choice changes

*The rule*

- **Not a rule.** "Buy loggers if detection works well."
  "Act if many bills are estimated."
- **A rule.** "Buy for a district if detection cut non-revenue water by at least 3 points and the district is above 25%."
  "Book second visits if more than 10% of Al-Hamra bills are estimated."

> **Why write it now.** A threshold set after the result is seen bends to the result. Al-Hamra's share is 16.4% (Lab 1.1): the rule was set before anyone looked.

#### [day1#affected-and-personal-data] Every card says who is affected and whether personal data are needed at all

*Responsible framing*

- **Affected:** customers facing interruptions, readers, crews, the budget that funds something else
- **Personal data:** a district total answers R4; names, mobiles and national IDs do not help
- Decide it on the card, before the data request is written

- **The rule behind it.** The Personal Data Protection Law limits collected personal data to the minimum the purpose needs; its implementing regulation asks for a map linking each item to a purpose.

#### [day1#peer-test] A card is done when a peer can plan from it without asking you

*The test of a card*

```python
# file: Lab 1.1
U.card_gaps({"decision": "Look into the estimated bills",
             "decision_rule": "Act if the share is high"})
# What is the decision maker?  What are the options?
# Is the decision written as a question that ends in a choice?
# Estimand: what is the population? ... the summary?
# Decision rule: at what number does the choice change?
# What does 'high' mean here, in a number?
```

#### [day1#check-framing] Which gap matters most in this card?

*Checkpoint*

**Question:** Khalil's card reads: "Measure how accurate Al-Hamra's bills were in 2026, using all billing data, and report the results to management." What should be added first?

- A. A longer period, so the estimate is more precise
- B. The decision it informs and the number at which that decision changes
- C. A chart template for the management report
- D. A model of which bills will be inaccurate next year

#### [day1#lab-1-1] Two framing cards (AI-off)

Lab 1.1 · 25 min

Reframe two vague requests as decision questions with an estimand (AI-off): two framing cards that a peer can plan from without further questions.

[D1_1_reframe_two_vague.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D1_1_reframe_two_vague.ipynb)

- [ ] Read the two requests and the baseline numbers (4 min)
- [ ] Card 1: decision maker, decision and options (6 min)
- [ ] Card 1: estimand and decision rule (6 min)
- [ ] Card 2: the same, faster (6 min)
- [ ] Peer test: what a planner would still ask (3 min)
- [ ] ✱ Stretch: Frame a third request and swap it with a neighbour

### Session 2: Question types

#### [day1#s2] Question types

*Session 2*

- Classify a request as descriptive, predictive, causal or unanswerable
- Match each type to description, an experiment, a causal analysis, a model or no analysis
- Change the recommendation when a constraint changes

#### [day1#four-labels] Each kind of question needs a different kind of analysis

*Four labels*

| Label | The request asks | It needs |
| --- | --- | --- |
| **Descriptive** | What happened, how much, where | A description |
| **Predictive** | What will happen to each unit | A predictive model |
| **Causal** | What a change did, or would do | An experiment if one can still run; otherwise a causal analysis of existing data |
| **Unanswerable** | Something the data cannot reach, or no decision | No analysis yet: reframe or collect |

#### [day1#mistaken-type] Most analysis errors start by mistaking the type of question

*The commonest error*

- Leek and Peng list six types: descriptive, exploratory, inferential, predictive, causal, mechanistic
- They call mistaking the type the most common error in data analysis

| Real type | Taken for | The error has a name |
| --- | --- | --- |
| Inferential | Causal | Correlation read as causation |
| Exploratory | Inferential | Data dredging |
| Exploratory | Predictive | Overfitting |
| Descriptive | Inferential | An "n of 1" analysis |

#### [day1#which-misleads] "Which" can open a description or a prediction

*Words mislead*

- **C1 · descriptive.** "How many leak repairs did each district have last quarter?" A count of the past.
- **C2 · predictive.** "Which accounts are likely to get an estimated bill next month?" A forecast per account.
- **C5 · predictive.** "Which mains are most likely to burst next summer?" A forecast per main.

> **Ask two things.** Past or future? The whole group, or each unit?

#### [day1#experiment-or-not] An experiment only when the change can still be assigned at random

*Causal questions*

1. **C4 · text before the reader's visit** Not done yet: randomise accounts, an experiment
2. **C8 · smart meters in one district** Done, one district: causal analysis against similar districts
3. **C3 · target in every team at once** Done, everywhere: causal analysis of existing data, weakest

> **Recap.** Designing and sizing the experiment is DS-205; here you decide whether one is possible.

#### [day1#unanswerable] "Unanswerable" is an answer, if it comes with a better question

*The fourth label*

- **C6 as asked.** "Why do customers distrust us?" No decision, and no data on trust.
- **C6 reframed.** "Which contact reasons are followed by a repeat contact within seven days most often, so we fix the top two first?"

- Say what data would make it answerable, and what decision it would serve
- Do not produce a chart that pretends to answer the original

#### [day1#constraint-changes] When a constraint changes, the recommendation changes with it

*The meeting moves*

**Nadia:** The text-message budget is frozen until next year, and the board wants a decision on meter reading in ten business days. No new trial can run before then.

**Analyst (good example):** Then C4 gets no analysis now: decide the reading schedule on cost and practicality, and run the reminder experiment when the budget returns.

> **In the capstone.** The sponsor changes one constraint during your talk. You revise out loud.

#### [day1#process-models] CRISP-DM starts with the business; it does not frame the question for you

*Process models*

1. **Business understanding** the only phase about the decision
2. **Data understanding, preparation, modeling, evaluation, deployment** five phases about the data and the model

- The model is a cycle of **six phases**: useful as a checklist of stages
- It assumes a model will be built: no place for "description is enough" or "no analysis"
- It says little about stakeholders, estimands or when to stop

#### [day1#check-question-type] What does this request need?

*Checkpoint*

**Question:** In month 13 Ghadeer moved meter reading in all six districts to a new contractor. Khalil asks: "Did the new contractor cut the number of estimated bills?" The decision is whether to renew the contract.

- A. A description of estimated bills by month
- B. An experiment that randomises districts
- C. A causal analysis of existing data, stating its weaknesses
- D. A predictive model of estimated bills

#### [day1#lab-1-2] Eight requests classified

Lab 1.2 · 25 min

Classify eight requests as descriptive, predictive, causal or unanswerable, name the analysis each needs, and revise when the sponsor changes a constraint.

[D1_2_classify_eight_requests.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D1_2_classify_eight_requests.ipynb)

- [ ] Read the four labels and the eight requests (3 min)
- [ ] Classify each request (8 min)
- [ ] Name the analysis each one needs (6 min)
- [ ] The sponsor changes a constraint: revise (5 min)
- [ ] Compare with the key and explain one disagreement (3 min)
- [ ] ✱ Stretch: Rewrite the unanswerable request so that data could answer it

### Session 3: Interviewing a stakeholder

#### [day1#s3] Interviewing a stakeholder

*Session 3*

- Map decision makers, users and affected groups for a request
- Ask open questions that surface constraints and acceptable evidence
- Record what was said apart from what was assumed

#### [day1#three-groups] Map who decides, who uses the answer and who is affected

*Who to talk to*

- **Decide.** Sultana, with Nadia for the call-centre contract
- **Use.** Team leaders; the outsourced call-centre supplier
- **Affected.** Customers who call again; agents whose bonus rides on a target; older customers with estimated bills

> **What goes wrong.** Only the decider is interviewed, and the affected groups appear for the first time in a complaint.

#### [day1#open-questions] Open questions find constraints; closed and leading ones find agreement

*How you ask*

**Leading:** Don't you think it's the agents?

**Sultana (weak example):** Yes, I suppose so.

**Open:** How do you count a repeat contact today: how do you know it is the same customer?

**Sultana (good example):** The system links contacts by mobile number. When a customer calls from another phone, it is a new customer to us.

#### [day1#six-topics] Six topics cover most of what a stakeholder knows and you do not

*What to ask*

1. **The decision and its date**: what will you do differently, and by when?
2. **How the number is counted**: how do you know it is a repeat, a leak, an estimate?
3. **Acceptable evidence**: what would convince you, and what would you not trust?
4. **Incentives**: which targets do people work under?
5. **What changed**: what moved in the last year?
6. **Rules on data**: what may be used, by whom, where?

#### [day1#hidden-constraints] Five constraints changed the analysis before it started

*What nobody volunteers*

| Heard in the interview | What it changes |
| --- | --- |
| Contract renewal in four weeks | The deadline, and the decision |
| First-contact target in bonuses since month 13 | "Resolved" is no longer a clean measure |
| Contacts linked by mobile number | Repeats from another phone are missed |
| Recordings need the data protection officer | No call audio in a two-week plan |
| Trusts repeats within seven days, not the survey | Which measure the answer uses |

#### [day1#heard-assumed] Write what you heard apart from what you assumed

*The record*

- **Heard.** "We shortened the call script in month 13. Handling time fell a lot."
- **Assumed.** That repeat contacts rose after month 13. Not yet checked in the data.

> **Why it matters.** An assumption written as a fact becomes a finding by Day 3, and nobody remembers it was a guess.

#### [day1#acceptable-evidence] Agree the evidence before you produce it

*Before the analysis*

- Sultana trusts **repeat contacts within seven days**
- She does not trust the **satisfaction survey**: few people answer it
- An analysis built on the survey would be ignored, however good

- **On the framing card.** The variable of the estimand is the evidence the decision maker accepts; if it is not, say why in the card.

#### [day1#role-play-rules] The interview is a role-play; the stand-in is for practice

*The lab*

- **In the room.** The trainer or a neighbour holds Sultana's role card and answers only what is asked. Eight minutes, then swap.
- **Alone.** `U.interview("sultana", q)` answers by topic, gives agreement to a leading question, and counts the constraints you reached.

#### [day1#check-interview] Which question finds out how a repeat is counted?

*Checkpoint*

**Question:** You suspect the repeat-contact rate is undercounted, but you do not know how the system links contacts. Which question do you ask Sultana?

- A. "How does the system decide that two contacts come from the same customer?"
- B. "Is the repeat rate accurate?"
- C. "Surely some repeats are missed, right?"
- D. "Do you trust the repeat-contact figures?"

#### [day1#lab-1-3] Interview the operations manager

Lab 1.3 · 25 min

Interview a role-played operations manager and record constraints and acceptable evidence: an interview record with the constraints found and the questions left.

[D1_3_interview_role_played.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D1_3_interview_role_played.ipynb)

- [ ] Read the request and the stakeholder map (3 min)
- [ ] Write six open questions (6 min)
- [ ] Interview: a role-play or the stand-in (8 min)
- [ ] Record constraints and acceptable evidence (6 min)
- [ ] List what you did not ask (2 min)
- [ ] ✱ Stretch: Interview the data protection officer about the same request

### Session 4: Feasibility and scope

#### [day1#s4] Feasibility and scope

*Session 4*

- Estimate when each dataset in a plan can be ready
- Apply classification, sharing time limits and minimisation to a data request
- Cut a question's scope until it fits the deadline

#### [day1#three-clocks] Three clocks decide whether a question is answerable in time

*Feasibility*

1. **Data ready** access, approval or a sharing request
2. **Analysis** 4 business days for this team
3. **Decision** the board meets in 10 business days

> **What goes wrong.** The data request goes out after the plan is written, and the answer arrives after the decision.

#### [day1#inventory-days] The burst question wants five datasets; two arrive in time

*The given*

| Dataset | Held by | Class | Ready (business days) |
| --- | --- | --- | --- |
| Leak-repair work orders | Ghadeer | Restricted | 1 |
| Daily temperature | Open data | Public | 0 |
| Billing reads | Ghadeer | Restricted | 2 |
| Pipe network | Ghadeer | Secret | 8 |
| Road-works permits | Regional Roads Office | Restricted | 15 |

#### [day1#sharing-timeframe] A sharing request can take three weeks, by policy

*Data held by another entity*

**10 + 5** business days: assess the request, then share once approved

- The NDMO Data Sharing Policy gives the sharing entity up to 10 business days to assess and 5 to share after approval
- It can extend the time for an extraordinary effort
- The request must also respect data minimisation

#### [day1#classification-levels] The classification of a dataset sets where and how fast you can use it

*Classification*

- **Top Secret.** Not in an analysis plan with a two-week deadline
- **Secret.** Pipe network: a security approval, 8 days
- **Restricted.** Billing, repairs, contacts: inside Ghadeer's environment
- **Public.** Open temperature data: no request

> **Hosted assistants.** A Restricted extract does not go to a public assistant; Day 3 reviews an assistant's work on synthetic data only.

#### [day1#minimise-request] Ask for what the purpose needs, not what happens to be ready

*Minimisation*

- **Tempting.** "Billing reads are ready in two days: take them, we might link bursts to customers later."
- **Minimised.** "The burst question needs repairs and temperature. Billing brings names, mobiles and national IDs it does not need."

> **On the card.** Every dataset kept has a reason tied to the question; every personal field dropped has one too.

#### [day1#cut-scope] Cut the question until it fits, and say what the cut leaves out

*Cutting scope*

1. **Asked (causal)** Do road works explain the bursts in Al-Rawdah, and should renewal go to its oldest mains?
2. **Scoped (descriptive)** Have bursts in Al-Rawdah become more frequent over 24 months, and do they follow summer temperatures, enough to justify a renewal study?

Lab 1.4 run: 4.7 repairs a month in year 1, 4.9 in year 2; 4.8 in summer and 4.8 otherwise.

#### [day1#phase-two] A scoped card says what is left unanswered and requests it now

*The cost of the cut*

- **Left unanswered:** whether road works or pipe age cause the bursts
- **Requested today:** road-works permits through a data-sharing request; the pipe network through the security approval
- **Told to the sponsor:** the board gets a description now and a causal answer in about a month

> **What goes wrong.** The scoped answer is presented as the answer to the original question.

#### [day1#check-feasibility] How do you answer this data request?

*Checkpoint*

**Question:** Planning the burst analysis, a colleague asks for the billing extract with national IDs "in case we want to link bursts to customers later". The question is about bursts by month.

- A. Take it: it is ready in two days
- B. Take it, but hash the national IDs
- C. Refuse it: Restricted data cannot be analysed
- D. Leave it out: the burst question needs no personal data; a later purpose gets its own request

#### [day1#lab-1-4] Check and cut one question

Lab 1.4 · 25 min

Check one question against the data inventory and the deadline and cut its scope until it is answerable in ten business days.

[D1_4_check_one_question.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D1_4_check_one_question.ipynb)

- [ ] Read the card and the data inventory (3 min)
- [ ] Days until each dataset is ready (7 min)
- [ ] Classification and personal data per dataset (5 min)
- [ ] Cut the scope to fit ten business days (7 min)
- [ ] Write the scoped card (3 min)
- [ ] ✱ Stretch: The sponsor moves the deadline to five business days: cut again

#### [day1#wrap-up] Three things to keep

*Day 1 · wrap-up*

- **Decision first.** A framing card names a choice, an estimand with five parts and the number at which the choice changes.
- **Type before method.** Descriptive, predictive, causal or unanswerable; and "no analysis" is a valid recommendation.
- **Feasible by the date.** Count back from the decision; minimise personal data; say what the cut leaves out.

#### [day1#next] Day 2: Know the domain, plan the work

*Next*

Read the three short files in `labs/data/briefing/` (metering, billing cycles, leak repair). Tomorrow you learn how the numbers are made before you plan with them.
