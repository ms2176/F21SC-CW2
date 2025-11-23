import json
from collections import Counter
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

# histogram taska
useragents = Counter(r.get("visitor_useragent") for r in records)

plt.figure(figsize=(10, 5))
plt.bar(useragents.keys(), useragents.values())
plt.xlabel("User Agent")
plt.ylabel("Viewer count")
plt.title(f"Viewer distribution by User Agent")
plt.xticks(rotation=0)
plt.show()

#task b
def get_main_browser(useragent):
    if not useragent:
        return "Unknown"
    match = re.match(r'([^\s/]+)', useragent)
    return match.group(1)

# count main browsers
main_browsers = Counter(get_main_browser(r.get("visitor_useragent")) for r in records)

plt.figure(figsize=(10, 5))
plt.bar(main_browsers.keys(), main_browsers.values())
plt.xlabel("Browser")
plt.ylabel("Viewer count")
plt.title("Viewer distribution by main browser")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()