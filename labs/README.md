# Problem Framing and Analytical Review: labs

Notebooks for the SDAIA Academy course **DS-310 Problem Framing and Analytical Review**. Every lab works on
**Ghadeer Water Company**, a fictional water utility with six districts, and starts from files supplied in `data/`, so
none depends on an earlier lab. Each lab has a solution in `solutions/`. All data is synthetic and generated with a
fixed seed by `prepare_data.py`.

Nothing runs a model on your machine. A laptop CPU or a Colab CPU runtime is enough.

## Quick start

**Google Colab.** Open a notebook from the table below. Its first cell clones this repository and installs
`requirements-colab.txt`. To use the AI-tutor cells with a live model, add `OPENROUTER_API_KEY` in the Secrets panel
and turn on notebook access.

**Locally**, with [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/SDAIAAcademy/ds-310
cd ds-310/labs
cp .env.example .env            # optional: paste a free OpenRouter key
uv sync                         # creates .venv from pyproject.toml; uv.lock pins every version
uv run python prepare_data.py   # optional: rebuilds data/ (committed) from the seed
uv run jupyter lab
```

On Windows, set `PYTHONUTF8=1` before running if the console shows encoding errors.

Run `00_setup_check.ipynb` once before Day 1.

## Models and stand-ins

The AI-tutor cells ask a question about your work; the stretch of Lab 3.3 asks an assistant for an analysis. Both use a
free hosted open-weight model through OpenRouter when `OPENROUTER_API_KEY` is set.

| Setting (`.env`) | Default | Notes |
|---|---|---|
| `OPENROUTER_API_KEY` | empty | a free key from <https://openrouter.ai/keys>; optional |
| `ASSISTANT_MODEL` | `google/gemma-4-31b-it:free` | any free model id from <https://openrouter.ai/models?max_price=0> |
| `ASSISTANT_FALLBACKS` | `google/gemma-4-26b-a4b-it:free` | tried in order when the first is busy |
| `GHADEER_QUICK` | `0` | `1` shortens the slower cells |
| `GHADEER_PARTICIPANT` | `0` | your participant number for Lab 3.2, if you prefer not to edit `MY_NUMBER` |

Without a key, or when a free model does not answer, every lab still runs: the tutor cells print a stand-in question,
and Lab 3.3 returns the recorded answer of Sareea, the case's assistant, and says so. Free model ids change every few
weeks: if the default disappears, pick another free model.

The role-played interviews of Lab 1.3 use recorded answers from `data/roles.json`; in class the trainer plays the
roles.

## Notebooks

| Unit | Session | Notebook |
|---|---|---|
| Setup | Before Day 1 | [`00_setup_check.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/00_setup_check.ipynb) |
| Day 1 | Session 1 · Requests are not questions | [`D1_1_reframe_two_vague.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D1_1_reframe_two_vague.ipynb) |
| Day 1 | Session 2 · Question types | [`D1_2_classify_eight_requests.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D1_2_classify_eight_requests.ipynb) |
| Day 1 | Session 3 · Interviewing a stakeholder | [`D1_3_interview_role_played.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D1_3_interview_role_played.ipynb) |
| Day 1 | Session 4 · Feasibility and scope | [`D1_4_check_one_question.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D1_4_check_one_question.ipynb) |
| Day 2 | Session 1 · How the data are made | [`D2_1_map_meter_bill.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D2_1_map_meter_bill.ipynb) |
| Day 2 | Session 2 · Metrics and proxies | [`D2_2_stress_test_water.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D2_2_stress_test_water.ipynb) |
| Day 2 | Session 3 · Analysis plans | [`D2_3_write_plan_framed.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D2_3_write_plan_framed.ipynb) |
| Day 2 | Session 4 · Threats to validity | [`D2_4_swap_plans_peer.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D2_4_swap_plans_peer.ipynb) |
| Day 3 | Session 1 · A review checklist | [`D3_1_apply_checklist_short.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D3_1_apply_checklist_short.ipynb) |
| Day 3 | Session 2 · Finding the flaws that matter | [`D3_2_review_seeded_flaw.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D3_2_review_seeded_flaw.ipynb) |
| Day 3 | Session 3 · Reviewing assistant-generated analysis | [`D3_3_rerun_assistant_generated.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D3_3_rerun_assistant_generated.ipynb) |
| Day 3 | Session 4 · Review notes people act on | [`D3_4_rewrite_review_notes.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-310/blob/main/labs/D3_4_rewrite_review_notes.ipynb) |
| Capstone | Hima Municipality permits backlog | [`capstone/README.md`](capstone/README.md) |

Your work is saved to `labs/out/`, which is not part of the course.

The variants of Lab 3.2 are for practice: the code that makes them is in this repository. The variants used in the
capstone review are prepared by the trainer and are not published.

## For maintainers

The notebooks are generated from the percent-format sources in `_src/` by `_tools/py2nb.py`
(`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `solutions/`. Edit the sources, not
the notebooks.
