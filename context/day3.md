---
course: "Problem Framing and Analytical Review"
code: "DS-310"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-310/slides/day3.html"
---

# Problem Framing and Analytical Review

## Day 3: Review others' work

Review the question, the data, the method, the inference and the words, then rank by consequence

#### [day3#title] Review others' work

*SDAIA Academy · Problem Framing and Analytical Review*

Day 3: Review the question, the data, the method, the inference and the words, then rank by consequence

Data Science Track · 3 teaching days + capstone day · 4 sessions · 4 labs · DS-310

#### [day3#agenda] Review others' work

*Today*

- **Session 1 · A review checklist**: Rerun first, then check five areas from question to conclusion
- **Session 2 · Finding the flaws that matter**: Rank flaws by what they do to the decision, not by how easy they were to find
- **Session 3 · Reviewing assistant-generated analysis**: An assistant's analysis looks finished; rerun it and verify every number before anyone uses it
- **Session 4 · Review notes people act on**: Each note states the problem, its consequence and a fix; the note that matters most comes first

#### [day3#review-day2] Which plan is protected against yesterday's main threats?

*Review of Day 2*

**Question:** Three plans for the logger decision. Which one answers the bulk-meter drift and the month-13 changes?

- A. Al-Wurud months 10 to 12 against 13 to 15
- B. Al-Wurud year 1 against year 2
- C. Leaks found in Al-Wurud, year 1 against year 2
- D. Al-Wurud against the other districts, months 1 to 9 against 15 to 24, without Al-Nakheel

### Session 1: A review checklist

#### [day3#s1] A review checklist

*Session 1*

- Rerun an analysis before judging it
- Apply a checklist of five areas from question fit to communication
- Score an analysis so another reviewer would score it alike

#### [day3#rerun-first] A review starts by running the analysis, not by reading it

*The first step*

1. **Rerun** does it run, from the supplied data?
2. **Reconcile** does every sentence match the output above it?
3. **Check five areas** from question to communication

> **What goes wrong.** The reviewer reads a fluent text, agrees, and never sees that the code prints something else.

#### [day3#five-areas] Five areas, from the question to the words, scored 0 to 2

*The checklist*

| Area | 2 | 1 | 0 |
| --- | --- | --- | --- |
| **Question fit** | Answers the decision asked | A nearby question | Another question |
| **Data handling** | Right rows and denominators, checked | One unchecked step | A step that changes the answer |
| **Method** | Fits the question type, with a comparison | Fits, but weak | Does not fit |
| **Inference** | Claims match evidence, uncertainty stated | Some overreach | Claims what the data cannot show |
| **Communication** | The reader acts correctly | Misleading in part | Misleads |

#### [day3#short-notebook] The sentence was not written from the output

*The rerun catches it*

```text
# file: cell 2 output
district
D5    707
D4    705
D3    699
D6    684
D1    668
D2    635
```

- **Cell 3 prints.** "Al-Hamra (D4) has the most contacts, so it is where service is worst. Move two agents to the Al-Hamra queue."
- **The output says.** Al-Salam (D5) has the most contacts, 707 against 705: and a count of contacts is not a measure of service anyway.

#### [day3#service-measure] A measure of service ranks the districts differently

*Method*

| Item | Value |
| --- | --- |
| Al-Rawdah | 28.0% |
| Al-Shifa | 27.2% |
| Al-Salam | 26.6% |
| Al-Hamra | 26.4% |
| Al-Wurud | 26.0% |
| Al-Nakheel | 25.3% |

- Contacts followed by another within 7 days, months 13 to 24
- The districts sit within three points of each other: no district stands out
- A reviewer may run one check of their own; they do not redo the analysis

#### [day3#score-sheet] Two points out of ten, each with its sentence

*The score*

| Area | Score | Why |
| --- | --- | --- |
| Question fit | 1 | Answers "most contacts", not "worst service" |
| Data handling | 1 | Raw counts; Al-Hamra's access problems drive billing calls |
| Method | 0 | A count of contacts does not measure service |
| Inference | 0 | Volume read as quality; staff moved on it |
| Communication | 0 | Names Al-Hamra; the output shows Al-Salam first |

#### [day3#reviewer-agreement] A checklist is useful when two reviewers land within a point

*Calibration*

- **Anchors.** What a 2, a 1 and a 0 look like, written down before scoring
- **Evidence.** One sentence per score that points at a cell or a number
- **Compare.** Two reviewers score alone, then discuss only the gaps of two points

