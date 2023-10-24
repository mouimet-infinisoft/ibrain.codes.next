from pprint import pprint
from components.ast_binary_graph.codebase_graph import CodebaseGraph
from components.ast_binary_graph.resource_processor.python_resource_processor import PythonResourceProcessor


processor = PythonResourceProcessor()
graph_generator = CodebaseGraph(processor)
graph, metadata_map = graph_generator.generate(base=".", recursive=True, include_pattern=r".*", exclude_pattern="")

pprint(vars(graph))
pprint(metadata_map)