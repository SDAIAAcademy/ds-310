---
course: "Problem Framing and Analytical Review"
code: "DS-310"
version: "2027.1.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-310/slides/day2.html"
---

# Problem Framing and Analytical Review

## Day 2: Know the domain, plan the work

Learn how the numbers are made before you plan what to do with them

#### [day2#title] Know the domain, plan the work

*SDAIA Academy · Problem Framing and Analytical Review*

Day 2: Learn how the numbers are made before you plan what to do with them

Data Science Track · 3 teaching days + capstone day · 4 sessions · 4 labs · DS-310

#### [day2#agenda] Know the domain, plan the work

*Today*

- **Session 1 · How the data are made**: Meter reads become bills through estimates, billing cycles and meter swaps, and each step can mislead
- **Session 2 · Metrics and proxies**: A metric tree is a set of proxies; under a target, each one can be gamed
- **Session 3 · Analysis plans**: Data, method, threats and the result that would change the decision, fixed before outcomes are seen
- **Session 4 · Threats to validity**: What could make the answer wrong: selection, regression to the mean, measurement change and more

#### [day2#review-day1] Which card is ready to plan from?

*Review of Day 1*

**Question:** Four drafts for Mamdouh's logger request. Which one could a peer plan from without asking anything?

- A. "Should Ghadeer buy loggers for Al-Rawdah next year? Buy if detection cut non-revenue water by 3 points or more in Al-Wurud against the other districts."
- B. "Analyse how many leaks the loggers found in Al-Wurud."
- C. "Should Ghadeer buy loggers if detection works?"
- D. "Build a model of leak risk by district."

### Session 1: How the data are made

#### [day2#s1] How the data are made

*Session 1*

- Read a briefing pack and an expert interview for how a metric is produced
- Draw the meter-to-bill process as a diagram
- Mark where the data can mislead, with a number from the data

#### [day2#water-balance] Non-revenue water mixes water that leaked with water that was not billed

*The domain*

1. **System input** what the bulk meters measure
2. **Billed consumption** what the bills say
3. **Non-revenue water** the difference

- **Real losses.** Leaks, bursts and overflows up to the customer meter
- **Apparent losses.** Meter inaccuracy, billing data errors, unauthorised use: water delivered but not billed

#### [day2#meter-to-bill] Seven steps turn water at a meter into a percentage in a report

*The process*

1. Water passes the customer meter
2. A reader visits on a route, every 27 to 35 days
3. A read is taken, or the bill is estimated from the last three reads
4. A bill is issued for the period ending this month
5. Bills are summed by district and month
6. The bulk meter gives district input for the calendar month
7. Non-revenue water is input minus billed

#### [day2#estimated-bills] Al-Hamra estimates one bill in six, and estimates miss the summer

*Step 3*

| Item | Value |
| --- | --- |
| Al-Hamra | 16.4% |
| Al-Rawdah | 4.3% |
| Al-Salam | 3.2% |
| Al-Shifa | 2.9% |
| Al-Wurud | 2.4% |
| Al-Nakheel | 2.3% |

- An estimate is the **average of the last three actual reads**
- It does not follow the summer rise, so summer bills come in low
- The next actual read catches up: the error **moves between months**

#### [day2#billing-cycles] A "monthly" bill covers 27 to 35 days, and that alone moves the percentage

*Step 2*

**4.29 → 0.85** standard deviation of monthly non-revenue water in Al-Salam, months 1 to 12, in points: raw, then bills rescaled to 30 days

- The bulk meter measures a calendar month; the bill measures a reading period
- A 35-day bill in a 30-day month makes the district look tight
- Rescaling each bill to 30 days removes about four fifths of the swing

#### [day2#smart-meter-step] Smart meters raised Al-Nakheel's bills by measuring, not by use

*Step 1*

| Billed per account per 30 days, year 2 against year 1 | Change |
| --- | --- |
| Al-Nakheel, smart meters from month 13 | +12.1% |
| The other five districts | -1.6% |

