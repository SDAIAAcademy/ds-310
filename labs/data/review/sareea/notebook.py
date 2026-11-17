# Notebook written by the assistant Sareea (as returned, not edited)
# cell s1
reads = U.csv("reads")
d3 = reads[reads.district == "D3"]
# cell s2
before = d3[d3.month <= 12]["consumption"].mean()
after = d3[d3.month >= 13]["consumption"].mean()
# cell s3
change = (after - before) / before * 100
print(f"Average monthly consumption before: {before:.1f} m3, after: {after:.1f} m3, change: {change:.1f}%")
