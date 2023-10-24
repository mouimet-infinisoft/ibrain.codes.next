from pprint import pprint
import uuid
import re
from components.ast_binary_graph.data_model.circular_binary_graph import CircularBinaryGraph

class CodebaseGraph:
    
    def __init__(self, resource_processor):
        self.graph = CircularBinaryGraph()
        self.metadata_map = {}
        self.resource_to_uuid_map = {}
        self.resource_processor = resource_processor

    def should_include_resource(self, resource_name, include_pattern, exclude_pattern):
        return re.match(include_pattern, resource_name) #and not re.match(exclude_pattern, resource_name)

    def get_or_create_uuid(self, resource_name):
        if resource_name in self.resource_to_uuid_map:
            return self.resource_to_uuid_map[resource_name]
        
        new_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, resource_name))
        self.resource_to_uuid_map[resource_name] = new_uuid
        return new_uuid

    def process_resource(self, resource, path):
        uuid_ = self.get_or_create_uuid(resource.name)

        if uuid_ not in self.metadata_map:
            self.metadata_map[uuid_] = resource

        pprint(self.resource_processor.get_imports_and_exports(resource))
        for imp_exp in self.resource_processor.get_imports_and_exports(resource):
            linked_resource_uuid = self.get_or_create_uuid(imp_exp)
            self.graph.link(uuid_, linked_resource_uuid)

    def traverse_folder(self, folder_path, recursive, include_pattern, exclude_pattern):
        for resource in self.resource_processor.get_resources_in_folder(folder_path):
            pprint(resource)
            if not self.should_include_resource(resource.name, include_pattern, exclude_pattern):
                continue

            if recursive and self.resource_processor.is_resource_a_folder(resource):
                self.traverse_folder(resource.path, recursive, include_pattern, exclude_pattern)
            else:
                self.process_resource(resource, folder_path + resource.name)

    def generate(self, base, recursive, include_pattern, exclude_pattern):
        self.traverse_folder(base, recursive, include_pattern, exclude_pattern)
        return self.graph, self.metadata_map
