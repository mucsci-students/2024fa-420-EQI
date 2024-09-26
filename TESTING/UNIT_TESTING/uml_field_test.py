import sys
import os
import unittest 


###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_CORE.UML_FIELD.uml_field import UMLField  # noqa: E402

###############################################################################
class TestUMLField(unittest.TestCase):

    def setUp(self):
        # Set up an instance of UMLField for testing
        self.test_field = UMLField("test_field")

    def test_get_name(self):
        # Test that the field name is returned correctly
        self.assertEqual(self.test_field._get_name(), "test_field")

    def test_set_name(self):
        # Test setting a new field name
        self.test_field._set_name("new_field_name")
        self.assertEqual(self.test_field._get_name(), "new_field_name")

    def test_str(self):
        # Test the string representation of the field
        self.assertEqual(str(self.test_field), "test_field")

if __name__ == '__main__':
    unittest.main()
