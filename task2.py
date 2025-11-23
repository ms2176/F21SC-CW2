import json
from collections import Counter
import matplotlib.pyplot as plt
from continent import continent_lookup  # your dictionary of country -> continent

# loading json
records = []
with open("issuu_cw2.json", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            records.append(json.loads(line))

# user input for doc_uuid
target = input("Enter subject_doc_id: ")

filtering = [r for r in records if r.get("subject_doc_id") == target]

if not filtering:
    print("No records found for this document.")
    exit()

# histogram by country
country_counts = Counter(r.get("visitor_country") for r in filtering)

plt.figure(figsize=(10, 5))
plt.bar(country_counts.keys(), country_counts.values())
plt.xlabel("Country")
plt.ylabel("Viewer count")
plt.title(f"Viewer distribution by country for {target}")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# histogram by continent
continent_counts = Counter()
for r in filtering:
    country = r.get("visitor_country")
    continent = continent_lookup.get(country, "Unknown")
    continent_counts[continent] += 1 # 

plt.figure(figsize=(10, 5))
plt.bar(continent_counts.keys(), continent_counts.values())
plt.xlabel("Continent")
plt.ylabel("Viewer count")
plt.title(f"Viewer distribution by continent for {target}")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()