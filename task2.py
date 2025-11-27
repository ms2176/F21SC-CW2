from collections import Counter
from load import load_data
from histogram import plot_histogram
import pycountry_convert as cc

def get_country_counts_2a(file_path, document_uuid):
    return Counter(
        record.get("visitor_country", "Unknown")
        for record in load_data(file_path)
        if record.get("subject_doc_id") == document_uuid
    )

def get_continent_from_country_2b(country_code):
    if not country_code or country_code == "Unknown":
        return "Unknown"
    try:
        continent_code = cc.country_alpha2_to_continent_code(country_code)
        continent_name = cc.convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except Exception:
        return "Unknown"

def get_continent_counts_2b(country_counter):
    cont_counter = Counter()
    for country_code, count in country_counter.items():
        continent = get_continent_from_country_2b(country_code)
        cont_counter[continent] += count
    return cont_counter

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
