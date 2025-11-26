from collections import defaultdict
from load import load_data


def run_task_4(file_path, document_uuid=None, top_n=10):
    user_readtime = defaultdict(int)

    for r in load_data(file_path):
        if document_uuid is not None and r.get("subject_doc_id") != document_uuid:
            continue

        user = r.get("visitor_uuid")
        readtime = r.get("event_readtime")

        if user and readtime:
            user_readtime[user] += readtime

    top_readers = sorted(user_readtime.items(), key=lambda x: x[1], reverse=True)[:top_n]

    if not top_readers:
        print("No records found for this document.")
        return None

    print(f"Top {top_n} readers by total reading time"
          + (f" for {document_uuid}:" if document_uuid else ":"))
    print("{:<20} {:>10}".format("Visitor UUID", "Total Read Time"))

    for user, total_time in top_readers:
        print(f"{user:<20} {total_time:>10}")

    return top_readers
