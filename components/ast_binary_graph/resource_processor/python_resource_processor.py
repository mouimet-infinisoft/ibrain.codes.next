import ast
import os
from pprint import pprint
from components.ast_binary_graph.data_model.metadata import Metadata
from components.ast_binary_graph.resource_processor.resource_processor import ResourceProcessor

class PythonResourceProcessor(ResourceProcessor):

    def get_filename(self, path):
        return os.path.basename(path)

    def count_lines(self, resource):
        # Assuming resource is the content of a file
        return 10#len(resource.splitlines())

    def count_relations(self, resource):
        # Parse the resource using Python's AST
        # tree = ast.parse(resource)
        return 0#len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))])

    def determine_resource_type(self, resource):
        # Here, we'll just classify everything as a 'file' for simplicity
        return 'file'

    def get_imports_and_exports(self, resource):
        with open(resource.path, 'r') as file:
            file_contents = file.read()
    
        tree = ast.parse(source=file_contents)

        return [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]

    def get_resources_in_folder(self, folder_path):
        # Return Metadata objects for all Python files in the specified folder
        resources = []
        
        for f in os.listdir(folder_path):
            full_path = os.path.join(folder_path, f)
            if f.endswith('.py'):
                resource_metadata = Metadata(
                    name=f,
                    filename=f,
                    path=full_path,
                    lines=10,
                    relations_count=10,#self.count_relations(full_path),  # Assuming you have a method to count relations
                    resource_type="file"
                )
                resources.append(resource_metadata)
            elif os.path.isdir(full_path):
                resource_metadata = Metadata(
                    name=f,
                    filename=f,
                    path=full_path,
                    lines=0,  # Folders don't have lines, so set to 0
                    relations_count=0,  # Placeholder value; could be the number of files/subfolders
                    resource_type="folder"
                )
                resources.append(resource_metadata)
    
        return resources


    def is_resource_a_folder(self, resource):
        return resource.resource_type == "folder"
