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
    try:
        counter = count_user_agents(filepath)
    except Exception:
        print(f"Error processing file: {filepath}")
        return f"Error processing file: {filepath}"
    
    if not counter:
            print(f"No data found for user agents in file: {filepath}")
            return f"No data found for user agents in file: {filepath}"

    plot_histogram(
        counter=counter,
        title="Viewer distribution by user agent",
        xlabel="User Agent"

    )
    return True

# Runs Task 3b: Viewer distribution by main browser histogram
def run_task_3b(filepath):
    try:
        counter = count_main_browsers(filepath)
    except Exception:
        print(f"Error processing file: {filepath}")
        return f"Error processing file: {filepath}"

    if not counter:
        print(f"No data found for main browsers in file: {filepath}")
        return f"No data found for main browsers in file: {filepath}"

    plot_histogram(
        counter=counter,
        title="Viewer distribution by main browser",
        xlabel="Main Browser"
    )
    return True