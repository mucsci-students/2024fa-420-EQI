import sys
import os
import unittest 


###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter

###############################################################################


class TestUMLParameter(unittest.TestCase):

    def setUp(self):
        # Set up an instance of UMLParameter for testing
        self.test_parameter = UMLParameter("test_parameter")

    def test_get_parameter_name(self):
        # Test that the parameter name is returned correctly
        self.assertEqual(self.test_parameter._get_parameter_name(), "test_parameter")

    def test_set_parameter_name(self):
        # Test setting a new parameter name
        self.test_parameter._set_parameter_name("new_parameter_name")
        self.assertEqual(self.test_parameter._get_parameter_name(), "new_parameter_name")

if __name__ == '__main__':
    unittest.main()
