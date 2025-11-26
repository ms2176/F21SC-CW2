from collections import Counter
import re
from histogram import plot_histogram
from load import load_data

def count_user_agents(filepath, document_uuid=None):
    return Counter(r.get("visitor_useragent", "Unknown")
                   for r in load_data(filepath)
                   if document_uuid is None or r.get("subject_doc_id") == document_uuid)


def get_main_browser(useragent):
    if not useragent:
        return "Unknown"
    match = re.match(r'([^\s/]+)', useragent)
    return match.group(1)

# count main browsers
def count_main_browsers(filepath, document_uuid=None):
    return Counter(get_main_browser(r.get("visitor_useragent")) for r in load_data(filepath)
                   if document_uuid is None or r.get("subject_doc_id") == document_uuid)


def run_task_3a(filepath, document_uuid=None):
    counter = count_user_agents(filepath, document_uuid)
    if not counter:
        return None

    plot_histogram(
        counter=counter,
        title="Viewer distribution by user agent" + (f" for {document_uuid}" if document_uuid else ""),
        xlabel="User Agent"
    )
    return True


def run_task_3b(filepath, document_uuid=None):
    counter = count_main_browsers(filepath, document_uuid)
    if not counter:
        return None

    plot_histogram(
        counter=counter,
        title="Viewer distribution by main browser" + (f" for {document_uuid}" if document_uuid else ""),
        xlabel="Main Browser"
    )
    return True