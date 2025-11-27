from collections import Counter
import re
from histogram import plot_histogram
from load import load_data

# Count user agents from the file
def count_user_agents(filepath):
    return Counter(
        r.get("visitor_useragent", "Unknown")
        for r in load_data(filepath)
    )

# Extract main browser from user agent string
def get_main_browser(useragent):
    match = re.match(r'([^\s/]+)', useragent) # Match the first word before a space or slash
    return match.group(1) if match else "Other" # Return "Other" if no match found

# Count main browsers from the file
def count_main_browsers(filepath):
    return Counter(
        get_main_browser(r.get("visitor_useragent", "Unknown"))
        for r in load_data(filepath)
    )

# Runs Task 3a: Viewer distribution by user agent histogram
def run_task_3a(filepath):
    counter = count_user_agents(filepath)
    if not counter:
        return None

    plot_histogram(
        counter=counter,
        title="Viewer distribution by user agent",
        xlabel="User Agent"

    )
    return True

# Runs Task 3b: Viewer distribution by main browser histogram
def run_task_3b(filepath):
    counter = count_main_browsers(filepath)
    if not counter:
        return None

    plot_histogram(
        counter=counter,
        title="Viewer distribution by main browser",
        xlabel="Main Browser"
    )
    return True