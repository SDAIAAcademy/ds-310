"""Helpers shared by every lab of Problem Framing and Analytical Review (DS-310).

The case: Ghadeer Water Company, a fictional water utility with six districts. All data is synthetic
(prepare_data.py, seed 310).

    import ghadeer as U
    reads = U.csv("reads")                 # a DataFrame from data/reads.csv
    U.check(cond, "what is true")          # prints a tick, or stops with what is not true yet
    U.interview("sultana", "question?")    # the scripted stand-in for a role-played stakeholder
    U.tutor(draft, "what to look at")      # AI-tutor feedback: a free hosted model, or a stand-in that says so
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
OUT = LABS / "out"
QUICK = os.getenv("GHADEER_QUICK", "0") == "1"
DISTRICTS = {"D1": "Al-Rawdah", "D2": "Al-Wurud", "D3": "Al-Nakheel", "D4": "Al-Hamra", "D5": "Al-Salam", "D6": "Al-Shifa"}
TARGET_MONTH = 13


def _load_env():
    env = LABS / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"'))
    try:  # Colab: the Secrets panel
        from google.colab import userdata  # type: ignore
        os.environ.setdefault("OPENROUTER_API_KEY", userdata.get("OPENROUTER_API_KEY") or "")
    except Exception:
        pass


_load_env()


# ------------------------------------------------------------------ files
def pick(full, quick):
    """The small value in quick mode (GHADEER_QUICK=1), the full one otherwise."""
    return quick if QUICK else full


def csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / f"{name}.csv")


def js(name: str):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def text(name: str) -> str:
    return (DATA / name).read_text(encoding="utf-8")


def reference(name: str):
    """A reference result, so later cells run when an exercise is not done yet."""
    return json.loads((DATA / "reference" / f"{name}.json").read_text(encoding="utf-8"))


def save(name: str, content: str) -> Path:
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")
    print("saved", p.relative_to(LABS).as_posix())
    return p


def check(cond: bool, what: str):
    if not cond:
        raise AssertionError("not yet: " + what)
    print("✅", what)


def words(s: str) -> int:
    return len(re.findall(r"[\w'%.,-]+", s))


# ------------------------------------------------------------------ the water balance
def nrw(normalise_cycle: bool = False) -> pd.DataFrame:
    """Non-revenue water by district and month: (system input - billed) / system input, in percent.

    normalise_cycle=True rescales each bill to 30 days, the length of the supply month."""
    reads, supply = csv("reads"), csv("supply")
    vol = reads.billed_m3 / reads.cycle_days * 30 if normalise_cycle else reads.billed_m3
    billed = vol.groupby([reads.district, reads.month]).sum().rename("billed_m3").reset_index()
    m = supply.merge(billed, on=["district", "month"])
    m["nrw_pct"] = 100 * (m.system_input_m3 - m.billed_m3) / m.system_input_m3
    return m


def period_mean(df: pd.DataFrame, district: str, months: range, col: str = "nrw_pct") -> float:
    return float(df[(df.district == district) & df.month.isin(list(months))][col].mean())


def detectable_change(sd: float, n_before: int, n_after: int, z: float = 2.8) -> float:
    """Smallest difference of two period means that a comparison can tell from noise (80% power, 5% two-sided):
    about 2.8 standard errors."""
    return z * sd * math.sqrt(1 / n_before + 1 / n_after)


# ------------------------------------------------------------------ framing cards
CARD_FIELDS = ["decision_maker", "decision", "options", "estimand", "decision_rule", "affected", "personal_data_needed"]
ESTIMAND_FIELDS = ["population", "variable", "contrast", "intercurrent", "summary"]
VAGUE = ["improve", "better", "high", "low", "soon", "look into", "find out", "understand", "why", "issues", "problem"]


def card_gaps(card: dict) -> list[str]:
    """The questions a peer would still have to ask before planning from this card."""
    gaps = []
    for f in CARD_FIELDS:
        if f not in card or card[f] in (None, "", []):
            gaps.append(f"What is the {f.replace('_', ' ')}?")
    dec = str(card.get("decision", ""))
    if dec and not dec.strip().endswith("?"):
        gaps.append("Is the decision written as a question that ends in a choice?")
    if dec and not re.match(r"\s*(should|which|do we|does|is it worth|can we)", dec.lower()):
        gaps.append("Which choice does the decision ask for (should we ..., which ...)?")
    if len(card.get("options", []) or []) < 2:
        gaps.append("What are the options, including doing nothing?")
    est = card.get("estimand", {}) or {}
    for f in ESTIMAND_FIELDS:
        if not str(est.get(f, "")).strip():
            gaps.append(f"Estimand: what is the {f}?")
    rule = str(card.get("decision_rule", ""))
    if rule and not re.search(r"\d", rule):
        gaps.append("Decision rule: at what number does the choice change?")
    for w in VAGUE:
        if re.search(r"\b" + re.escape(w) + r"\b", (dec + " " + rule).lower()):
            gaps.append(f"What does '{w}' mean here, in a number?")
    if card.get("personal_data_needed") not in (True, False):
        gaps.append("Does the question need personal data at all (yes or no)?")
    return gaps


def card_markdown(card: dict, title: str) -> str:
    est = card.get("estimand", {})
    lines = [f"# {title}", "", f"**Decision maker.** {card.get('decision_maker', '')}", "",
             f"**Decision.** {card.get('decision', '')}", "", "**Options**"]
    lines += [f"- {o}" for o in card.get("options", [])]
    lines += ["", "**Estimand**"] + [f"- {k}: {est.get(k, '')}" for k in ESTIMAND_FIELDS]
    lines += ["", f"**Decision rule.** {card.get('decision_rule', '')}", "", "**Affected**"]
    lines += [f"- {a}" for a in card.get("affected", [])]
    lines += ["", f"**Personal data needed.** {'yes' if card.get('personal_data_needed') else 'no'}"]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ interviews (scripted stand-ins for role-play)
_LOG: dict[str, set] = {}
LEADING = ["don't you think", "isn't it", "wouldn't you agree", "surely", "right?", "obviously", "you agree"]
CLOSED = ("is ", "are ", "do ", "does ", "did ", "can ", "could ", "will ", "would ", "have ", "has ")


def question_kind(q: str) -> str:
    s = q.strip().lower()
    if any(x in s for x in LEADING):
        return "leading"
    if s.startswith(CLOSED):
        return "closed"
    return "open"


def interview(role: str, question: str) -> str:
    """The stand-in answers by topic. The trainer or a peer with the role card is better: use this to practise."""
    r = js("roles")[role]
    kind = question_kind(question)
    q = question.lower()
    hits = [t for t in r["topics"] if any(k in q for k in t["keys"])]
    if kind == "leading":
        return f"{r['name']}: Yes, I suppose so. (A leading question gets agreement, not information.)"
    if not hits:
        return f"{r['name']}: I am not sure what you mean. Can you ask about something specific?"
    score = {t["id"]: sum(k in q for k in t["keys"]) for t in hits}
    hits.sort(key=lambda t: -score[t["id"]])
    hits = hits[:1] + [t for t in hits[1:2] if score[t["id"]] >= 1 and len(hits) > 1 and " and " in q]
    _LOG.setdefault(role, set()).update(t["id"] for t in hits)
    ans = " ".join(t["answer"] for t in hits)
    if kind == "closed":
        ans = "Yes. " + ans.split(". ")[0] + "."
    return f"{r['name']}: {ans}"


def interview_coverage(role: str) -> tuple[int, int, list[str]]:
    """How many of the role's constraints your questions reached, and which topics you did not."""
    r = js("roles")[role]
    asked = _LOG.get(role, set())
    cons = [t["id"] for t in r["topics"] if t.get("constraint")]
    return len(asked & set(cons)), len(cons), [t for t in cons if t not in asked]


