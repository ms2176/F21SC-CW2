# task2.py
from collections import Counter
from load import load_data
from continent import continent_lookup
from histogram import plot_histogram


def get_country_counts_2a(file_path, document_uuid):
    return Counter(
        record.get("visitor_country", "Unknown")
        for record in load_data(file_path)
        if record.get("subject_doc_id") == document_uuid
    )


def get_continent_counts_2b(country_counter):
    cont_counter = Counter()
    for country, count in country_counter.items():
        continent = continent_lookup.get(country, "Unknown")
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