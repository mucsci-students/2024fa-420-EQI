import sys
import os
import unittest 


###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_CORE.UML_METHOD.uml_method import UMLMethod
###############################################################################


class TestUMLMethod(unittest.TestCase):

    def setUp(self):
        # Set up an instance of UMLMethod for testing
        self.test_method = UMLMethod("test_method")

    def test_get_name(self):
        # Test that the method name is returned correctly
        self.assertEqual(self.test_method._get_name(), "test_method")

    def test_set_name(self):
        # Test setting a new method name
        self.test_method._set_name("new_method_name")
        self.assertEqual(self.test_method._get_name(), "new_method_name")

    def test_str(self):
        # Test the string representation of the method
        self.assertEqual(str(self.test_method), "test_method")

if __name__ == '__main__':
    unittest.main()
