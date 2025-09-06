import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

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
        write_file.invoke({"path": file_path, "content": content})
        self.assertEqual(read_file.invoke({"path": file_path}), content)

    def test_list_files(self):
        file_path = os.path.join(self.test_dir, "test.txt")
        with open(file_path, "w") as f:
            f.write("test")
        self.assertIn("test.txt", list_files.invoke({"path": self.test_dir}))

    def test_make_directory(self):
        dir_path = os.path.join(self.test_dir, "new_dir")
        make_directory.invoke({"path": dir_path})
        self.assertTrue(os.path.isdir(dir_path))