- Old mechanical meters miss about **1.5% more each year**
- New meters bill water the old ones missed: **apparent losses** fall
- This is why Al-Nakheel had the lowest non-revenue water on Day 1

#### [day2#ask-the-engineer] The engineer knows what the documents leave out

*The expert interview*

**You:** How is the district input measured, and has anything changed with those meters?

**Mamdouh (good example):** The Al-Wurud bulk meter was over-reading for a few months. It was recalibrated in month 13.

**You:** When is a repair job closed?

**Mamdouh (good example):** Since the three-day target, crews close the job when they leave the site. If the leak comes back, it is reopened.

#### [day2#map-with-marks] A process map is done when it marks where the data mislead, with a number

*The deliverable*

```text
# file: out/meter_to_bill.mmd
flowchart LR
  S1["1. Water passes the customer meter"] --> S2["2. Reader visits ..."]
  S2 --> S3["3. Read taken, or estimate ..."]
  M3(["⚠ Estimates: 16.4% of Al-Hamra bills"]) -.- S3
  M2(["⚠ Cycle 27 to 35 days: sd 4.29 raw, 0.85 rescaled"]) -.- S2
  M1(["⚠ Smart meters: billed +12.1% against -1.6%"]) -.- S1
```

Mermaid text renders in a Mermaid viewer or in draw.io; the lab writes it for you.

#### [day2#check-data-made] What does the rise in recorded leaks show?

*Checkpoint*

**Question:** From month 13, Al-Wurud's crews search for leaks with acoustic loggers. Recorded leaks in Al-Wurud triple. A manager says "the network there is getting worse".

- A. The network in Al-Wurud is deteriorating
- B. The loggers have already cut water loss threefold
- C. The repair records are unreliable and should be ignored
- D. The crews are searching; whether less water is lost must be read from non-revenue water

#### [day2#lab-2-1] The meter-to-bill map

Lab 2.1 · 25 min

Map the meter-to-bill process and mark where the data can mislead: a Mermaid process map with three marked points, each with its number from the data.

[D2_1_map_meter_bill.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D2_1_map_meter_bill.ipynb)

- [ ] Read the briefing pack (5 min)
- [ ] Ask the metering engineer three questions (5 min)
- [ ] The process as a Mermaid map (5 min)
- [ ] Three points where the data mislead, with numbers (8 min)
- [ ] Save the map (2 min)
- [ ] ✱ Stretch: Add a fourth mark on the leak-repair work order

### Session 2: Metrics and proxies

#### [day2#s2] Metrics and proxies

*Session 2*

- Trace a goal to the proxies a metric tree uses for it
- Recognise the four ways a proxy fails under pressure
- Propose guardrail metrics that expose the gaming

#### [day2#metric-tree] Ghadeer's metric tree runs from a goal to leaves people can move

*The given*

1. **Goal** Little loss, good service
2. **Outcomes** Non-revenue water · customer service
3. **Leaves** Repair time · leaks found · estimated share · first-contact resolution · handling minutes

- From month 13, two leaves became **targets**: repair time of 3 days or less; first-contact resolution of 85% or more
- A leaf is a **proxy**: it stands for the goal while nobody pushes on it

#### [day2#goodhart-four] A proxy fails under pressure in four ways

*Goodhart's law*

- **Regressional.** Selecting on a noisy proxy also selects the noise
- **Extremal.** Pushed into a range where the old relation no longer holds
- **Causal.** The action taken on the proxy breaks its link to the goal
- **Adversarial.** People with other goals game the measure

> **The original law.** An observed regularity tends to collapse once pressure is placed on it for control.

#### [day2#repair-time-gamed] Repair time halved; the customer's wait did not

*The first target*

| Repair jobs | Months 1 to 12 | Months 13 to 24 |
| --- | --- | --- |
| Median days, job created to job closed (the target) | 4 | 2 |
| Jobs reopened after closure | 5.6% | 25.7% |
| Mean days, customer report to job created | 0.25 | 1.81 |
| Mean days, customer report to final fix | 4.85 | 5.17 |

#### [day2#fcr-gamed] More calls were marked resolved, and more customers called again