> **Pointer.** Team review standards (who reviews what, sign-off rules) are DS-407.

#### [day3#check-checklist] Which area does this flaw belong to?

*Checkpoint*

**Question:** An analysis of estimated bills prints "estimated share: 16.4%" for Al-Hamra. The summary below says "about one bill in four is estimated in Al-Hamra".

- A. Data handling
- B. Communication: the words misstate the output
- C. Method
- D. Inference

#### [day3#lab-3-1] Score a short notebook

Lab 3.1 · 25 min

Apply the checklist to a short notebook and score it in five areas, then compare with the reference score.

[D3_1_apply_checklist_short.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D3_1_apply_checklist_short.ipynb)

- [ ] Rerun the short notebook (5 min)
- [ ] Score question fit and data handling (6 min)
- [ ] Score method and inference (6 min)
- [ ] Score communication and the total (4 min)
- [ ] Compare with the reference score (4 min)
- [ ] ✱ Stretch: Name the one change that would raise the score most

### Session 2: Finding the flaws that matter

#### [day3#s2] Finding the flaws that matter

*Session 2*

- Locate seeded flaws cell by cell
- Measure each flaw's consequence with a recomputed number
- Rank flaws by their effect on the decision

#### [day3#seven-kinds] Seven kinds of flaw, four in each variant

*The pool*

|  | Kind of flaw | Area |
| --- | --- | --- |
| F1 | Success measured by an activity, not the outcome | Question fit |
| F2 | A join on a text key silently drops rows | Data handling |
| F3 | Before-after in one unit, no comparison, months that mix changes | Method |
| F4 | Significance or certainty claimed with no interval | Inference |
| F5 | Volumes not adjusted for the billing period | Data handling |
| F6 | A chart axis that does not start at zero | Communication |
| F7 | Estimated bills dropped from billed volume | Data handling |

#### [day3#consequence-defined] The consequence of a flaw is what it does to the answer, measured

*Consequence*

1. **The analysis with no flaw** the reference answer
2. **The analysis with only this flaw** the flawed answer
3. **The difference** points moved, and does the decision flip?

```python
# file: Lab 3.2
U.consequence(MY_NUMBER, "F3")
# clean 2.34 → flawed 4.12 points; decision: do not buy → buy
```

#### [day3#variant-zero] Two of four flaws reverse the recommendation; two change nothing

*Variant 0*

| Flaw alone | Effect, points | Decision |
| --- | --- | --- |
| F1 · success measured as leaks found (rose 3.4 times) | none | buy |
| F3 · months 10 to 12 against 13 to 15, Al-Wurud only | 4.12 | buy |
| F2 · join drops rows spelt "Al Wurud" | 2.34 | do not buy |
| F6 · chart axis from 20% | 2.34 | do not buy |

#### [day3#clean-answer] Without the flaws, detection cut non-revenue water by 2.3 points: do not buy

*The answer*

**2.3** points, 95% interval 1.4 to 3.3, against the other districts without Al-Nakheel

- The plan of Lab 2.3 fixed the rule before: below 3 points, do not buy
- Sabah's notebook said buy, on leaks found rising 3.4 times
- The fall is real but small: worth knowing, not worth the loggers at this price

#### [day3#rank-rule] Rank by consequence, not by the order you found the flaws

*Ranking*

1. **Flips the decision**: F1 and F3 in variant 0; F7 too where it appears (+1.8 points, past the rule)
2. **Moves the number**, by how many points: none here; F5 moves it by 0.02 in other variants
3. **Misleads without moving a number**: an axis, an unstated uncertainty
4. **No effect on this answer**: still worth a note if it can bite elsewhere (the join)

#### [day3#own-variant] Each participant reviews a variant of their own, checked without a visible key

*Authenticity*

- Your participant number picks four flaws from the pool
- `U.flags_correct` compares a hash of your flags with the variant's
- Right or wrong, without revealing which flaws you missed

- **In the capstone.** The assessed review uses unseen variants made for each participant; review notes are matched against your own seeded flaws.

#### [day3#check-consequence] Which flaw goes first in the review?

*Checkpoint*

**Question:** A variant holds: a chart from 20%, unadjusted billing periods (moves the effect by 0.02 points), significance with no interval, and a before-after with no comparison (moves the effect from 2.3 to 4.1, past the 3-point rule).

- A. The chart axis
- B. The missing interval
- C. The before-after with no comparison
- D. The unadjusted billing periods

