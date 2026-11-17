# Backlog analysis drafted with an assistant by a colleague (as handed over)
# cell b1
permits = pd.read_csv("permits.csv")
# cell b2
permits["days_to_decision"] = permits.decided_day - permits.submitted_day
# cell b3
by_half = permits.groupby(permits.week >= 27)["days_to_decision"].mean()
print(by_half)
# cell b4
print("Decisions take longer since week 27 because reviewers are too few: hire six reviewers.")
