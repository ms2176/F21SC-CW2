from collections import defaultdict
import os
import subprocess

from task5 import return_visitors, return_documents, also_likes, sort_by_shared_readers


def generate_dot_graph(input_doc, input_visitor, file_path, sort_func):
    """
    Build a DOT graph for the 'also likes' relationship around a given document.
    """
    visitors = return_visitors(input_doc, file_path)
    also_docs = also_likes(input_doc, file_path, sort_func)

    # Convert "no related docs" message to empty list
    if isinstance(also_docs, str):
        also_docs = []

    # Convert to set for O(1) lookup
    also_docs_set = set(also_docs)

    # Find readers who connect input_doc to also-like docs
    # AND track which also-like docs each reader has read
    linking_readers = set()
    doc_to_readers = defaultdict(set)

    for v in visitors:
        docs = return_documents(v, file_path)
        # Only consider documents that are in the also-like list
        for d in docs:
            if d in also_docs_set:
                linking_readers.add(v)
                doc_to_readers[d].add(v)

    dot = []
    dot.append("digraph AlsoLikesGraph {")
    dot.append("  rankdir=TB;")

    short_doc = input_doc[-4:]
    short_visitor = input_visitor[-4:] if input_visitor else None

    # --- NODES ---

    # Input document (green circle)
    dot.append(f'  "{short_doc}" [shape=circle, style=filled, fillcolor=lightgreen];')

    # Only linking readers who connect to also-like docs (white boxes)
    # Plus the input visitor if they're a reader (green box)
    for r in linking_readers:
        short_r = r[-4:]
        if short_visitor and short_r == short_visitor:
            fill = "lightgreen"
        else:
            fill = "white"
        dot.append(f'  "{short_r}" [shape=box, style=filled, fillcolor="{fill}"];')

    # If input visitor is in visitors but NOT a linking reader, still show them
    if input_visitor and input_visitor in visitors and input_visitor not in linking_readers:
        dot.append(f'  "{short_visitor}" [shape=box, style=filled, fillcolor="lightgreen"];')

    # Also-like documents (white circles)
    for d in also_docs:
        dot.append(f'  "{d[-4:]}" [shape=circle, style=filled, fillcolor=white];')

    # --- EDGES ---

    # Linking readers → input document
    for r in linking_readers:
        dot.append(f'  "{r[-4:]}" -> "{short_doc}";')

    # Input visitor → input document (if not already a linking reader)
    if input_visitor and input_visitor in visitors and input_visitor not in linking_readers:
        dot.append(f'  "{short_visitor}" -> "{short_doc}";')

    # Linking readers → also-like documents they've read
    for doc, readers in doc_to_readers.items():
        short_d = doc[-4:]
        for r in readers:
            dot.append(f'  "{r[-4:]}" -> "{short_d}";')

    dot.append("}")

    # Save DOT file
    dot_path = "also_likes.dot"
    with open(dot_path, "w") as f:
        f.write("\n".join(dot))

    print("DOT file generated:", os.path.abspath(dot_path))
    return dot_path


def run_task_6(file_path, document_uuid, visitor_uuid=None):

    # If a visitor id was supplied, check they actually read the document
    if visitor_uuid:
        visitors_of_doc = return_visitors(document_uuid, file_path)
        if visitor_uuid not in visitors_of_doc:
            # Visitor did not read this doc — inform caller (GUI prints message)
            return (
                f"Visitor {visitor_uuid} does not appear in the reader list for "
                f"document {document_uuid}. Graph not generated."
            )
        
    dot_path = generate_dot_graph(
        document_uuid, visitor_uuid, file_path, sort_by_shared_readers
    )

    png_path = os.path.splitext(dot_path)[0] + ".png"

    # Try to call Graphviz 'dot' to create a PNG image
    try:
        subprocess.run(
            ["dot", "-Tpng", dot_path, "-o", png_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        # If conversion fails, surface a clear error to the caller
        raise RuntimeError(
            "Failed to convert DOT to PNG. "
            "Make sure Graphviz is installed and 'dot' is on your PATH."
        ) from exc

    if not os.path.exists(png_path):
        raise RuntimeError("PNG file was not created.")

    print("PNG graph generated:", os.path.abspath(png_path))
    return png_path


# if __name__ == "__main__":
#     file_path = "issuu_cw2.json"
#     doc_id = "140227140914-9ebad8b641c3754defdd0aa4bdd3aa09"
#     visitor_id = "6262b769706ad29d"
#     run_task_6(file_path, doc_id, visitor_id)