#### [day3#lab-3-2] Rank the flaws of your variant

Lab 3.2 · 25 min

Review a seeded-flaw notebook, a variant of its own for each participant, and rank its flaws by consequence.

[D3_2_review_seeded_flaw.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D3_2_review_seeded_flaw.ipynb)

- [ ] Load your variant and rerun it (5 min)
- [ ] Find the flaws, cell by cell (9 min)
- [ ] Consequence of each, with a recomputed number (6 min)
- [ ] Rank by consequence (3 min)
- [ ] Check your flags (2 min)
- [ ] ✱ Stretch: Fix the top flaw and rerun the analysis

### Session 3: Reviewing assistant-generated analysis

#### [day3#s3] Reviewing assistant-generated analysis

*Session 3*

- Name the failures typical of assistant-generated analyses
- Rerun an assistant's notebook and reconcile its summary with its output
- Write a verification note that meets the duty to verify

#### [day3#assistant-failures] An assistant's analysis looks finished; check five things before believing it

*What to expect*

- **It may not run**: a column or a function that does not exist
- **Its numbers may not come from its code**: a summary written beside the output
- **Outside numbers** with no source: benchmarks, norms

- **The direction** of a change reversed in the words
- **The method** answers an easier question than the one asked

> **Recap.** Recomputing and running a request twice are DS-206; here you review someone else's assistant-generated work.

#### [day3#sareea-summary] Sareea's summary reversed the direction of the change

*The case*

| Al-Nakheel, billed m3 per account per month | Before | After | Change |
| --- | --- | --- | --- |
| Sareea's summary | 21.4 | 19.6 | -8.2% |
| Recomputed from reads.csv | 25.8 | 28.7 | +11.5% |

> **And.** The notebook stops at cell s2 (no column "consumption"), and the "industry benchmark of 15%" has no source.

#### [day3#four-checks] All four checks fail, each with its evidence

*Four checks*

| Check | Result | Evidence |
| --- | --- | --- |
| Reruns as delivered | fail | KeyError: "consumption" is not a column |
| Every number traced to output | fail | 21.4, 19.6 and -8.2% appear nowhere |
| Outside numbers sourced | fail | The 15% benchmark has no source |
| Method fits the question | fail | Bills measure what the meters register, not what people use |

#### [day3#duty-to-verify] Verifying assistant output before use is a duty, not a courtesy

*The national guideline*

- Identify content generated with generative AI
- Check it for factual accuracy, especially in official reports
- Verify generated code before using or running it

- **Source.** SDAIA's Generative AI Guidelines for Government, in its sections on reliability and on users' responsibilities.

#### [day3#verification-note] A verification note says what may be used, what may not, and what next

*The deliverable*

- **Status.** Not verified: do not use the summary
- **May be used.** Billed m3 per account in Al-Nakheel rose from 25.8 to 28.7 (+11.5%) after the smart meters
- **May not be used.** The 8.2% fall, the 15% benchmark, the roll-out advice
- **Next.** Measure use another way (night flow at the district meter), against districts without smart meters

#### [day3#hosted-models] A hosted model may analyse synthetic data; Ghadeer's real extracts stay inside

*In the lab*

- The stretch sends the same prompt to a free hosted open-weight model, and you verify its answer the same way
- Without a key, the lab returns Sareea's recorded answer and says so

> **Classification.** Billing and contact extracts are Restricted: they do not go to a public assistant. The course data is synthetic, which is why it may.

#### [day3#check-assistant] What do you do with this summary?

*Checkpoint*

**Question:** An assistant's notebook runs, and its summary's three numbers all appear in the output. The summary concludes that smart meters "cut leakage in Al-Nakheel by nine points".

- A. Withhold it: the numbers are right but the method measures billing, not leakage
- B. Accept it: every number traces to the output
- C. Accept it once a chart is added
- D. Reject it because an assistant wrote it

#### [day3#lab-3-3] Verify the assistant's analysis

Lab 3.3 · 25 min

Rerun an assistant-generated analysis, find where it fails and write a verification note.

[D3_3_rerun_assistant_generated.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D3_3_rerun_assistant_generated.ipynb)

- [ ] Read the prompt and the summary the assistant gave (3 min)
- [ ] Rerun the notebook (5 min)
- [ ] Where it fails: four checks (9 min)
- [ ] Write the verification note (6 min)
- [ ] Label the assistant's part (2 min)
- [ ] ✱ Stretch: Ask a free hosted model for the same analysis and verify its answer

