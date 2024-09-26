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
from UML_CORE.UML_FIELD.uml_field import UMLField
from UML_CORE.UML_METHOD.uml_method import UMLMethod
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship
from UML_MANAGER.uml_core_manager import UMLCoreManager

###############################################################################

class TestUMLCoreManagerIntegration(unittest.TestCase):

    def setUp(self):
        """Set up a UMLCoreManager instance for integration testing."""
        self.manager = UMLCoreManager()

    def test_add_class_with_field_and_method(self):
        """Test adding a class with a field and a method."""
        class_name = "TestClass"
        field_name = "test_field"
        method_name = "test_method"

        # Add class
        self.manager._add_class(class_name, is_loading=False)

        # Add field to class
        test_class = self.manager._UMLCoreManager__class_list[class_name]
        field = UMLField(field_name)
        test_class._set_class_field_list([field])  # Directly setting field list for testing
        
        # Add method to class
        method = UMLMethod(method_name)
        test_class._set_class_method_list([method])  # Directly setting method list for testing

        # Validate field and method were added
        self.assertIn(field, test_class._get_class_field_list())
        self.assertIn(method, test_class._get_class_method_list())

    def test_add_relationship(self):
        """Test adding a relationship between two classes."""
        source_class_name = "SourceClass"
        destination_class_name = "DestinationClass"
        rel_type = "Composition"

        # Add source and destination classes
        self.manager._add_class(source_class_name, is_loading=False)
        self.manager._add_class(destination_class_name, is_loading=False)

        # Create relationship
        relationship = UMLRelationship(source_class_name, destination_class_name, rel_type)

        self.manager._UMLCoreManager__relationship_list.append(relationship)

        # Validate relationship was added
        self.assertIn(relationship, self.manager._UMLCoreManager__relationship_list)


    def test_full_integration(self):
        """Test full integration of adding a class, field, method, and relationship."""
        class_a_name = "ClassA"
        class_b_name = "ClassB"
        field_a_name = "fieldA"
        method_a_name = "methodA"
        relationship_type = "Association"

        # Add Class A
        self.manager._add_class(class_a_name, is_loading=False)
        class_a = self.manager._UMLCoreManager__class_list[class_a_name]

        # Add field and method to Class A
        class_a._set_class_field_list([UMLField(field_a_name)])
        class_a._set_class_method_list([UMLMethod(method_a_name)])

        # Add Class B
        self.manager._add_class(class_b_name, is_loading=False)

        # Create and add relationship between Class A and Class B
        relationship = UMLRelationship(class_a_name, class_b_name, relationship_type)
        self.manager._UMLCoreManager__relationship_list.append(relationship)

        # Assertions
        self.assertIn(class_a_name, self.manager._UMLCoreManager__class_list)
        self.assertIn(class_b_name, self.manager._UMLCoreManager__class_list)
        self.assertEqual(class_a._get_class_field_list()[0]._get_name(), field_a_name)
        self.assertEqual(class_a._get_class_method_list()[0]._get_name(), method_a_name)
        self.assertIn(relationship, self.manager._UMLCoreManager__relationship_list)

    def test_add_duplicate_class(self):
        class_name = "DuplicateClass"

        # Add the class first time
        self.manager._add_class(class_name, is_loading=False)

        # Try to add the class again
        self.manager._add_class(class_name, is_loading=False)

        # Verify that the class still exists and no duplicate was added
        self.assertEqual(len(self.manager._UMLCoreManager__class_list), 1)

    def test_delete_class(self):
        class_name = "ClassToRemove"

        # Add the class
        self.manager._add_class(class_name, is_loading=False)

        # Remove the class (assuming a remove method exists)
        self.manager._delete_class(class_name, is_loading=False)

        # Check that the class is no longer in the class list
        self.assertNotIn(class_name, self.manager._UMLCoreManager__class_list)


if __name__ == "__main__":
    unittest.main()