def reset_interview(role: str):
    _LOG.pop(role, None)


# ------------------------------------------------------------------ feasibility
def ready_in_business_days(ds: dict) -> int:
    """Business days until a dataset can be used: internal access, or the sharing timeframe for another entity."""
    if ds.get("external") and ds.get("classification") != "Public":
        return ds["sharing_assess_business_days"] + ds["sharing_deliver_business_days"]
    return ds.get("access_business_days", 0)


# ------------------------------------------------------------------ diagrams
def mermaid_flow(steps: list[str], marks: dict[int, str] | None = None) -> str:
    """A left-to-right Mermaid flowchart; marks maps a step number (1-based) to a warning shown under it."""
    marks = marks or {}
    lines = ["flowchart LR"]
    for i, s in enumerate(steps, 1):
        label = s.replace('"', "'")
        lines.append(f'  S{i}["{i}. {label}"]')
        if i > 1:
            lines.append(f"  S{i - 1} --> S{i}")
    for i, m in marks.items():
        lines.append(f'  M{i}(["⚠ {m.replace(chr(34), chr(39))}"]) -.- S{i}')
        lines.append(f"  style M{i} fill:#fde2e1,stroke:#c0392b")
    return "\n".join(lines) + "\n"


def mermaid_tree(tree: dict, notes: dict[str, str] | None = None, guardrails: list[dict] | None = None) -> str:
    notes, guardrails = notes or {}, guardrails or []
    lines = ["flowchart TD", '  G["' + tree["goal"] + '"]']
    for n in tree["nodes"]:
        lab = n["name"] + (f"<br/>⚠ {notes[n['id']]}" if n["id"] in notes else "")
        lines.append(f'  {n["id"]}["{lab}"]')
        lines.append(f'  {n["parent"] or "G"} --> {n["id"]}')
    for i, g in enumerate(guardrails, 1):
        lines.append(f'  GR{i}{{{{"Guardrail: {g["metric"]}"}}}} -.- {g["guards"]}')
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ plans
PLAN_SECTIONS = ["question", "data", "method", "detectable_change", "threats", "would_change", "timeline"]


