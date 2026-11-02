def identify_gc_candidates(objects, relationships):
    gc_candidates = {
        obj_id
        for obj_id, count in objects.items()
        if count <= 1
    }

    visited = set()
    rec_stack = set()

    # Build graph
    graph = {}

    for src, dst in relationships:
        if src not in graph:
            graph[src] = []
        graph[src].append(dst)

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    gc_candidates.add(node)
            elif neighbor in rec_stack:
                # Cycle found
                gc_candidates.add(node)
                gc_candidates.add(neighbor)
                return True

        rec_stack.remove(node)
        return False

    # Check each object for circular references
    for obj_id in objects:
        if obj_id not in visited:
            dfs(obj_id)

    return list(gc_candidates)


# Example
objects = {
    "A": 2,
    "B": 2,
    "C": 1,
    "D": 3
}

relationships = [
    ("A", "B"),
    ("B", "A"),
    ("D", "C")
]

candidates = identify_gc_candidates(objects, relationships)

print("Objects:", objects)
print("Relationships:", relationships)
print("GC Candidates:", candidates)