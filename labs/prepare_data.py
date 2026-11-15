# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Write every synthetic file of Problem Framing and Analytical Review (DS-310).

The case: Ghadeer Water Company, a fictional water utility with six districts. Standard library only,
seed 310: the same bytes on every run. Run from labs/:  uv run prepare_data.py

Planted problems (the trainer's key is solutions/answer_key.md):
  P1  Estimated reads: accounts without meter access are billed on an average; Al-Hamra (D4) worst  -> Lab 2.1
  P2  Billing cycles of 27 to 35 days make monthly billed volume swing                              -> Lab 2.1
  P3  Smart meters in Al-Nakheel (D3) from month 13 register what old meters missed: billed use rises -> Labs 2.1, 3.3
  P4  Repair-time target from month 13: jobs closed at the first visit, reopenings rise; job creation
      delayed after the report                                                                    -> Lab 2.2
  P5  First-contact target from month 13: more contacts marked resolved, more repeat contacts         -> Lab 2.2
  P6  Al-Wurud (D2) bulk meter drift in months 10 to 12 (input over-read), corrected in month 13, the
      same month active leak detection starts there: before-after mixes three effects              -> Labs 2.4, 3.2
  P7  The repairs export spells Al-Wurud two ways                                                  -> Lab 3.2
  P8  Road-works data are held by another entity: the sharing timeframe exceeds the deadline        -> Lab 1.4
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CAP = ROOT / "capstone" / "data"
SEED = 310
MONTHS = 24
TARGET_MONTH = 13  # repair-time and first-contact targets, smart meters in D3, active detection in D2

DISTRICTS = [
    ("D1", "Al-Rawdah", 0.27), ("D2", "Al-Wurud", 0.21), ("D3", "Al-Nakheel", 0.17),
    ("D4", "Al-Hamra", 0.19), ("D5", "Al-Salam", 0.14), ("D6", "Al-Shifa", 0.16),
]  # id, name, real-loss share of input before any change
NAME = {d: n for d, n, _ in DISTRICTS}


def season(month: int) -> float:
    m = (month - 1) % 12 + 1
    return 1.25 if 6 <= m <= 9 else (1.1 if m in (5, 10) else 1.0)


def write_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def digest(*parts) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------------------------- accounts and reads
def make_accounts(rng: random.Random) -> list[dict]:
    rows = []
    for d, _, _ in DISTRICTS:
        for i in range(400):
            commercial = rng.random() < 0.12
            access_issue = rng.random() < (0.30 if d == "D4" else 0.05)
            rows.append({
                "account_id": f"{d}-{i + 1:04d}", "district": d,
                "customer_type": "commercial" if commercial else "residential",
                "meter_age_years": rng.randint(1, 12),
                "smart_meter_from_month": TARGET_MONTH if d == "D3" else 0,
                "access_issue": int(access_issue),
                "_daily": round(rng.lognormvariate(math.log(2.4 if commercial else 0.62), 0.35), 4),
            })
    return rows


def cycle_days(rng: random.Random) -> dict:
    return {(d, m): rng.choice([27, 28, 29, 30, 30, 31, 31, 32, 33, 35]) for d, _, _ in DISTRICTS for m in range(1, MONTHS + 1)}


def make_reads(rng: random.Random, accounts: list[dict], cyc: dict) -> tuple[list[dict], dict]:
    rows, true_use = [], {}
    for a in accounts:
        history = []
        for m in range(1, MONTHS + 1):
            days = cyc[(a["district"], m)]
            true = a["_daily"] * season(m) * days
            smart = a["smart_meter_from_month"] and m >= a["smart_meter_from_month"]
            reg = 1.0 if smart else 1 - 0.015 * (a["meter_age_years"] + (m - 1) / 12)
            actual = true * reg
            estimated = a["access_issue"] and rng.random() < 0.6 and len(history) >= 3
            if estimated:
                billed = sum(history[-3:]) / 3  # average of the last three actual reads
                read_type = "estimated"
            else:
                billed = actual
                read_type = "actual"
                history.append(actual)
            rows.append({"account_id": a["account_id"], "district": a["district"], "month": m, "read_type": read_type,
                         "cycle_days": days, "billed_m3": round(billed, 2)})
            true_use[(a["district"], m)] = true_use.get((a["district"], m), 0.0) + a["_daily"] * season(m) * 30
    return rows, true_use


def make_supply(rng: random.Random, true_use: dict) -> list[dict]:
    rows = []
    for d, _, loss in DISTRICTS:
        for m in range(1, MONTHS + 1):
            use = true_use[(d, m)]
            real = loss
            if d == "D2" and m >= TARGET_MONTH + 2:
                real = loss * 0.885  # active leak detection removes about a ninth of real losses, with a lag
            if d == "D1":
                real = loss * (1 + 0.004 * m)  # ageing mains
            unauthorised = 0.02
            input_true = use / (1 - real - unauthorised)
            input_true *= rng.uniform(0.985, 1.015)
            drift = 1.07 if (d == "D2" and 10 <= m <= 12) else 1.0  # P6: bulk meter over-reads, corrected in month 13
            rows.append({"district": d, "district_name": NAME[d], "month": m, "system_input_m3": round(input_true * drift, 1)})
    return rows


# ---------------------------------------------------------------------------------------------- repairs and contacts
def make_repairs(rng: random.Random) -> list[dict]:
    rows, n = [], 0
    for d, _, loss in DISTRICTS:
        for m in range(1, MONTHS + 1):
            k = rng.randint(2, 4) + (2 if d == "D1" else 0)
            sources = ["customer_report"] * k
            if d == "D2" and m >= TARGET_MONTH:
                sources += ["active_detection"] * rng.randint(6, 9)
            for src in sources:
                n += 1
                reported = (m - 1) * 30 + rng.randint(0, 29)
                after = m >= TARGET_MONTH
                lag_create = rng.choice([0, 0, 0, 1]) + (rng.choice([0, 1, 2, 2, 3]) if after else 0)
                created = reported + lag_create
                first_visit = created + rng.choice([1, 1, 2, 2, 3])
                if after:
                    closed = first_visit  # P4: closed at the first visit to meet the target
                    reopened = rng.random() < 0.24
                else:
                    closed = first_visit + rng.choice([1, 2, 2, 3, 4])
                    reopened = rng.random() < 0.06
                final_fix = closed + (rng.randint(3, 8) if reopened else 0)
                spelled = NAME[d]
                if d == "D2" and rng.random() < 0.35:
                    spelled = "Al Wurud"  # P7
                rows.append({"work_order": f"WO-{n:05d}", "district_name": spelled, "month": m, "source": src,
                             "reported_day": reported, "job_created_day": created, "first_visit_day": first_visit,
                             "closed_day": closed, "reopened": int(reopened), "final_fix_day": final_fix})
    return rows


def make_contacts(rng: random.Random, accounts: list[dict]) -> list[dict]:
    rows, n = [], 0
    reasons = ["billing", "billing", "leak", "pressure", "quality", "meter_access", "other"]
    pool = [a for a in accounts if a["customer_type"] == "residential"]
    for m in range(1, MONTHS + 1):
        after = m >= TARGET_MONTH
        for _ in range(260):
            a = rng.choice(pool)
            reason = rng.choice(reasons + (["billing"] if a["access_issue"] else []))
            day = (m - 1) * 30 + rng.randint(0, 27)
            # the shorter call script of month 13 resolves fewer calls for real
            truly_resolved = rng.random() < (0.70 if reason != "billing" else 0.60) - (0.08 if after else 0.0)
            marked = truly_resolved or (after and rng.random() < 0.55)  # P5
            n += 1
            rows.append({"contact_id": f"C-{n:05d}", "account_id": a["account_id"], "district": a["district"], "month": m,
                         "day": day, "reason": reason, "handle_min": round(max(2.0, rng.gauss(7.5 if not after else 5.9, 2.2)), 1),
                         "marked_resolved": int(marked)})
            if not truly_resolved and rng.random() < 0.75:
                n += 1
                rows.append({"contact_id": f"C-{n:05d}", "account_id": a["account_id"], "district": a["district"],
                             "month": m if day + 3 < m * 30 else min(m + 1, MONTHS), "day": day + rng.randint(1, 6),
                             "reason": reason, "handle_min": round(max(2.0, rng.gauss(8.5, 2.5)), 1), "marked_resolved": 1})
    rows.sort(key=lambda r: (r["day"], r["contact_id"]))
    return rows


# ---------------------------------------------------------------------------------------------- documents
REQUESTS = {
    "framing": [
        {"id": "R1", "from": "Nadia Al-Rubaie, director of non-revenue water and customer operations",
         "text": "Water loss in Al-Rawdah is out of control. I need to know why before the board meets in two weeks."},
        {"id": "R2", "from": "Khalil Al-Sabhi, billing manager",
         "text": "Customers in Al-Hamra say their bills are wrong. Can you look into the estimated bills?"},
        {"id": "R3", "from": "Sultana Al-Kanaan, customer service operations manager",
         "text": "Repeat complaints are too high. Find out what is going on."},
        {"id": "R4", "from": "Mamdouh Al-Qarawi, metering and leak-repair engineer",
         "text": "The acoustic-logger pilot in Al-Wurud found lots of leaks. Should we buy loggers for more districts?"},
        {"id": "R5", "from": "Nadia Al-Rubaie, director of non-revenue water and customer operations",
         "text": "Do the smart meters work? Al-Nakheel's consumption went up after we installed them."},
    ],
    "classify": [
        {"id": "C1", "text": "How many leak repairs did each district have last quarter?"},
        {"id": "C2", "text": "Which accounts are likely to get an estimated bill next month because the reader cannot reach the meter?"},
        {"id": "C3", "text": "Did the first-contact target, introduced in every team at once, improve service?"},
        {"id": "C4", "text": "Would a text message the day before the reader's visit raise the share of meters read?"},
        {"id": "C5", "text": "Which mains are most likely to burst next summer?"},
        {"id": "C6", "text": "Why do customers distrust us?"},
        {"id": "C7", "text": "What share of bills in Al-Hamra were estimated this year?"},
        {"id": "C8", "text": "Did the move to smart meters in Al-Nakheel reduce water loss there, compared with similar districts?"},
    ],
    "constraint_change": {
        "from": "Nadia Al-Rubaie",
        "text": "Change of plan: the text-message budget is frozen until next year, and the board wants a decision on meter "
                "reading in ten business days. No new trial can run before then.",
        "affects": "C4",
    },
}
CLASSIFY_KEY = {
    "C1": ["descriptive", "description"], "C2": ["predictive", "predictive model"],
    "C3": ["causal", "causal analysis"], "C4": ["causal", "experiment"], "C5": ["predictive", "predictive model"],
    "C6": ["unanswerable", "no analysis"], "C7": ["descriptive", "description"], "C8": ["causal", "causal analysis"],
}
CLASSIFY_AFTER = {"C4": "no analysis"}

ROLES = {
    "sultana": {
        "name": "Sultana Al-Kanaan", "role": "customer service operations manager",
        "opening": "Repeat complaints are too high and the board keeps asking me about them.",
        "topics": [
            {"id": "target", "keys": ["target", "kpi", "bonus", "measure", "measured", "first-contact", "first contact", "incentive"],
             "answer": "Since month 13 the agents have a first-contact resolution target, and it counts towards their bonus.",
             "constraint": True},
            {"id": "privacy", "keys": ["recording", "recordings", "personal", "privacy", "data protection", "listen"],
             "answer": "We record calls, but I was told nobody may use the recordings for analysis without the data protection officer.",
             "constraint": True},
            {"id": "matching", "keys": ["same customer", "count", "counted", "identify", "match", "mobile", "how do you know", "link"],
             "answer": "The system links contacts by mobile number. When a customer calls from another phone, it is a new customer to us.",
             "constraint": True},
            {"id": "deadline", "keys": ["when", "deadline", "decide", "decision", "timeline", "contract", "by when"],
             "answer": "The outsourced call-centre contract is renewed in four weeks. I need to know before then whether to change its terms.",
             "constraint": True},
            {"id": "evidence", "keys": ["evidence", "convince", "trust", "believe", "proof", "would show", "survey"],
             "answer": "I trust repeat contacts within seven days. I do not trust the satisfaction survey: few people answer it.",
             "constraint": True},
            {"id": "affected", "keys": ["affected", "elderly", "groups", "who calls", "who is"],
             "answer": "Billing callers are most of the repeats. Older customers in Al-Hamra call the most about estimated bills."},
            {"id": "tried", "keys": ["tried", "before", "already", "done", "changed"],
             "answer": "We shortened the call script in month 13 to save time. Handling time fell a lot."},
        ],
    },
    "mamdouh": {
        "name": "Mamdouh Al-Qarawi", "role": "metering and leak-repair engineer",
        "opening": "Ask me anything about meters and repairs. The data are only as good as the process.",
        "topics": [
            {"id": "estimate", "keys": ["estimate", "estimated", "access", "cannot read", "reach", "locked", "no read"],
             "answer": "If the reader cannot reach the meter, the bill is an estimate: the average of the last three actual reads. "
                       "The next actual read corrects it.", "constraint": True},
            {"id": "cycle", "keys": ["cycle", "days", "route", "monthly", "period", "when read"],
             "answer": "Readers follow routes. A billing period runs from 27 to 35 days, so a 'monthly' bill is not a month of use.",
             "constraint": True},
            {"id": "meters", "keys": ["smart", "old", "age", "accuracy", "accurate", "under", "register", "replace"],
             "answer": "Old mechanical meters slow down: they miss roughly one and a half per cent more each year. "
                       "The smart meters in Al-Nakheel register what the old ones missed.", "constraint": True},
            {"id": "repairs", "keys": ["repair", "close", "closed", "job", "work order", "fix"],
             "answer": "Since the three-day target, crews close the job when they leave the site. If the leak comes back, "
                       "the job is reopened.", "constraint": True},
            {"id": "bulk", "keys": ["bulk", "input", "supply", "district meter", "flow meter"],
             "answer": "The Al-Wurud bulk meter was over-reading for a few months. It was recalibrated in month 13.", "constraint": True},
        ],
    },
    "azizah": {
        "name": "Azizah Al-Matrood", "role": "data protection officer",
        "opening": "Tell me what you want to use and why.",
        "topics": [
            {"id": "purpose", "keys": ["purpose", "why", "need", "necessary", "minimum"],
             "answer": "Use only the personal data the question needs. Counts of repeat contacts need no names.", "constraint": True},
            {"id": "recordings", "keys": ["recording", "recordings", "listen", "audio"],
             "answer": "Recordings are personal data collected to handle the call. A new use needs my review first.", "constraint": True},
            {"id": "class", "keys": ["classification", "classified", "restricted", "share", "sharing"],
             "answer": "The contact-centre extract is Restricted. It stays inside Ghadeer's environment.", "constraint": True},
        ],
    },
}

INVENTORY = {
    "deadline_business_days": 10,
    "analysis_days_needed": 4,
    "datasets": [
        {"id": "billing_reads", "name": "Billing reads", "holder": "Ghadeer", "owner": "Khalil Al-Sabhi",
         "classification": "Restricted", "history_months": 24, "access_business_days": 2,
         "personal_data": ["customer name", "mobile number", "national ID", "address"], "file": "reads.csv"},
        {"id": "bulk_supply", "name": "District bulk-meter input", "holder": "Ghadeer", "owner": "Mamdouh Al-Qarawi",
         "classification": "Restricted", "history_months": 24, "access_business_days": 1, "personal_data": [], "file": "supply.csv"},
        {"id": "repair_orders", "name": "Leak-repair work orders", "holder": "Ghadeer", "owner": "Mamdouh Al-Qarawi",
         "classification": "Restricted", "history_months": 24, "access_business_days": 1, "personal_data": [], "file": "repairs.csv"},
        {"id": "contacts", "name": "Contact-centre log", "holder": "Ghadeer", "owner": "Sultana Al-Kanaan",
         "classification": "Restricted", "history_months": 24, "access_business_days": 3,
         "personal_data": ["mobile number", "call recording"], "file": "contacts.csv"},
        {"id": "pipe_network", "name": "Pipe network (age, material, location)", "holder": "Ghadeer", "owner": "Network asset team",
         "classification": "Secret", "history_months": 0, "access_business_days": 8, "personal_data": [], "file": None},
        {"id": "smart_interval", "name": "Smart-meter hourly reads, Al-Nakheel", "holder": "Ghadeer", "owner": "Mamdouh Al-Qarawi",
         "classification": "Restricted", "history_months": 12, "access_business_days": 4,
         "personal_data": ["household consumption pattern"], "file": None},
        {"id": "roadworks", "name": "Road-works permits", "holder": "Regional Roads Office (another government entity)",
         "owner": "Regional Roads Office", "classification": "Restricted", "history_months": 36, "external": True,
         "sharing_assess_business_days": 10, "sharing_deliver_business_days": 5, "personal_data": [], "file": None},
        {"id": "weather", "name": "Daily temperature, open data", "holder": "Open data portal", "owner": "Open data publisher",
         "classification": "Public", "history_months": 60, "access_business_days": 0, "personal_data": [], "file": None},
    ],
}

CARD_14 = {
    "question": "Do road works near the mains explain the bursts in Al-Rawdah, and should next year's renewal budget go to "
                "the oldest mains there?",
    "decision_maker": "Nadia Al-Rubaie", "deadline_business_days": 10,
    "datasets_wanted": ["repair_orders", "pipe_network", "roadworks", "billing_reads", "weather"],
}

CARD_23 = {
    "decision": "Should Ghadeer extend active leak detection to Al-Rawdah and Al-Hamra next year?",
    "decision_maker": "Nadia Al-Rubaie, with the capital committee",
    "options": ["Extend to both districts", "Extend to Al-Rawdah only", "Do not extend; repair on customer reports as now"],
    "estimand": {
        "population": "District-months in the six districts, months 1 to 24",
        "variable": "Real losses as a share of system input (non-revenue water minus estimated apparent losses)",
        "contrast": "With active detection against without it",
        "intercurrent": "The Al-Wurud bulk-meter recalibration in month 13; read the months after it",
        "summary": "Difference in percentage points, Al-Wurud against the other districts, after against before",
    },
    "decision_rule": "Extend if real losses fall by at least 3 percentage points in Al-Wurud relative to the other districts",
    "affected": ["customers in districts with more interruptions during repairs", "repair crews", "the capital budget"],
    "personal_data_needed": False,
}

THREATS = [
    {"id": "selection", "name": "Selection", "question": "Were the units compared chosen in a way linked to the outcome?"},
    {"id": "regression_to_mean", "name": "Regression to the mean", "question": "Was the unit picked because it was extreme just before?"},
    {"id": "history", "name": "History", "question": "Did something else change at the same time?"},
    {"id": "measurement_change", "name": "Measurement change", "question": "Did the way the outcome is measured change?"},
    {"id": "seasonality", "name": "Seasonality", "question": "Do the periods compared differ by season?"},
    {"id": "construct_proxy", "name": "Construct: the proxy is gamed", "question": "Does the metric still mean what it meant?"},
    {"id": "missing_data", "name": "Missing or merged records", "question": "Are some events lost or merged in the data?"},
    {"id": "spillover", "name": "Spillover", "question": "Can the change in one unit affect the units compared with it?"},
    {"id": "forking_paths", "name": "Forking paths", "question": "Were analysis choices made after seeing the data?"},
    {"id": "small_sample", "name": "Small sample", "question": "Are there too few units or periods to tell signal from noise?"},
]

PLAN_A = """# Plan A (from a peer): did active leak detection work in Al-Wurud?

**Question.** Did active leak detection reduce non-revenue water in Al-Wurud?

**Data.** District bulk-meter input and billed volume, Al-Wurud only, months 10 to 15.

**Method.** Non-revenue water in months 10 to 12 (before detection started) against months 13 to 15 (after). Al-Wurud was
chosen for the pilot because it had the highest non-revenue water of the six districts in month 12.

**Result that would change the decision.** If non-revenue water falls by less than 3 points, do not extend.

**Threats.** The pilot ran in one district only.
"""

PLAN_B = """# Plan B (from a peer): did the first-contact target improve service?

**Question.** Did the first-contact resolution target improve service?

**Data.** Contact-centre log, months 7 to 18; the 'marked resolved' flag that agents set at the end of a call.

**Method.** First-contact resolution rate in months 7 to 12 against months 13 to 18. Repeat contacts are found by
linking contacts with the same mobile number.

**Result that would change the decision.** If the rate rises by 10 points or more, keep the target in the new contract.

**Threats.** Agents may differ in experience.
"""
PLAN_KEYS = {"A": ["regression_to_mean", "measurement_change", "history"], "B": ["construct_proxy", "history", "missing_data"]}

METRIC_TREE = {
    "goal": "Deliver water with little loss and good service",
    "nodes": [
        {"id": "nrw", "name": "Non-revenue water, % of system input", "parent": None, "kind": "outcome"},
        {"id": "real", "name": "Real losses (leaks)", "parent": "nrw", "kind": "driver"},
        {"id": "apparent", "name": "Apparent losses (meters, estimates, theft)", "parent": "nrw", "kind": "driver"},
        {"id": "repair_time", "name": "Median days from job creation to job closed", "parent": "real", "kind": "target",
         "target": "3 days or less, from month 13"},
        {"id": "leaks_found", "name": "Leaks found per month", "parent": "real", "kind": "activity"},
        {"id": "estimated_share", "name": "Share of bills estimated", "parent": "apparent", "kind": "driver"},
        {"id": "service", "name": "Customer service", "parent": None, "kind": "outcome"},
        {"id": "fcr", "name": "First-contact resolution, % of contacts marked resolved", "parent": "service", "kind": "target",
         "target": "85% or more, from month 13"},
        {"id": "aht", "name": "Average handling minutes", "parent": "service", "kind": "activity"},
    ],
}

BRIEFING = {
    "metering.md": """# Briefing: metering at Ghadeer

- Every account has a customer meter. Until month 12 all were mechanical. From month 13 the meters in Al-Nakheel were
  replaced by smart meters, which register low flows that mechanical meters miss.
- A mechanical meter slows with age. Ghadeer's own tests found that an old meter misses about 1.5% more of the water each
  year of service.
- Each district has a bulk meter at its inlet. Its reading is the district's system input. Bulk meters are recalibrated
  when a check shows drift.
- Non-revenue water is system input minus billed authorised consumption. It mixes real losses (leaks) and apparent
  losses (meter inaccuracy, billing data errors, unauthorised use).
""",
    "billing_cycles.md": """# Briefing: billing cycles

- Readers follow routes. The period between two reads runs from 27 to 35 days, depending on the route and staffing.
- The bill of a month is the consumption of the period that ended in that month, not of the calendar month.
- When the reader cannot reach a meter twice, the bill is an estimate: the average of the account's last three actual
  reads. The next actual read corrects the difference. Estimates do not follow the summer rise in use.
- Bills are issued to the account holder. The billing system holds the name, mobile number, national ID and address.
""",
    "leak_repair.md": """# Briefing: leak repair

- A leak is reported by a customer or found by a crew. The dispatcher creates a job; a crew visits; the job is closed.
- From month 13 the repair target is: job closed within three days of creation.
- If the leak is still running after closure, the job is reopened and a second visit fixes it.
- From month 13 Al-Wurud has active leak detection: crews with acoustic loggers search for leaks nobody reported. Those
  leaks are recorded with the source 'active_detection'.
""",
}

SHORT_NOTEBOOK = '''# Short analysis by Sabah Al-Huwaidi: "Where is customer service worst?"
# cell 1
contacts = U.csv("contacts")
year2 = contacts[contacts.month >= 13]
# cell 2
by_district = year2.groupby("district").size().sort_values(ascending=False)
print(by_district)
# cell 3
print("Al-Hamra (D4) has the most contacts, so it is where service is worst.")
print("Recommendation: move two agents to the Al-Hamra queue.")
'''
SHORT_REFERENCE = {"question_fit": 1, "data_handling": 1, "method": 0, "inference": 0, "communication": 0,
                   "notes": {"question_fit": "Answers 'most contacts', not 'worst service'.",
                             "data_handling": "Counts contacts, but districts have different numbers of accounts and access issues.",
                             "method": "No rate per account and no measure of service such as repeat contacts.",
                             "inference": "Volume of contacts read as quality of service.",
                             "communication": "The text names Al-Hamra as highest; the rerun shows Al-Salam (707) above Al-Hamra (705)."}}

SAREEA = {
    "prompt.md": """# The request Sabah gave the assistant Sareea

"Using reads.csv, tell me whether the smart meters in Al-Nakheel (D3) changed consumption. Compare months 1 to 12
with months 13 to 24. Give me a short summary for Nadia."
""",
    "notebook.py": '''# Notebook written by the assistant Sareea (as returned, not edited)
# cell s1
reads = U.csv("reads")
d3 = reads[reads.district == "D3"]
# cell s2
before = d3[d3.month <= 12]["consumption"].mean()
after = d3[d3.month >= 13]["consumption"].mean()
# cell s3
change = (after - before) / before * 100
print(f"Average monthly consumption before: {before:.1f} m3, after: {after:.1f} m3, change: {change:.1f}%")
''',
    "summary.md": """# Sareea's summary for Nadia (as returned)

The smart meters reduced consumption in Al-Nakheel by 8.2%. Average monthly consumption fell from 21.4 m3 to 19.6 m3
per account. This is well below the industry benchmark of 15% for meter replacement programmes, so the programme is
performing as expected and can be rolled out to the other districts.
""",
}

WEAK_NOTES = [
    {"id": "N1", "text": "The join looks off."},
    {"id": "N2", "text": "Chart is ugly, please fix."},
    {"id": "N3", "text": "Is this significant?"},
    {"id": "N4", "text": "Use a better method."},
    {"id": "N5", "text": "Typo in the title: 'Wurud' is spelt two ways."},
    {"id": "N6", "text": "Where is the 15% from?"},
    {"id": "N7", "text": "What about estimated reads?"},
    {"id": "N8", "text": "Wrong question?"},
]
NOTE_SEVERITY = {"N8": "critical", "N4": "critical", "N1": "major", "N6": "major", "N7": "major", "N3": "major",
                 "N2": "minor", "N5": "minor"}

# ---------------------------------------------------------------------------------------------- the seeded-flaw review (Lab 3.2)
FLAWS = {
    "F1": {"area": "question_fit", "severity": "critical", "cell": "c4",
           "what": "Success is measured as leaks found, not as water lost"},
    "F2": {"area": "data_handling", "severity": "major", "cell": "c2",
           "what": "Repairs are joined on the district name, and 'Al Wurud' rows are dropped"},
    "F3": {"area": "method", "severity": "critical", "cell": "c3",
           "what": "Before-after in Al-Wurud only, months 10 to 12 against 13 to 15, no comparison districts"},
    "F4": {"area": "inference", "severity": "major", "cell": "c5",
           "what": "A fall over three months each side is called significant with no interval"},
    "F5": {"area": "data_handling", "severity": "minor", "cell": "c1",
           "what": "Billed volume is not adjusted for billing-cycle length"},
    "F6": {"area": "communication", "severity": "minor", "cell": "c6",
           "what": "The chart's axis starts at 20%, which magnifies the fall"},
    "F7": {"area": "data_handling", "severity": "major", "cell": "c1",
           "what": "Estimated reads are dropped from billed volume, which inflates non-revenue water"},
}


def variant_flaws(variant: int) -> list[str]:
    if variant == 0:
        return ["F1", "F2", "F3", "F6"]
    r = random.Random(SEED * 1000 + variant)
    crit = r.choice(["F1", "F3"])
    rest = r.sample([f for f in FLAWS if f != crit], 3)
    return sorted([crit] + rest)


# ---------------------------------------------------------------------------------------------- capstone: Hima Municipality
def make_permits(rng: random.Random) -> list[dict]:
    rows = []
    kinds = [("new_building", 0.45), ("extension", 0.30), ("fit_out", 0.25)]
    for i in range(3600):
        week = rng.randint(1, 52)
        kind = rng.choices([k for k, _ in kinds], [w for _, w in kinds])[0]
        complete = rng.random() < (0.55 if week >= 27 else 0.75)  # the online form from week 27 lets incomplete files in
        review_days = rng.randint(5, 20) + (8 if week >= 27 else 0) + (6 if kind == "new_building" else 0)
        returns = 0 if complete else rng.choice([1, 1, 2])
        submitted = (week - 1) * 7 + rng.randint(0, 6)
        decided = submitted + review_days + returns * rng.randint(6, 14)
        status = "decided" if decided <= 364 else "open"
        rows.append({"application": f"P-{i + 1:05d}", "week": week, "kind": kind, "channel": "online" if week >= 27 else "counter",
                     "complete_on_submission": int(complete), "returns_for_missing_documents": returns,
                     "submitted_day": submitted, "decided_day": decided if status == "decided" else "", "status": status})
    return rows


CAP_BRIEF = """# Capstone brief: Hima Municipality, Building Permits Department

Fahda Al-Bishr, director of permits, wrote:

> "The backlog of building permits has doubled since we moved applications online. The council wants a plan. Should we hire
> six more plan reviewers? Tell me what to do."

Daifallah Al-Juaid, head of the plan-review section, adds that many online applications arrive without the documents the
reviewers need, and that files are returned to applicants, sometimes twice.

Your materials: `permits.csv` (3,600 synthetic applications of one year), `inventory.json` (what data exist, who holds
them, how long they take), and `review/backlog_analysis.py`, an analysis drafted with an assistant by a colleague. All
data is synthetic.

You hand in (a public GitHub repository): the framing card, an analysis plan of at most two pages, and review notes on
the supplied analysis ranked by consequence. You present for eight minutes; during the talk the sponsor changes one
constraint, and you defend your recommendation for ten minutes.
"""
CAP_INVENTORY = {
    "deadline_business_days": 10,
    "datasets": [
        {"id": "permits", "name": "Permit applications and decisions", "holder": "Hima Municipality", "classification": "Restricted",
         "access_business_days": 1, "personal_data": ["applicant name", "national ID", "plot address"], "file": "permits.csv"},
        {"id": "reviewer_rota", "name": "Plan reviewers' rota and leave", "holder": "Hima Municipality", "classification": "Restricted",
         "access_business_days": 3, "personal_data": ["employee names"], "file": None},
        {"id": "civil_defence", "name": "Civil-defence approvals", "holder": "another government entity", "classification": "Restricted",
         "external": True, "sharing_assess_business_days": 10, "sharing_deliver_business_days": 5, "personal_data": [], "file": None},
    ],
}
CAP_ANALYSIS = '''# Backlog analysis drafted with an assistant by a colleague (as handed over)
# cell b1
permits = pd.read_csv("permits.csv")
# cell b2
permits["days_to_decision"] = permits.decided_day - permits.submitted_day
# cell b3
by_half = permits.groupby(permits.week >= 27)["days_to_decision"].mean()
print(by_half)
# cell b4
print("Decisions take longer since week 27 because reviewers are too few: hire six reviewers.")
'''
CAP_PRACTICE_CHANGE = """# A practice constraint change (the one used in the defence is different and unseen)

"The council has frozen hiring for this year. Whatever you recommend must work with the reviewers we have."
"""


# ---------------------------------------------------------------------------------------------- reference results
REF_INTERVIEW = {
    "map": {"decides": ["Sultana Al-Kanaan, with Nadia Al-Rubaie for the call-centre contract"],
            "uses": ["Contact-centre team leaders", "The outsourced call-centre supplier"],
            "affected": ["Customers who call again", "Agents whose bonus depends on the target"]},
    "questions": [
        "What decision do you need to take about repeat complaints, and by when?",
        "How do you count a repeat contact today: how do you know it is the same customer?",
        "What evidence would convince you that a change worked, and what would you not trust?",
        "Which targets or incentives do the agents work under at the moment?",
        "What has changed in the contact centre in the last year that might matter?",
        "Which data about calls can we use, and what about the call recordings and personal data?",
    ],
    "record": {
        "decision": "Whether to change the terms of the outsourced call-centre contract, renewed in four weeks",
        "constraints": ["Decision needed within four weeks", "First-contact target counts towards bonuses since month 13",
                        "Contacts are linked by mobile number", "Recordings need the data protection officer's review"],
        "acceptable_evidence": ["Repeat contacts within seven days"],
        "heard": ["The call script was shortened in month 13"],
        "assumed": ["That repeat contacts rose after month 13: not yet checked"],
    },
}
REF_NOTES = [
    {"id": "N8", "problem": "Cell c4 measures success as leaks found, which rose 3.4 times, not as water lost",
     "consequence": "The recommendation to buy loggers rests on activity; measured on water, the effect is 2.3 points and the decision is not to buy",
     "fix": "Report the change in non-revenue water against the other districts as the headline, and leaks found as context"},
    {"id": "N4", "problem": "Cell c3 compares Al-Wurud's months 10 to 12 with 13 to 15, with no comparison districts",
     "consequence": "The bulk-meter drift and regression to the mean add about 1.8 points, enough to cross the 3-point rule and reverse the decision",
     "fix": "Use months 1 to 9 against 15 to 24, bills rescaled to 30 days, against the other districts without Al-Nakheel"},
    {"id": "N6", "problem": "Sareea's summary cites an industry benchmark of 15% with no source",
     "consequence": "A number nobody can verify becomes the reason to roll out meters; the decision would rest on it",
     "fix": "Remove the benchmark, or replace it with a sourced figure and its reference"},
    {"id": "N7", "problem": "Sareea's analysis treats estimated bills in Al-Nakheel as actual reads",
     "consequence": "Estimates repeat past reads, so the before-after mixes billing timing with metering and the 11.5% rise is overstated or understated",
     "fix": "Recompute on actual reads only and report the share of estimates beside the result"},
    {"id": "N1", "problem": "Cell c2 joins repairs on the district name, and rows spelt 'Al Wurud' are dropped",
     "consequence": "About a third of Al-Wurud's repairs vanish from the leaks-found count, so any count-based claim is wrong",
     "fix": "Normalise the spelling or join on a district code, and assert the row count before and after the join"},
    {"id": "N3", "problem": "Sareea's summary states the fall as a fact with no interval or check of noise",
     "consequence": "The reader cannot tell a real change from month-to-month swing, so the claim looks more certain than it is",
     "fix": "Report an interval, as the corrected analysis does (1.4 to 3.3 points), and say what it means for the rule"},
    {"id": "N2", "problem": "The chart in cell c6 starts its axis at 20%, which makes a small fall look steep",
     "consequence": "The picture overstates the change for readers who look at the chart rather than the number in the text",
     "fix": "Start the axis at zero, or mark the axis break clearly and print the change on the chart"},
    {"id": "N5", "problem": "The repairs export spells the district as both 'Al Wurud' and 'Al-Wurud'",
     "consequence": "Cosmetic in the report itself, but it is the cause of the dropped rows of note N1",
     "fix": "Ask the export owner to use one spelling, and keep the join on the district code"},
]

REF_SCOPED = {
    "question": "Have bursts in Al-Rawdah become more frequent over 24 months, and do they follow summer temperatures, "
                "enough to justify a mains-renewal study next year?",
    "kind": "descriptive", "datasets": ["repair_orders", "weather"],
    "left_unanswered": "Whether road works or pipe age cause the bursts",
    "request_now": ["Road-works permits through a data-sharing request", "Pipe-network extract through the security approval"],
}


def references(accounts, reads, supply, repairs, contacts) -> dict:
    """Results the labs compute, written so that a cell after a skipped exercise can still run."""
    ref = {}
    billed = {}
    est = {}
    for r in reads:
        k = (r["district"], r["month"])
        billed[k] = billed.get(k, 0.0) + r["billed_m3"]
        est.setdefault(r["district"], [0, 0])
        est[r["district"]][0] += r["read_type"] == "estimated"
        est[r["district"]][1] += 1
    nrw = {}
    for s in supply:
        k = (s["district"], s["month"])
        nrw[k] = 100 * (s["system_input_m3"] - billed[k]) / s["system_input_m3"]
    ref["nrw_last12"] = {d: round(sum(nrw[(d, m)] for m in range(13, 25)) / 12, 1) for d, _, _ in DISTRICTS}
    ref["estimated_share"] = {d: round(100 * a / b, 1) for d, (a, b) in est.items()}
    ref["nrw_by_month"] = {d: [round(nrw[(d, m)], 2) for m in range(1, 25)] for d, _, _ in DISTRICTS}

    def med(xs):
        xs = sorted(xs)
        n = len(xs)
        return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2

    pre = [r for r in repairs if r["month"] < TARGET_MONTH]
    post = [r for r in repairs if r["month"] >= TARGET_MONTH]
    ref["repair"] = {
        "median_close_before": med([r["closed_day"] - r["job_created_day"] for r in pre]),
        "median_close_after": med([r["closed_day"] - r["job_created_day"] for r in post]),
        "reopen_before": round(100 * sum(r["reopened"] for r in pre) / len(pre), 1),
        "reopen_after": round(100 * sum(r["reopened"] for r in post) / len(post), 1),
        "median_report_to_fix_before": med([r["final_fix_day"] - r["reported_day"] for r in pre]),
        "median_report_to_fix_after": med([r["final_fix_day"] - r["reported_day"] for r in post]),
    }
    return ref


def main():
    rng = random.Random(SEED)
    accounts = make_accounts(rng)
    cyc = cycle_days(rng)
    reads, true_use = make_reads(rng, accounts, cyc)
    supply = make_supply(rng, true_use)
    repairs = make_repairs(rng)
    contacts = make_contacts(rng, accounts)

    write_csv(DATA / "accounts.csv", [{k: v for k, v in a.items() if not k.startswith("_")} for a in accounts])
    write_csv(DATA / "reads.csv", reads)
    write_csv(DATA / "supply.csv", supply)
    write_csv(DATA / "repairs.csv", repairs)
    write_csv(DATA / "contacts.csv", contacts)
    write_json(DATA / "requests.json", REQUESTS)
    write_json(DATA / "roles.json", ROLES)
    write_json(DATA / "inventory.json", INVENTORY)
    write_json(DATA / "card_1_4.json", CARD_14)
    write_json(DATA / "card_2_3.json", CARD_23)
    write_json(DATA / "threats.json", THREATS)
    write_json(DATA / "metric_tree.json", METRIC_TREE)
    write_json(DATA / "weak_notes.json", WEAK_NOTES)
    write_text(DATA / "plans" / "plan_A.md", PLAN_A)
    write_text(DATA / "plans" / "plan_B.md", PLAN_B)
    for name, text in BRIEFING.items():
        write_text(DATA / "briefing" / name, text)
    write_text(DATA / "review" / "short_complaints.py", SHORT_NOTEBOOK)
    for name, text in SAREEA.items():
        write_text(DATA / "review" / "sareea" / name, text)
    write_json(DATA / "review" / "flaws.json", {k: {"area": v["area"], "cell": v["cell"]} for k, v in FLAWS.items()})
    # Lab 3.2: a hash of each variant's flaw set, so a participant can check flags without seeing the key
    write_json(DATA / "review" / "variant_hashes.json",
               {str(v): digest("ds310", v, ",".join(variant_flaws(v))) for v in range(0, 41)})

    ref = references(accounts, reads, supply, repairs, contacts)
    R = DATA / "reference"
    write_json(R / "numbers.json", ref)
    write_json(R / "classify.json", {"key": CLASSIFY_KEY, "after_change": CLASSIFY_AFTER})
    write_json(R / "plan_threats.json", PLAN_KEYS)
    write_json(R / "short_scores.json", SHORT_REFERENCE)
    write_json(R / "note_severity.json", NOTE_SEVERITY)
    write_json(R / "card_2_3.json", CARD_23)
    write_json(R / "interview.json", REF_INTERVIEW)
    write_json(R / "scoped.json", REF_SCOPED)
    write_json(R / "review_notes.json", REF_NOTES)

    write_text(CAP.parent / "BRIEF.md", CAP_BRIEF)
    write_csv(CAP / "permits.csv", make_permits(random.Random(SEED + 1)))
    write_json(CAP / "inventory.json", CAP_INVENTORY)
    write_text(CAP / "review" / "backlog_analysis.py", CAP_ANALYSIS)
    write_text(CAP / "practice_constraint_change.md", CAP_PRACTICE_CHANGE)

    # the trainer's variant table for Lab 3.2 (never published in a trainee build)
    sol = ROOT / "solutions"
    sol.mkdir(exist_ok=True)
    write_json(sol / "flaw_variants.json", {"flaws": FLAWS, "variants": {str(v): variant_flaws(v) for v in range(0, 41)}})
    print("wrote", sum(1 for _ in DATA.rglob("*") if _.is_file()), "files in data/ and the capstone data")
    print("NRW last 12 months by district:", ref["nrw_last12"])
    print("estimated share:", ref["estimated_share"])
    print("repair:", ref["repair"])


if __name__ == "__main__":
    main()
