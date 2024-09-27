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

class TestUMLClassManagement(unittest.TestCase):

    def setUp(self):
        """Set up a UMLCoreManager instance for class management testing."""
        self.manager = UMLCoreManager()

    def test_add_class(self):
        """Test adding a class."""
        class_name = "TestClass"
        self.manager._add_class(class_name, is_loading=False)
        self.assertIn(class_name, self.manager._UMLCoreManager__class_list)

    def test_add_duplicate_class(self):
        """Test attempting to add a duplicate class."""
        class_name = "DuplicateClass"
        self.manager._add_class(class_name, is_loading=False)
        self.manager._add_class(class_name, is_loading=False)
        self.assertEqual(len(self.manager._UMLCoreManager__class_list), 1)

    def test_delete_class(self):
        """Test deleting a class."""
        class_name = "ClassToRemove"
        self.manager._add_class(class_name, is_loading=False)
        self.manager._delete_class(class_name, is_loading=False)
        self.assertNotIn(class_name, self.manager._UMLCoreManager__class_list)

    def test_rename_class(self):
        """Test renaming a class."""
        old_name = "OldClassName"
        new_name = "NewClassName"
        self.manager._add_class(old_name, is_loading=False)
        self.manager._rename_class(old_name, new_name, is_loading=False)
        self.assertNotIn(old_name, self.manager._UMLCoreManager__class_list)
        self.assertIn(new_name, self.manager._UMLCoreManager__class_list)


class TestUMLFieldManagement(unittest.TestCase):

    def setUp(self):
        """Set up a UMLCoreManager instance for field management testing."""
        self.manager = UMLCoreManager()

    def test_add_field_to_class(self):
        """Test adding a field to a class."""
        class_name = "TestClass"
        field_name = "test_field"
        self.manager._add_class(class_name, is_loading=False)
        test_class = self.manager._UMLCoreManager__class_list[class_name]
        field = UMLField(field_name)
        test_class._set_class_field_list([field])
        self.assertIn(field, test_class._get_class_field_list())

    def test_remove_field_from_class(self):
        """Test removing a field from a class using the manager's delete field method."""
        class_name = "TestClass"
        field_name = "test_field"

        # Add class and field
        self.manager._add_class(class_name, is_loading=False)
        test_class = self.manager._UMLCoreManager__class_list[class_name]
        field = UMLField(field_name)
        test_class._set_class_field_list([field])

        # Ensure field was added
        self.assertIn(field, test_class._get_class_field_list())

        # Use the UMLCoreManager's delete field method to remove the field
        self.manager._delete_field(class_name, field_name, is_loading=False)

        # Verify that the field has been removed
        self.assertNotIn(field, test_class._get_class_field_list())

    def test_rename_field_in_class(self):
        """Test renaming a field in a class."""
        class_name = "TestClass"
        old_field_name = "old_field"
        new_field_name = "new_field"

        # Add class and field
        self.manager._add_class(class_name, is_loading=False)
        test_class = self.manager._UMLCoreManager__class_list[class_name]
        field = UMLField(old_field_name)
        test_class._set_class_field_list([field])

        # Ensure field was added
        self.assertIn(field, test_class._get_class_field_list())

        # Use the UMLCoreManager's rename field method
        self.manager._rename_field(class_name, old_field_name, new_field_name, is_loading=False)

        # Verify that the field's name has been updated
        renamed_field = test_class._get_class_field_list()[0]
        self.assertEqual(renamed_field._get_name(), new_field_name)

class TestUMLRelationshipManagement(unittest.TestCase):

    def setUp(self):
        """Set up a UMLCoreManager instance for relationship management testing."""
        self.manager = UMLCoreManager()

    def test_add_relationship(self):
        """Test adding a relationship between two classes."""
        source_class_name = "SourceClass"
        destination_class_name = "DestinationClass"
        rel_type = "Composition"
        self.manager._add_class(source_class_name, is_loading=False)
        self.manager._add_class(destination_class_name, is_loading=False)
        relationship = UMLRelationship(source_class_name, destination_class_name, rel_type)
        self.manager._UMLCoreManager__relationship_list.append(relationship)
        self.assertIn(relationship, self.manager._UMLCoreManager__relationship_list)

    def test_delete_relationship(self):
        """Test deleting a relationship between two classes."""
        source_class_name = "SourceClass"
        destination_class_name = "DestinationClass"
        rel_type = "Association"

        # Add classes
        self.manager._add_class(source_class_name, is_loading=False)
        self.manager._add_class(destination_class_name, is_loading=False)

        # Create a relationship
        relationship = UMLRelationship(source_class_name, destination_class_name, rel_type)
        self.manager._UMLCoreManager__relationship_list.append(relationship)

        # Verify that the relationship was added
        self.assertIn(relationship, self.manager._UMLCoreManager__relationship_list)

        # Delete the relationship using the manager's delete relationship method
        self.manager._delete_relationship(source_class_name, destination_class_name, is_loading=False)

        # Verify that the relationship has been removed
        self.assertNotIn(relationship, self.manager._UMLCoreManager__relationship_list)

class TestUMLIntegration(unittest.TestCase):

    def setUp(self):
        """Set up a UMLCoreManager instance for full integration testing."""
        self.manager = UMLCoreManager()

    def test_full_integration(self):
        """Test adding a class, field, method, and relationship."""
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

    def test_relationship_updates_when_class_is_renamed(self):
        """Test that the relationship updates when a class is renamed."""
        class_a_name = "ClassA"
        class_b_name = "ClassB"
        renamed_class_a_name = "ClassC"
        relationship_type = "Association"

        # Add ClassA and ClassB
        self.manager._add_class(class_a_name, is_loading=False)
        self.manager._add_class(class_b_name, is_loading=False)

        # Create a relationship between ClassA and ClassB
        relationship = UMLRelationship(class_a_name, class_b_name, relationship_type)
        self.manager._UMLCoreManager__relationship_list.append(relationship)

        # Verify that the relationship was added
        self.assertIn(relationship, self.manager._UMLCoreManager__relationship_list)
        self.assertEqual(relationship._get_source_class(), class_a_name)  # Check if source is ClassA
        self.assertEqual(relationship._get_destination_class(), class_b_name)  # Check if destination is ClassB

        # Rename ClassA to ClassC
        self.manager._rename_class(class_a_name, renamed_class_a_name, is_loading=False)

        # Check if the source class in the relationship is updated to ClassC
        updated_relationship = self.manager._UMLCoreManager__relationship_list[0]  # Get the updated relationship
        self.assertEqual(updated_relationship._get_source_class(), renamed_class_a_name)  # Check if source is now ClassC

        # Verify that the destination class (ClassB) is unchanged
        self.assertEqual(updated_relationship._get_destination_class(), class_b_name)

if __name__ == "__main__":
    unittest.main()