*The second target*

- **73.5 → 85.9%** contacts marked resolved
- **22.7 → 26.6%** contacts followed by another within 7 days
- **7.7 → 6.6** average handling minutes

> **Two changes in one month.** The target and a shorter call script both started in month 13 (Lab 1.3): the repeat rise has two candidate causes.

#### [day2#guardrails] A guardrail is a second metric that worsens when the first is gamed

*Guardrails*

| Guardrail | Guards | Behaviour it exposes | Before → after |
| --- | --- | --- | --- |
| Jobs reopened after closure | Repair time | Closing before the leak is fixed | 5.6 → 25.7% |
| Contacts followed by another within 7 days | First-contact resolution | Marking a call resolved when the customer must call again | 22.7 → 26.6% |

#### [day2#good-guardrail] A good guardrail is hard to game in the same move

*Design*

- **Opposite direction.** It worsens when the target is gamed: reopenings rise when jobs close early
- **Different owner.** Someone other than the people under the target produces it: the customer's next call
- **Closer to the goal.** It measures what the customer or the network lives with: report to final fix

> **Pointer.** Writing the definition of each metric (grain, filters, owner) is DS-307, Day 1.

#### [day2#tree-annotated] The annotated tree shows each failure and its guardrail on one page

*The deliverable*

```text
# file: out/metric_tree_annotated.mmd
flowchart TD
  nrw --> repair_time["Median days, job created to closed
     ⚠ adversarial: closed at first visit, jobs created later"]
  nrw --> leaks_found["Leaks found per month
     ⚠ causal: searching harder raises the count"]
  service --> fcr["First-contact resolution
     ⚠ adversarial: marked resolved for the bonus"]
  GR1{{"Guardrail: jobs reopened, %"}} -.- repair_time
  GR2{{"Guardrail: repeat within 7 days, %"}} -.- fcr
```

#### [day2#check-proxies] Which guardrail fits this target?

*Checkpoint*

**Question:** Ghadeer sets readers a new target: 98% of meters read on the scheduled day. Which guardrail best exposes gaming of it?

- A. Number of reader visits per day
- B. Size of the correction at the next actual read, by reader
- C. Share of meters read on the scheduled day, by district
- D. Readers' own notes on access problems

#### [day2#lab-2-2] Stress-test the metric tree

Lab 2.2 · 25 min

Stress-test the water-loss and customer-service metric tree for gaming, label each failure, and add two guardrails with the behaviour each prevents.

[D2_2_stress_test_water.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D2_2_stress_test_water.ipynb)

- [ ] Read the tree and the date the targets started (3 min)
- [ ] Repair time before and after the target (6 min)
- [ ] First-contact resolution and repeat contacts (6 min)
- [ ] Label each gamed metric with its mechanism (4 min)
- [ ] Two guardrails and the behaviour each prevents (6 min)
- [ ] ✱ Stretch: A guardrail for estimated reads inside non-revenue water

### Session 3: Analysis plans

#### [day2#s3] Analysis plans

*Session 3*

- Write an analysis plan with data, method and threats to validity
- Compute what change the available data can detect
- State in advance the result that would change the decision

#### [day2#plan-sections] Seven sections, two pages, written before any result

*An analysis plan*

1. **Question**: the framed decision
2. **Data**: datasets, fields, grain, when ready
3. **Method**: with its comparison
4. **Detectable change**: can the data see the effect?

5. **Threats**: at least three, each with its answer
6. **The result that changes the decision**, in numbers
7. **Timeline**: in business days, back from the decision

#### [day2#fixed-before] Choices made after seeing the data bend the answer, even without fishing

*Why before*

- Which months, which districts, raw or rescaled, mean or median: each choice is a fork
- Made after looking, each fork drifts toward the result someone hoped for
- Gelman and Loken: a multiple-comparisons problem arises even with **one analysis and no conscious fishing**

- **In Lab 2.3.** You do not compute the effect of detection. You write the method, the threshold and the exclusions first.

> **Recap.** DS-205 pre-registers an experiment; here the same discipline covers any analysis.

