---
course: "Problem Framing and Analytical Review"
code: "DS-310"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-310/index.html"
---

# Problem Framing and Analytical Review

صياغة المشكلات التحليلية ومراجعة التحليلات

Data Science Track · 3 teaching days + capstone day · 21 hours · Level 300

Turn vague requests into answerable decision questions, plan the analysis, and review analyses by people and assistants by consequence

Participants practise the work before and after an analysis, using requests from Ghadeer Water Company, a fictional water utility. They turn vague requests into decision questions with an estimand, a metric and a decision rule, interview a role-played manager, use domain knowledge of metering, billing and repair to see where the data mislead, and test whether data and deadline make the question answerable. They then review analyses by peers and by an assistant and write review notes ranked by consequence. Metric definition is DS-307; team review standards are DS-407.

**Who it is for:** Practitioners. Data scientists and analysts who have completed the level 200 set or can show equivalent work: an analysis they framed, carried out and explained to a stakeholder.

**Format:** Intensive: 3 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Ghadeer Water Company.** Ghadeer Water Company is a fictional water utility with six districts whose managers send vague requests about water loss, leak repair, billing and complaints. Participants frame those requests with an estimand and a decision rule, interview a role-played operations manager and metering engineer, map how meter reads become bills, stress-test the water-loss and customer-service metric tree, write and attack analysis plans, and review three seeded-flaw analyses, one written by the assistant Sareea. The capstone moves to a second case, the Building Permits Department of Hima Municipality and its permits backlog. All data is synthetic and generated with a fixed seed.

## The course

### Day 1: From request to question

Slides: https://sdaiaacademy.github.io/ds-310/slides/day1.md

