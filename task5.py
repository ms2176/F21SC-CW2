from load import load_data
from collections import defaultdict


visitors_cache = {}
documents_cache = {}

def return_visitors(document_uuid, file_path):
    if document_uuid in visitors_cache:
        return visitors_cache[document_uuid]

    visitors = set()

    for record in load_data(file_path):
        # Must be a document event
        if record.get("subject_type") != "doc":
            continue

        # Must match the target doc
        if record.get("subject_doc_id") == document_uuid:
            visitors.add(record.get("visitor_uuid"))

    visitors_cache[document_uuid] = visitors
    return visitors


def return_documents(visitor_uuid, file_path):
    if visitor_uuid in documents_cache:
        return documents_cache[visitor_uuid]

    docs = set()

    for record in load_data(file_path):
        # Only count events that have a document
        if record.get("subject_type") != "doc":
            continue

        # Check visitor match
        if record.get("visitor_uuid") == visitor_uuid:
            doc_id = record.get("subject_doc_id")
            if doc_id:            # filter out None
                docs.add(doc_id)

    documents_cache[visitor_uuid] = docs
    return docs

def sort_by_shared_readers(doc_counter):
    # Convert dict to list of tuples (doc_id, count)
    doc_items = list(doc_counter.items())
    
    # Sort using Python's sorted internally
    sorted_docs = sorted(doc_items, key=lambda x: x[1], reverse=True)
    
    # Return only document UUIDs in sorted order
    sorted_list = [doc[0] for doc in sorted_docs]
    
    return sorted_list


def also_likes(document_uuid, file_path, sort_func):
    visitors = return_visitors(document_uuid, file_path)
    doc_counter = defaultdict(int)

    for visitor in visitors:
        docs = return_documents(visitor, file_path)
        for doc in docs:
            if doc and doc != document_uuid:  # ignore None
                doc_counter[doc] += 1

    sorted_docs = sort_func(doc_counter)
    
    return sorted_docs[:10]

def run_task_5d(file_path, document_uuid):
    top10 = also_likes(document_uuid, file_path, sort_by_shared_readers)
    if not top10:
        message = "No related documents found for this document."
        print(message)  
        return message
    print(f"Top 10 also-like documents for {document_uuid}:")
    for doc in top10:
        print(doc)
    return top10


# if __name__ == "__main__":
#     file_path = "issuu_cw2.json"
#     doc_id = "130810070956-4f21f422b9c8a4ffd5f62fdadf1dbee8"

#     top10 = also_likes(doc_id, file_path, sort_by_shared_readers)
#     print(top10)
     
   