#### [day2#plan-data-grain] Ask for the grain the method needs, not the rows the system holds

*Data*

| Dataset | What the plan asks for | Ready |
| --- | --- | --- |
| Bulk supply | Input by district and month | 1 day |
| Billing reads | Billed m3 and billing days as district-month totals: no names, mobiles or national IDs | 2 days |
| Pipe network, road works | Not needed for this question | 8 and 15 days |

#### [day2#plan-method] Compare Al-Wurud with the other districts, and skip the months that mix effects

*Method*

1. **Before: months 1 to 9** Al-Wurud and five districts
2. **Months 10 to 14 left out** meter drift, recalibration, detection starting
3. **After: months 15 to 24** the same districts

Difference in differences: Al-Wurud's change minus the other districts' change, bills rescaled to 30 days.

#### [day2#detectable-change] With raw bills the plan cannot see the 3 points it needs

*Detectable change*

| Item | Value |
| --- | --- |
| Raw bills | 6.45 points |
| Rescaled to 30 days | 1.27 points |
| The decision rule | 3 points |

- Smallest change 9 months before and 10 after can detect: about 2.8 standard errors
- Noise from the five comparison districts in year 1
- Knowing this **before** the analysis changes the method

#### [day2#would-change] Write the result that would change the decision, in numbers

*The deciding result*

- **Vague.** "If detection shows a meaningful effect, consider extending it."
- **Deciding.** "Below 3 points, or an interval that reaches 0: do not buy. 3 points or more: buy for Al-Rawdah (39.3%) and consider Al-Hamra."

#### [day2#plan-rubric] A rule check catches missing parts; a reader judges the rest

*Scoring*

```python
# file: Lab 2.3
U.score_plan(plan)
{'complete': 2, 'data_feasible': 2, 'method_has_comparison': 2,
 'threats': 2, 'would_change_numeric': 2, 'fits_two_pages': 2,
 'total': 12, 'max': 12}
```

> **Necessary, not sufficient.** A plan can score 12 and pick the wrong comparison. The peer swap of Session 4 is the second check.

#### [day2#check-plans] What is wrong with this plan?

*Checkpoint*

**Question:** An analyst computes non-revenue water for all six districts, sees which districts moved like Al-Wurud before month 13, and then writes into the plan that those two are the comparison.

- A. Two comparison districts are too few
- B. Pre-period data should never be looked at
- C. The comparison was chosen after seeing the data, so it can bend toward a hoped-for result
- D. It should say "difference in differences" explicitly

#### [day2#lab-2-3] A plan for a framed question

Lab 2.3 · 25 min

Write a plan for a framed question, including the result that would change the decision, and score it against the rubric.

[D2_3_write_plan_framed.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D2_3_write_plan_framed.ipynb)

- [ ] Read the card, the inventory and the deadline (3 min)
- [ ] Data and method (7 min)
- [ ] What change the data can detect (5 min)
- [ ] Threats and the result that changes the decision (7 min)
- [ ] Score the plan against the rubric (3 min)
- [ ] ✱ Stretch: Plan B, if the meter data arrive a week late

### Session 4: Threats to validity

#### [day2#s4] Threats to validity

*Session 4*

- Name the main threats to the validity of a plan
- Show regression to the mean in data chosen for being extreme
- Rank threats by how much they could change the decision

#### [day2#threat-catalogue] Ten questions that could make the answer wrong

*Ten threats*

| Threat | The question | Threat | The question |
| --- | --- | --- | --- |
| Selection | Chosen in a way linked to the outcome? | Construct | Does the metric still mean what it meant? |
| Regression to the mean | Picked because it was extreme? | Missing or merged | Are events lost or merged? |
| History | Did something else change at once? | Spillover | Does one unit affect the others? |
| Measurement change | Did the way of measuring change? | Forking paths | Choices made after seeing the data? |
| Seasonality | Do the periods differ by season? | Small sample | Too few units to see the signal? |

#### [day2#regression-to-mean] The district picked for its worst month improves next month on its own

*In the data*

