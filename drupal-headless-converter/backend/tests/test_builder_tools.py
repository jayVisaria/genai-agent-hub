import unittest
import os
import shutil
from backend.agents.builder_agent import read_file, write_file, list_files, make_directory

class TestBuilderTools(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_builder_tools"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_write_and_read_file(self):
        file_path = os.path.join(self.test_dir, "test.txt")
        content = "Hello, world!"
        write_file(file_path, content)
        self.assertEqual(read_file(file_path), content)

    def test_list_files(self):
        file_path = os.path.join(self.test_dir, "test.txt")
        with open(file_path, "w") as f:
            f.write("test")
        self.assertIn("test.txt", list_files(self.test_dir))

    def test_make_directory(self):
        dir_path = os.path.join(self.test_dir, "new_dir")
        make_directory(dir_path)
        self.assertTrue(os.path.isdir(dir_path))