- **Session 1: Requests are not questions**
  - Separate the decision behind a request from the topic it names
  - State an estimand with population, variable, contrast and summary
  - Write a decision rule a peer can apply without asking you
  - [Lab 1.1: Two framing cards (AI-off) (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D1_1_reframe_two_vague.ipynb)
- **Session 2: Question types**
  - Classify a request as descriptive, predictive, causal or unanswerable
  - Match each type to description, an experiment, a causal analysis, a model or no analysis
  - Change the recommendation when a constraint changes
  - [Lab 1.2: Eight requests classified (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D1_2_classify_eight_requests.ipynb)
- **Session 3: Interviewing a stakeholder**
  - Map decision makers, users and affected groups for a request
  - Ask open questions that surface constraints and acceptable evidence
  - Record what was said apart from what was assumed
  - [Lab 1.3: Interview the operations manager (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D1_3_interview_role_played.ipynb)
- **Session 4: Feasibility and scope**
  - Estimate when each dataset in a plan can be ready
  - Apply classification, sharing time limits and minimisation to a data request
  - Cut a question's scope until it fits the deadline
  - [Lab 1.4: Check and cut one question (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D1_4_check_one_question.ipynb)

### Day 2: Know the domain, plan the work

Slides: https://sdaiaacademy.github.io/ds-310/slides/day2.md

- **Session 1: How the data are made**
  - Read a briefing pack and an expert interview for how a metric is produced
  - Draw the meter-to-bill process as a diagram
  - Mark where the data can mislead, with a number from the data
  - [Lab 2.1: The meter-to-bill map (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D2_1_map_meter_bill.ipynb)
- **Session 2: Metrics and proxies**
  - Trace a goal to the proxies a metric tree uses for it
  - Recognise the four ways a proxy fails under pressure
  - Propose guardrail metrics that expose the gaming
  - [Lab 2.2: Stress-test the metric tree (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D2_2_stress_test_water.ipynb)
- **Session 3: Analysis plans**
  - Write an analysis plan with data, method and threats to validity
  - Compute what change the available data can detect
  - State in advance the result that would change the decision
  - [Lab 2.3: A plan for a framed question (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D2_3_write_plan_framed.ipynb)
- **Session 4: Threats to validity**
  - Name the main threats to the validity of a plan
  - Show regression to the mean in data chosen for being extreme
  - Rank threats by how much they could change the decision
  - [Lab 2.4: Three threats each (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D2_4_swap_plans_peer.ipynb)

### Day 3: Review others' work

Slides: https://sdaiaacademy.github.io/ds-310/slides/day3.md

- **Session 1: A review checklist**
  - Rerun an analysis before judging it
  - Apply a checklist of five areas from question fit to communication
  - Score an analysis so another reviewer would score it alike
  - [Lab 3.1: Score a short notebook (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D3_1_apply_checklist_short.ipynb)
- **Session 2: Finding the flaws that matter**
  - Locate seeded flaws cell by cell
  - Measure each flaw's consequence with a recomputed number
  - Rank flaws by their effect on the decision
  - [Lab 3.2: Rank the flaws of your variant (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D3_2_review_seeded_flaw.ipynb)
- **Session 3: Reviewing assistant-generated analysis**
  - Name the failures typical of assistant-generated analyses
  - Rerun an assistant's notebook and reconcile its summary with its output
  - Write a verification note that meets the duty to verify
  - [Lab 3.3: Verify the assistant's analysis (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D3_3_rerun_assistant_generated.ipynb)
- **Session 4: Review notes people act on**
  - Rewrite a vague note as problem, consequence and fix
  - Order notes by consequence for the decision
  - Recommend the kind of analysis the request needed
  - [Lab 3.4: Notes that get acted on (25 min)](https://sdaiaacademy.github.io/ds-310/labs/D3_4_rewrite_review_notes.ipynb)

### Capstone: Capstone: the permits backlog, framed and defended

Slides: https://sdaiaacademy.github.io/ds-310/slides/capstone.md

## Capstone

A framing card, analysis plan and peer review for a second synthetic case (a municipal permits backlog), submitted as a repository and presented while the role-played sponsor changes a constraint, with ten minutes of defence

**What you submit:** A public GitHub repository link holding the framing card, the analysis plan and the review notes, with the capstone README filled in

**Rubric:**

- Framing card a peer can plan from: 20%
- Analysis plan, threats and the deciding result: 20%
- Review notes ranked by consequence: 20%
- The kind of analysis recommended: 10%
- Defence under the changed constraint: 30%

## Outcomes

- **LO1** Prepare a decision question with estimand, population, metric and decision rule from a vague request, given five requests from the utility's managers (Applied) Evidence: framing cards a peer can plan from without further questions
- **LO2** Analyse a metric set for proxy failure and gaming, and propose guardrail metrics, given the utility's metric tree for water loss and customer service (Applied) Evidence: an annotated tree with two guardrails and the behaviour each prevents
- **LO3** Use domain documents and an expert interview to map how the data behind a metric are produced, given a briefing pack on metering, billing cycles and leak repair, and a role-played engineer (Applied) Evidence: a process map marking three points where the data can mislead
- **LO4** Design an analysis plan stating data, method, threats to validity and the result that would change the decision, given a framed question, a data inventory and a two-week deadline (Performance) Evidence: a two-page plan scored against a rubric
- **LO5** Review an analysis for errors in question fit, data handling, method, inference and communication, given three seeded-flaw notebooks, one generated by an assistant (Performance) Evidence: review notes ranking the critical flaws by consequence, each with a fix
- **LO6** Decide whether a request needs description, an experiment, a causal analysis, a predictive model or no analysis, given a role-played sponsor whose constraints change during the meeting (Performance) Evidence: a recommendation defended against the assessor's challenge

## Tools

- **Notebook or report:** Jupyter, marimo, Quarto
- **Diagrams for process maps and metric trees:** Mermaid, draw.io
- **Review comments:** pull or merge requests in Git, comments in a shared document
- **Assistant that generates the analysis under review:** a free hosted open-weight model, any commercial coding assistant

## Prerequisites

- DS-204 Machine Learning for Tabular Data: Baselines and Validation
- DS-205 Designing and Reading Experiments
- Has completed at least one analysis for a stakeholder
- Reads a notebook in Python or R and reruns it
- Setup: a laptop processor with uv, or Google Colab. Nothing downloads a model; a free hosted model key is optional (every assistant cell has a stand-in). Run 00_setup_check before Day 1; see labs/README.md.

## Sources

### Framing and question types

- [Leek and Peng (2015), What is the question? Science 347(6228)](https://doi.org/10.1126/science.aaa6146)
- [ICH E9(R1) Addendum on estimands and sensitivity analysis in clinical trials (2019)](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf)
- [IBM SPSS Modeler, CRISP-DM Help Overview](https://www.ibm.com/docs/en/spss-modeler/saas?topic=dm-crisp-help-overview)

### Metrics, plans and validity

- [Manheim and Garrabrant (2018), Categorizing Variants of Goodhart's Law](https://arxiv.org/abs/1803.04585)
- [Gelman and Loken (2013), The garden of forking paths](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf)

### Water utility domain

- [Alliance for Water Efficiency, Water Audit (the IWA and AWWA water balance)](https://allianceforwaterefficiency.org/resource/water-audit/)

### National references

- [Personal Data Protection Law](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [Data Classification Policy (NDMO)](https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf)
- [Data Sharing Policy (NDMO)](https://sdaia.gov.sa/en/SDAIA/about/Documents/DataSharingPolicyEN.pdf)
- [Principles of AI Ethics (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)
- [Generative AI Guidelines for Government (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Files/GenAIGuidelinesForGovernmentENCompressed.pdf)

### Tools

- [Jupyter](https://jupyter.org/)
- [marimo](https://marimo.io/)
- [Quarto](https://quarto.org/)
- [draw.io](https://www.drawio.com/)
- [OpenRouter free models](https://openrouter.ai/models?max_price=0)

---

SDAIA Academy · Data Science Track · Problem Framing and Analytical Review

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-15 · commit 95ffc6b
