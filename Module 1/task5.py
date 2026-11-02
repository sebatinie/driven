from collections import defaultdict


def find_gc_candidates(ref_counts, relationships):
    """
    Identify objects eligible for garbage collection.

    Criteria:
    1. Reference count <= 1
    2. Object participates in a circular reference
    """

    candidates = {
        obj_id
        for obj_id, count in ref_counts.items()
        if count <= 1
    }

    # Build graph
    graph = defaultdict(list)
    for src, dst in relationships:
        graph[src].append(dst)

    index = 0
    indices = {}
    lowlink = {}
    stack = []
    on_stack = set()

    def tarjan(node):
        nonlocal index

        indices[node] = lowlink[node] = index
        index += 1

        stack.append(node)
        on_stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in indices:
                tarjan(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif neighbor in on_stack:
                lowlink[node] = min(lowlink[node], indices[neighbor])

        # Root of a strongly connected component
        if lowlink[node] == indices[node]:
            scc = []

            while True:
                n = stack.pop()
                on_stack.remove(n)
                scc.append(n)

                if n == node:
                    break

            # Multi-node SCC indicates a cycle
            if len(scc) > 1:
                candidates.update(scc)

            # Self-loop cycle
            elif node in graph[node]:
                candidates.add(node)

    # Process all nodes
    all_nodes = set(ref_counts.keys())

    for src, dst in relationships:
        all_nodes.add(src)
        all_nodes.add(dst)

    for node in all_nodes:
        if node not in indices:
            tarjan(node)

    return sorted(candidates)


# Test data
ref_counts = {
    "A": 2,
    "B": 2,
    "C": 1,
    "D": 3,
    "E": 2
}

relationships = [
    ("A", "B"),
    ("B", "A"),  # Circular reference
    ("D", "E")
]

# Run analysis
candidates = find_gc_candidates(ref_counts, relationships)

# Display relevant information
print("\n=== Garbage Collection Analysis ===")
print(f"Reference Counts: {ref_counts}")
print(f"Relationships: {relationships}")
print(f"GC Candidates: {candidates}")