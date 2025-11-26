import os
import sys
import matplotlib.pyplot as plt
from load import load_data
from collections import Counter
from continent import continent_lookup 
from histogram import plot_histogram

def get_country_counts_2a(file_path, document_uuid):
    return Counter(
        record.get("visitor_country", "Unknown")
        for record in load_data(file_path)
        if record.get("subject_doc_id") == document_uuid
    )

def get_continent_counts_2b(country_counter, continent_map):
    cont_counter = Counter()

    for country, count in country_counter.items():
        continent = continent_map.get(country, "Unknown")
        cont_counter[continent] += count

    return cont_counter

if __name__ == "__main__":

    file = "issuu_cw2.json"              
    doc = input("Enter document UUID: ") 

  
    country_counter = get_country_counts_2a(file, doc)
    if not country_counter:
        print("No records found for this document.")
        exit()

    plot_histogram(
        counter=country_counter,
        title=f"Viewer distribution by country for {doc}",
        xlabel="Country"
    )
    
    continent_counter = get_continent_counts_2b(country_counter, continent_lookup)

    plot_histogram(
        counter=continent_counter,
        title=f"Viewer distribution by continent for {doc}",
        xlabel="Continent"
    )