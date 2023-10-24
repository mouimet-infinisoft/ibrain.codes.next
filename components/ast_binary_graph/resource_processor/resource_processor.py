from abc import ABC, abstractmethod

class ResourceProcessor(ABC):

    @abstractmethod
    def get_filename(self, path):
        pass

    @abstractmethod
    def count_lines(self, resource):
        pass

    @abstractmethod
    def count_relations(self, resource):
        pass

    @abstractmethod
    def determine_resource_type(self, resource):
        pass

    @abstractmethod
    def get_imports_and_exports(self, resource):
        pass

    @abstractmethod
    def get_resources_in_folder(self, folder_path):
        pass

    @abstractmethod
    def is_resource_a_folder(self, resource):
        pass