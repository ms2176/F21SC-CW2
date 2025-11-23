import json
from collections import defaultdict
import matplotlib.pyplot as plt
from continent import continent_lookup  # your dictionary of country -> continent
import re

# loading json
records = []
with open("issuu_cw2.json", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            records.append(json.loads(line))

user_readtime = defaultdict(int)

for r in records:
    user = r.get("visitor_uuid")
    readtime = r.get("event_readtime")
    if user and readtime:
        user_readtime[user] += readtime

top_readers = sorted(user_readtime.items(), key=lambda x: x[1], reverse=True)[:10]

print("Top 10 readers by total reading time:")
print("{:<20} {:>10}".format("Visitor UUID", "Total Event Read Time"))
for user, total_time in top_readers:
    print(f"{user:<20} {total_time:>10}")