def score_plan(plan: dict, deadline_business_days: int = 10) -> dict:
    """The plan rubric, checked by rule: each criterion 0, 1 or 2. A person reads the plan too."""
    inv = {d["id"]: d for d in js("inventory")["datasets"]}
    s = {}
    s["complete"] = 2 if all(str(plan.get(k, "")).strip() for k in PLAN_SECTIONS) else 0
    data = plan.get("data", []) if isinstance(plan.get("data"), list) else []
    late = [d for d in data if d in inv and ready_in_business_days(inv[d]) > deadline_business_days - 4]
    unknown = [d for d in data if d not in inv]
    s["data_feasible"] = 2 if data and not late and not unknown else (1 if data and not unknown else 0)
    method = str(plan.get("method", "")).lower()
    s["method_has_comparison"] = 2 if re.search(r"compar|difference.in.difference|other (\w+ )?districts|control|against", method) else 0
    threats = plan.get("threats", []) if isinstance(plan.get("threats"), list) else []
    s["threats"] = 2 if len(threats) >= 3 else (1 if threats else 0)
    wc = str(plan.get("would_change", ""))
    s["would_change_numeric"] = 2 if re.search(r"\d", wc) and any(w in wc.lower() for w in ("if", "below", "above", "less", "more")) else 0
    s["fits_two_pages"] = 2 if words(json.dumps(plan)) <= 900 else 0
    s["total"] = sum(s.values())
    s["max"] = 12
    return s


# ------------------------------------------------------------------ review (Labs 3.1 to 3.4)
AREAS = ["question_fit", "data_handling", "method", "inference", "communication"]
SEVERITY_ORDER = {"critical": 0, "major": 1, "minor": 2}


def flags_hash(variant: int, flags: list[str]) -> str:
    return hashlib.sha256(f"ds310|{variant}|{','.join(sorted(set(flags)))}".encode()).hexdigest()[:16]


def flags_correct(variant: int, flags: list[str]) -> bool:
    """True when your flags are exactly the flaws seeded in your variant (checked against a hash, not a key)."""
    return js("review/variant_hashes")[str(variant)] == flags_hash(variant, flags)