- **-3.42** points: next-month change of the district with the highest non-revenue water, months 1 to 12
- **+0.33** points: next-month change of all districts in the same months

> **Plan A.** Al-Wurud was chosen because it was highest in month 12. Part of its fall would have happened with no detection at all.

#### [day2#measurement-change] Plan A's "before" months were inflated by a meter fault

*Measurement change*

| Non-revenue water, bills rescaled to 30 days | Al-Wurud | Other districts |
| --- | --- | --- |
| Months 1 to 9 | 31.5% | 29.0% |
| Months 10 to 12 (bulk meter over-reading) | 36.2% | 29.1% |
| Months 13 to 15 | 32.1% | 27.4% |

#### [day2#history-month-13] Month 13 changed five things at once

*History*

- Active detection in Al-Wurud
- Bulk-meter recalibration in Al-Wurud
- Smart meters in Al-Nakheel
- Repair-time and first-contact targets everywhere
- A shorter call script in the contact centre

- **What a comparison answers.** Changes shared by every district cancel out. Changes in one district, such as Al-Nakheel's meters, distort the comparison: run it with and without that district.

#### [day2#construct-threat] Plan B measures the target with the metric the target corrupted

*Construct*

- **Plan B.** "First-contact resolution rose by 12 points: keep the target." The flag is set by the agents whose bonus depends on it.
- **Better.** Judge the target by repeat contacts within seven days, which the customer produces, and state that mobile-number linking undercounts them.

#### [day2#rank-threats] List three threats, ordered by how much each could change the decision

*Ranking*

1. **Could reverse the decision**: the estimate may be mostly artefact (regression to the mean, measurement change)
2. **Could move it across the threshold**: a bias of a few points near the 3-point rule (history)
3. **Adds noise only**: mention it, do not lead with it (small sample, when the detectable change is small)

> **Tomorrow.** Review notes are ranked the same way: by consequence, not by the order you found them.

#### [day2#peer-swap] Give a peer three threats, most dangerous first, with one sentence each

*The swap*

**Reviewer:** 1. Measurement change: you use months 10 to 12 as "before", and the bulk meter over-read then. 2. History: Al-Nakheel's smart meters change one comparison district. 3. Seasonality: the periods hold different months.

**Author (good example):** Agreed on 1 and 2. On 3: both periods compare against districts measured in the same months, so seasonality cancels.

#### [day2#check-threats] What is the main threat to this plan?

*Checkpoint*

**Question:** A plan compares Al-Nakheel's non-revenue water, bills rescaled to 30 days, in year 1 (27.7%) and year 2 (19.0%), after the smart meters, and concludes that the meters cut leakage.

- A. Measurement change: the new meters bill water the old ones missed
- B. Small sample: twelve months each side are too few
- C. Regression to the mean: Al-Nakheel was picked for a bad month
- D. Seasonality: summer months differ

#### [day2#lab-2-4] Three threats each

Lab 2.4 · 25 min

Swap plans with a peer and list each other's three main threats, after doing the same for two supplied plans.

[D2_4_swap_plans_peer.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D2_4_swap_plans_peer.ipynb)

- [ ] Read the threat catalogue (3 min)
- [ ] Plan A: its three main threats (7 min)
- [ ] Regression to the mean in the data (5 min)
- [ ] Plan B: its three main threats (5 min)
- [ ] Swap with your neighbour and list theirs (5 min)
- [ ] ✱ Stretch: Rewrite one plan so that its worst threat is answered

#### [day2#wrap-up] Three things to keep

*Day 2 · wrap-up*

- **Know how it is made.** Estimates, billing cycles and meter swaps move non-revenue water without a drop saved.
- **Targets bend proxies.** Pair every target with a guardrail that worsens when it is gamed.
- **Plan, then look.** Method, exclusions, detectable change and the deciding result are fixed before the outcome.

#### [day2#next] Day 3: Review others' work

*Next*

Tomorrow you review three analyses of Sabah's and one by the assistant Sareea. Bring your threat list from Lab 2.4: it is the start of a review checklist.
