import unittest
from mock import MagicMock, patch

from components.ast_binary_graph.codebase_graph import CodebaseGraph
from components.ast_binary_graph.data_model.circular_binary_graph import CircularBinaryGraph
from components.ast_binary_graph.data_model.metadata import Metadata

class TestCodebaseGraph(unittest.TestCase):

    def setUp(self):
        # Mock the resource_processor to avoid actual file operations
        self.mock_processor = MagicMock()
        self.codebase_graph = CodebaseGraph(self.mock_processor)

    def test_should_include_resource(self):
        result = self.codebase_graph.should_include_resource('include_me.py', r'include_.*', r'exclude_.*')
        self.assertTrue(result)

        result = self.codebase_graph.should_include_resource('exclude_me.py', r'include_.*', r'exclude_.*')
        self.assertFalse(result)

    def test_get_or_create_uuid(self):
        resource_name = "sample_resource"
        uuid1 = self.codebase_graph.get_or_create_uuid(resource_name)
        uuid2 = self.codebase_graph.get_or_create_uuid(resource_name)

        # Ensure the same UUID is returned for subsequent calls
        self.assertEqual(uuid1, uuid2)

    @patch('components.ast_binary_graph.codebase_graph.CodebaseGraph.process_resource')
    def test_traverse_folder(self, mock_process_resource):
        # Mocking the get_resources_in_folder method to return a sample list of resources
        self.mock_processor.get_resources_in_folder.return_value = ["include_file1.py", "include_file2.py"]
        self.mock_processor.get_filename.side_effect = lambda x: x
        self.mock_processor.is_resource_a_folder.return_value = False

        self.codebase_graph.traverse_folder("test_folder", True, r'include_.*', r'exclude_.*')

        # Ensure process_resource is called for each file
        self.assertEqual(mock_process_resource.call_count, 2)

    def test_generate(self):
        with patch('components.ast_binary_graph.codebase_graph.CodebaseGraph.traverse_folder') as mock_traverse_folder:
            self.codebase_graph.generate("test_base", True, r'include_.*', r'exclude_.*')
            mock_traverse_folder.assert_called_once_with("test_base", True, r'include_.*', r'exclude_.*')
    
    def test_get_or_create_uuid_new_resource(self):
        resource_name = "new_resource"
        uuid_ = self.codebase_graph.get_or_create_uuid(resource_name)
        self.assertEqual(uuid_, self.codebase_graph.resource_to_uuid_map[resource_name])

    def test_process_resource_metadata_creation(self):
        resource = MagicMock()
        resource.name = "test_resource"
        self.mock_processor.get_filename.return_value = "test_filename"
        self.mock_processor.count_lines.return_value = 10
        self.mock_processor.count_relations.return_value = 2
        self.mock_processor.determine_resource_type.return_value = "file"

        self.codebase_graph.process_resource(resource, "test_path")
        self.assertIn(self.codebase_graph.get_or_create_uuid(resource.name), self.codebase_graph.metadata_map)

    def test_get_or_create_uuid_new_resource(self):
            resource_name = "new_resource"
            uuid_ = self.codebase_graph.get_or_create_uuid(resource_name)
            self.assertIn(resource_name, self.codebase_graph.resource_to_uuid_map)
            self.assertEqual(uuid_, self.codebase_graph.resource_to_uuid_map[resource_name])

    def test_process_resource_with_new_metadata(self):
        resource = MagicMock(name="test_resource")
        resource.name = "test_resource"
        self.mock_processor.get_imports_and_exports.return_value = []

        self.codebase_graph.process_resource(resource, "test_path")
        uuid_ = self.codebase_graph.get_or_create_uuid(resource.name)
        self.assertIn(uuid_, self.codebase_graph.metadata_map)

    def test_process_resource_graph_linking(self):
        resource = MagicMock(name="test_resource")
        resource.name = "test_resource"
        linked_resources = ["linked_resource1", "linked_resource2"]
        self.mock_processor.get_imports_and_exports.return_value = linked_resources

        self.codebase_graph.process_resource(resource, "test_path")

    def test_traverse_folder_exclude_resources(self):
        excluded_file = "exclude_me.py"
        self.mock_processor.get_resources_in_folder.return_value = [excluded_file]
        self.mock_processor.get_filename.return_value = excluded_file

        self.codebase_graph.traverse_folder("test_folder", True, r'include_.*', r'exclude_.*')
        # Ensure that process_resource wasn't called for the excluded file
        self.mock_processor.process_resource.assert_not_called()

    def test_traverse_folder_recursive(self):
        # Mock return values to simulate a folder and files
        self.mock_processor.reset_mock()
        self.mock_processor = MagicMock()
        self.mock_processor.get_resources_in_folder.side_effect = [
            [Metadata(name="test_resource",path="", filename="",lines=2,relations_count=2,resource_type="file")],       # First call returns a folder
            [Metadata(name="file1.py",path="", filename="",lines=2,relations_count=2,resource_type="file"), Metadata(name="file2.py",path="", filename="",lines=2,relations_count=2,resource_type="file")]  # Second call returns files inside the folder
        ]
        self.mock_processor.get_imports_and_exports.side_effect = [
            ["test_resource"],       # First call returns a folder
            ["file1.py","file2.py"]  # Second call returns files inside the folder
        ]
        self.mock_processor.is_resource_a_folder.side_effect = [True,False,False,False]
        self.mock_processor.get_filename.side_effect = [
            "test_resource",       # First call returns a folder
            "file1.py",
            "file2.py"  # Second call returns files inside the folder
        ]

        self.codebase_graph.traverse_folder("test_folder", True, r'.*', r'')

    def test_generate(self):
        self.mock_processor.get_resources_in_folder.return_value = ["file1.py"]
        self.mock_processor.get_filename.return_value = "file1.py"
        graph, metadata_map = self.codebase_graph.generate("test_base", True, r'include_.*', r'exclude_.*')
        self.assertIsInstance(graph, CircularBinaryGraph)
        self.assertIsInstance(metadata_map, dict)


if __name__ == '__main__':
    unittest.main()
