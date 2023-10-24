class CircularBinaryGraph:
    def __init__(self):
        self.graph = {}

    def link(self, src_uuid, dest_uuid):
        if src_uuid not in self.graph:
            self.graph[src_uuid] = []
        self.graph[src_uuid].append(dest_uuid)

    def __repr__(self):
        return f"CircularBinaryGraph(graph={self.graph!r})"

    def __str__(self):
        # Assuming you want a pretty printed format for the graph
        graph_str = "\n".join([f"{src} -> {', '.join(dests)}" for src, dests in self.graph.items()])
        return f"CircularBinaryGraph:\n{graph_str}"