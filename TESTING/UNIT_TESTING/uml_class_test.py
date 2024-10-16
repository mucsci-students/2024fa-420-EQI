import sys
import os
import unittest 


###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_CORE.UML_CLASS.uml_class import UMLClass

###############################################################################

class TestUMLClass(unittest.TestCase):

    def setUp(self):
        # Set up an instance of UMLClass for testing
        self.test_class = UMLClass("test_class")

    def test_get_class_name(self):
        # Test that the class name is returned correctly
        self.assertEqual(self.test_class._get_class_name(), "test_class")

    def test_set_class_name(self):
        # Test setting a new class name
        self.test_class._set_class_name("new_class_name")
        self.assertEqual(self.test_class._get_class_name(), "new_class_name")


if __name__ == '__main__':
    unittest.main()
