import sys
import os
import unittest 


###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship

###############################################################################

class TestUMLRelationship(unittest.TestCase):

    def setUp(self):
        # Set up an instance of UMLRelationship for testing
        self.test_relationship = UMLRelationship("classA", "classB", "association")

    def test_get_source_class(self):
        # Test that the source class name is returned correctly
        self.assertEqual(self.test_relationship._get_source_class(), "classA")

    def test_get_destination_class(self):
        # Test that the destination class name is returned correctly
        self.assertEqual(self.test_relationship._get_destination_class(), "classB")

    def test_get_type(self):
        # Test that the relationship type is returned correctly
        self.assertEqual(self.test_relationship._get_type(), "association")

    def test_set_source_class(self):
        # Test setting a new source class name
        self.test_relationship._set_source_class("newClassA")
        self.assertEqual(self.test_relationship._get_source_class(), "newClassA")

    def test_set_destination_class(self):
        # Test setting a new destination class name
        self.test_relationship._set_destination_class("newClassB")
        self.assertEqual(self.test_relationship._get_destination_class(), "newClassB")

    def test_set_type(self):
        # Test setting a new relationship type
        self.test_relationship._set_type("aggregation")
        self.assertEqual(self.test_relationship._get_type(), "aggregation")

if __name__ == '__main__':
    unittest.main()
