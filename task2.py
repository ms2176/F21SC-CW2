from collections import Counter
from load import load_data
from histogram import plot_histogram
import pycountry_convert as cc

# Get country counts for a specific document
def get_country_counts_2a(file_path, document_uuid):
    return Counter(
        record.get("visitor_country", "Unknown")
        for record in load_data(file_path)
        if record.get("subject_doc_id") == document_uuid
    )

# Get continent from country code
def get_continent_from_country_2b(country_code):
    if not country_code or country_code == "Unknown":
        return "Unknown"
    try:
        continent_code = cc.country_alpha2_to_continent_code(country_code) # Convert country code to continent code
        continent_name = cc.convert_continent_code_to_continent_name(continent_code) # Convert continent code to continent name
        return continent_name
    except Exception: # Catch any conversion errors
        return "Unknown"

# Get continent counts based on country counts
def get_continent_counts_2b(country_counter):
    cont_counter = Counter() 
    for country_code, count in country_counter.items(): # Iterate through country counts
        continent = get_continent_from_country_2b(country_code) # Get continent name
        cont_counter[continent] += count # Aggregate counts by continent
    return cont_counter

# Runs Task 2a: Viewer distribution by country histogram
def run_task_2a(file_path, document_uuid):
    country_counter = get_country_counts_2a(file_path, document_uuid)
    if not country_counter:
        return None
    
    plot_histogram(
        counter=country_counter,
        title=f"Viewer distribution by country for {document_uuid}",
        xlabel="Country"
    )
    return True

# Runs Task 2b: Viewer distribution by continent histogram
def run_task_2b(file_path, document_uuid):
    country_counter = get_country_counts_2a(file_path, document_uuid)
    if not country_counter:
        return None

    continent_counter = get_continent_counts_2b(country_counter)

    plot_histogram(
        counter=continent_counter,
        title=f"Viewer distribution by continent for {document_uuid}",
        xlabel="Continent"
    )
    return True

# Test runs
# if __name__ == "__main__":
#     file_path = "issuu_cw2.json"
#     doc_id = "140227140914-9ebad8b641c3754defdd0aa4bdd3aa09"

#     print("Running Task 2a...")
#     run_task_2a(file_path, doc_id)

#     print("Running Task 2b...")
#     run_task_2b(file_path, doc_id)