### Session 4: Review notes people act on

#### [day3#s4] Review notes people act on

*Session 4*

- Rewrite a vague note as problem, consequence and fix
- Order notes by consequence for the decision
- Recommend the kind of analysis the request needed

#### [day3#weak-strong-note] A note gets acted on when it names the problem, the consequence and the fix

*One note, twice*

- **Weak.** "The join looks off."
- **Acted on.** **Problem:** cell c2 joins repairs on the district name; rows spelt "Al Wurud" are dropped. **Consequence:** about a third of Al-Wurud's repairs vanish from the count. **Fix:** join on a district code and assert the row count.

#### [day3#note-parts] Three parts, each a full sentence

*The parts*

- **Problem.** Where, and exactly what: the cell, the line, the number
- **Consequence.** What it does to the number or the decision, in points or in the choice
- **Fix.** An action: "join on the code", not "consider the join"

> **Tone.** Write about the analysis, not the analyst: "cell c3 compares" rather than "you compared".

#### [day3#ranked-notes] Eight notes, ranked by what they do to the decision

*The order*

| Rank | Note | Consequence |
| --- | --- | --- |
| 1 | Success measured as leaks found | Reverses the decision |
| 2 | Before-after with no comparison | Adds about 1.8 points, past the rule |
| 3 to 6 | The unsourced 15%; estimates as actual reads; the join; no interval | A wrong or unverifiable number |
| 7, 8 | Chart axis; the spelling in the export | Cosmetic, or a cause handled elsewhere |

#### [day3#verdict-first] A review opens with its verdict on the decision

*The first lines*

- **For Nadia.** The recommendation to buy loggers does not hold. Measured on water lost against the other districts, detection cut non-revenue water by 2.3 points, below the 3-point rule; the analysis counted leaks found and compared the wrong months. Sabah will rerun it with the fixes below before the capital committee meets.

#### [day3#recommend-kind] A review can conclude that the request needed another kind of analysis

*After the review*

- Sareea's request asked a causal question and got a description of bills
- The right answer is a causal analysis against districts without smart meters, on a measure of use
- Sometimes the right recommendation is **no analysis yet**: the data cannot reach the question by the date

- **In the capstone defence.** You recommend the kind of analysis, and defend it when the sponsor changes a constraint.

#### [day3#capstone-brief] Hima Municipality's permits backlog doubled: frame it, plan it, review an analysis of it

*Capstone kickoff*

- **Sponsor:** Fahda Al-Bishr, director of permits: "Should we hire six more plan reviewers?"
- **Data:** 3,600 synthetic applications, an inventory, and an assistant-drafted analysis to review
- **Hand in:** a framing card, a two-page plan, ranked review notes, in a public repository

**8 + 10** minutes: the talk, during which the sponsor changes a constraint, then the defence

#### [day3#check-notes] Which note will the author act on?

*Checkpoint*

**Question:** Four notes on the same flaw in Sareea's analysis, which treats estimated bills as actual reads.

- A. "What about estimated reads?"
- B. "Use actual reads only."
- C. "You have overstated the change."
- D. "Cell s2 averages estimated bills as reads, so the change mixes billing timing with metering; recompute on actual reads and report the estimated share."

#### [day3#lab-3-4] Notes that get acted on

Lab 3.4 · 25 min

Rewrite review notes so each states the problem, its consequence and a fix, rank them, and choose the review target of the capstone.

[D3_4_rewrite_review_notes.ipynb](https://sdaiaacademy.github.io/ds-310/labs/D3_4_rewrite_review_notes.ipynb)

- [ ] Read the eight weak notes (3 min)
- [ ] Rewrite each: problem, consequence, fix (12 min)
- [ ] Rank by consequence (4 min)
- [ ] Tutor feedback and one revision (4 min)
- [ ] Open the capstone brief (2 min)
- [ ] ✱ Stretch: Write the summary paragraph a manager reads first

#### [day3#wrap-up] Three things to keep

*Day 3 · wrap-up*

- **Rerun, then read.** Run the analysis, reconcile every sentence with its output, then score five areas.
- **Rank by consequence.** A flaw that flips the decision goes first, whatever order you found it in.
- **Verify, label, then use.** Assistant output passes four checks and carries its label before anyone acts on it.

#### [day3#next] Capstone day: Hima Municipality's permits backlog

*Next*

Read `labs/capstone/BRIEF.md`, start your repository from `labs/capstone/README.md`, and draft the framing card. Bring questions for the sponsor.
