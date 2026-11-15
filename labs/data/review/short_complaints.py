# Short analysis by Sabah Al-Huwaidi: "Where is customer service worst?"
# cell 1
contacts = U.csv("contacts")
year2 = contacts[contacts.month >= 13]
# cell 2
by_district = year2.groupby("district").size().sort_values(ascending=False)
print(by_district)
# cell 3
print("Al-Hamra (D4) has the most contacts, so it is where service is worst.")
print("Recommendation: move two agents to the Al-Hamra queue.")
