from collections import defaultdict
from task5 import return_visitors, return_documents, also_likes, sort_by_shared_readers

def generate_dot_graph(input_doc, input_visitor, file_path, sort_func):
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
    with open("also_likes.dot", "w") as f:
        f.write("\n".join(dot))

    print("DOT file generated: also_likes.dot")


if __name__ == "__main__":
    file_path = "issuu_cw2.json"
    # doc_id = "140228202800-6ef39a241f35301a9a42cd0ed21e5fb0"
    # visitor_id = "2f63e0cca690da91"
    doc_id = "140227140914-9ebad8b641c3754defdd0aa4bdd3aa09"
    visitor_id = "6262b769706ad29d"
    generate_dot_graph(doc_id, visitor_id, file_path, sort_by_shared_readers)
    also_docs = also_likes(doc_id, file_path, sort_by_shared_readers)
    print("Top 10 also-like docs (last 4 chars):")
    for d in also_docs:
        print(f"  {d[-4:]}")