def run_cells(source: str, env: dict | None = None) -> dict:
    """Run a notebook kept as a text file (cells marked '# cell <id>'), cell by cell. Returns each cell's result:
    'ok' or the error it raised, so a review can say exactly where an analysis fails."""
    import contextlib
    import io
    env = {"U": __import__(__name__), "pd": pd} if env is None else env
    results = {}
    for block in re.split(r"(?m)^# cell ", source)[1:]:
        cid, _, code = block.partition("\n")
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(code, env)
            results[cid.strip()] = {"status": "ok", "out": buf.getvalue()}
        except Exception as e:  # the analysis under review may fail: record, do not stop
            results[cid.strip()] = {"status": f"{type(e).__name__}: {e}", "out": buf.getvalue()}
    results["_env"] = env
    return results


NOTE_FIELDS = ["problem", "consequence", "fix"]


def note_problems(note: dict) -> list[str]:
    """What a reader of a review note would still miss."""
    out = []
    for f in NOTE_FIELDS:
        if words(str(note.get(f, ""))) < 6:
            out.append(f"{note.get('id', '?')}: the {f} needs a full sentence")
    cons = str(note.get("consequence", "")).lower()
    if cons and not (re.search(r"\d", cons) or any(w in cons for w in ("decision", "recommend", "wrong", "overstat", "understat", "reverse", "cannot"))):
        out.append(f"{note.get('id', '?')}: the consequence does not say what it does to the result or the decision")
    fix = str(note.get("fix", "")).strip().lower()
    if fix and fix.split()[0] in ("maybe", "consider", "perhaps", "think"):
        out.append(f"{note.get('id', '?')}: the fix should be an action, not a suggestion to think")
    return out


# ------------------------------------------------------------------ the hosted model: tutor and assistant
OPENROUTER = "https://openrouter.ai/api/v1/chat/completions"
# Free models change every few weeks: choose one at openrouter.ai/models?max_price=0 and set ASSISTANT_MODEL.
MODEL = os.getenv("ASSISTANT_MODEL", "google/gemma-4-31b-it:free")  # an open-weight model, free tier
FALLBACKS = [m for m in os.getenv("ASSISTANT_FALLBACKS", "google/gemma-4-26b-a4b-it:free").split(",") if m]
TUTOR_RULES = ("You are a tutor for analysts learning to frame questions and review analyses. Ask at most four short "
               "questions about the draft. Do not rewrite it and do not supply a framing or an answer.")


def _call(messages: list[dict], timeout: int = 60) -> str | None:
    key = os.getenv("OPENROUTER_API_KEY", "")
    if not key:
        return None
    body = {"model": MODEL, "models": [MODEL] + [m for m in FALLBACKS if m != MODEL], "messages": messages}
    req = urllib.request.Request(OPENROUTER, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"]
    except (urllib.error.URLError, KeyError, TimeoutError, json.JSONDecodeError):
        return None


def tutor(draft: str, focus: str) -> str:
    """AI-tutor questions on a draft: a free hosted model when OPENROUTER_API_KEY is set and answers, otherwise a
    rule-based stand-in that says so in its first line. Advice only: you decide."""
    reply = _call([{"role": "system", "content": TUTOR_RULES},
                   {"role": "user", "content": f"Focus: {focus}\n\nDraft:\n{draft}"}])
    if reply:
        return reply
    qs = []
    if not re.search(r"\d", draft):
        qs.append("Which number would show the reader how big the problem is?")
    if not any(w in draft.lower() for w in ("decision", "recommend", "choose", "should")):
        qs.append("Which decision does this change?")
    if words(draft) > 120:
        qs.append(f"The draft has {words(draft)} words: which sentence could go?")
    qs.append(f"You asked about this: {focus.rstrip('?.')}. What would a sceptical manager ask first?")
    return "[stand-in tutor (no model answered): rule checks, not a model's reading]\n- " + "\n- ".join(qs)


def assistant(prompt: str) -> tuple[str, str]:
    """Ask a free hosted model for an analysis. Without a key or an answer: the recorded answer of Sareea, the
    assistant whose work Lab 3.3 reviews. Returns (source, text)."""
    reply = _call([{"role": "user", "content": prompt}], timeout=90)
    if reply:
        return MODEL, reply
    return "recorded answer (no model answered)", text("review/sareea/notebook.py") + "\n" + text("review/sareea/summary.md")
