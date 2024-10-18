import sys
import os
import unittest
from unittest.mock import MagicMock


###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_MVC.UML_VIEW.UML_CLI_VIEW.uml_cli_view import UMLView
from UML_INTERFACE.uml_controller_interface import UMLInterface
from UML_MVC.UML_MODEL.uml_model import UMLModel

###############################################################################

class TestUMLClassManagement(unittest.TestCase):

    def setUp(self):
        """Set up a UMLInterface instance for class management testing."""
        # Mock the view and model
        self.mock_view = MagicMock()
        self.mock_model = MagicMock()

        # Create a UMLInterface instance
        self.manager = UMLInterface(self.mock_view)
        self.manager.Model = self.mock_model  # Replace with mock model

    ################################################################################################################
    ## ADD FUNCTIONS ##
    ################################################################################################################

    def test_add_class(self):
        """Test adding a class."""
        class_name = "TestClass"

        # Simulate the expected output from the model
        self.manager.Model._add_class.return_value = "Class added"

        # Call the method
        result = self.manager.add_class(class_name)

        # Verify that the model's _add_class method was called with the correct arguments
        self.manager.Model._add_class.assert_called_once_with(class_name, is_loading=False)

        # Assert that the method's return value is as expected
        self.assertEqual(result, "Class added")

    def test_add_duplicate_class(self):
        """Test trying to add a duplicate class."""
        class_name = "TestClass"

        # Simulate the expected output when trying to add a duplicate class
        self.manager.Model._add_class.return_value = "Class already exists"

        # Call the method
        result = self.manager.add_class(class_name)

        # Verify that the model's _add_class method was called with the correct arguments
        self.manager.Model._add_class.assert_called_once_with(class_name, is_loading=False)

        # Assert that the method's return value indicates a duplicate class
        self.assertEqual(result, "Class already exists")
    
    def test_add_empty_class_name(self):
        """Test trying to add a class with an empty name."""
        class_name = ""

        # Simulate the expected output when trying to add a class with an empty name
        self.manager.Model._add_class.return_value = "Invalid class name"

        # Call the method
        result = self.manager.add_class(class_name)

        # Verify that the model's _add_class method was called with the correct arguments
        self.manager.Model._add_class.assert_called_once_with(class_name, is_loading=False)

        # Assert that the method's return value indicates an invalid class name
        self.assertEqual(result, "Invalid class name")

    def test_add_class_case_sensitivity(self):
        """Test adding two classes with names that differ only by case."""
        class_name_1 = "TestClass"
        class_name_2 = "testclass"

        # Simulate the expected output for adding the first class
        self.manager.Model._add_class.return_value = "Class added"
        result = self.manager.add_class(class_name_1)
        self.assertEqual(result, "Class added")

        # Simulate the expected output for adding the second class (assuming case-sensitive system)
        self.manager.Model._add_class.return_value = "Class added"
        result = self.manager.add_class(class_name_2)
        self.assertEqual(result, "Class added")

        # Verify that the model's _add_class method was called twice, with different case-sensitive names
        self.manager.Model._add_class.assert_any_call(class_name_1, is_loading=False)
        self.manager.Model._add_class.assert_any_call(class_name_2, is_loading=False)
        
    ################################################################################################################
    ## DELETE FUNCTIONS ##
    ################################################################################################################

    def test_delete_class(self):
        """Test deleting an existing class."""
        class_name = "TestClass"

        # Simulate the expected output when the class is successfully deleted
        self.manager.Model._delete_class.return_value = "Class deleted"

        # Call the method
        result = self.manager.delete_class(class_name)

        # Verify that the model's _delete_class method was called with the correct arguments
        self.manager.Model._delete_class.assert_called_once_with(class_name)

        # Assert that the method's return value is as expected
        self.assertEqual(result, "Class deleted")

    def test_delete_nonexistent_class(self):
        """Test trying to delete a class that doesn't exist."""
        class_name = "NonExistentClass"

        # Simulate the expected output when trying to delete a class that doesn't exist
        self.manager.Model._delete_class.return_value = "Class does not exist"

        # Call the method
        result = self.manager.delete_class(class_name)

        # Verify that the model's _delete_class method was called with the correct arguments
        self.manager.Model._delete_class.assert_called_once_with(class_name)

        # Assert that the method's return value indicates the class does not exist
        self.assertEqual(result, "Class does not exist")

    def test_delete_class_with_empty_name(self):
        """Test trying to delete a class with an empty name."""
        class_name = ""

        # Simulate the expected output when trying to delete a class with an empty name
        self.manager.Model._delete_class.return_value = "Invalid class name"

        # Call the method
        result = self.manager.delete_class(class_name)

        # Verify that the model's _delete_class method was called with the correct arguments
        self.manager.Model._delete_class.assert_called_once_with(class_name)

        # Assert that the method's return value indicates the class name is invalid
        self.assertEqual(result, "Invalid class name")

    def test_delete_class_already_deleted(self):
        """Test trying to delete a class that has already been deleted."""
        class_name = "TestClass"

        # Simulate the first successful deletion
        self.manager.Model._delete_class.return_value = "Class deleted"
        result = self.manager.delete_class(class_name)
        self.assertEqual(result, "Class deleted")

        # Simulate the output when trying to delete the same class again
        self.manager.Model._delete_class.return_value = "Class does not exist"
        result = self.manager.delete_class(class_name)

        # Assert that the second deletion attempt indicates the class does not exist
        self.assertEqual(result, "Class does not exist")


    ################################################################################################################
    ## RENAME FUNCTIONS ##
    ################################################################################################################

    def test_rename_class(self):
        """Test renaming an existing class."""
        old_name = "OldClassName"
        new_name = "NewClassName"

        # Simulate the expected output when the class is successfully renamed
        self.manager.Model._rename_class.return_value = "Class renamed"

        # Call the method
        result = self.manager.rename_class(old_name, new_name)

        # Verify that the model's _rename_class method was called with the correct arguments
        self.manager.Model._rename_class.assert_called_once_with(old_name, new_name)

        # Assert that the method's return value is as expected
        self.assertEqual(result, "Class renamed")

    def test_rename_nonexistent_class(self):
        """Test trying to rename a class that doesn't exist."""
        old_name = "NonExistentClass"
        new_name = "NewClassName"

        # Simulate the expected output when trying to rename a nonexistent class
        self.manager.Model._rename_class.return_value = "Class does not exist"

        # Call the method
        result = self.manager.rename_class(old_name, new_name)

        # Verify that the model's _rename_class method was called with the correct arguments
        self.manager.Model._rename_class.assert_called_once_with(old_name, new_name)

        # Assert that the method's return value indicates the class does not exist
        self.assertEqual(result, "Class does not exist")

    def test_rename_class_to_existing_name(self):
        """Test renaming a class to a name that already exists."""
        old_name = "OldClassName"
        new_name = "ExistingClassName"

        # Simulate the expected output when trying to rename to an existing class name
        self.manager.Model._rename_class.return_value = "Class name already exists"

        # Call the method
        result = self.manager.rename_class(old_name, new_name)

        # Verify that the model's _rename_class method was called with the correct arguments
        self.manager.Model._rename_class.assert_called_once_with(old_name, new_name)

        # Assert that the method's return value indicates the new class name already exists
        self.assertEqual(result, "Class name already exists")

    def test_rename_class_to_case_sensitive_duplicate(self):
        """Test renaming a class to a name that differs only by case."""
        old_name = "TestClass"
        new_name = "testclass"

        # Simulate the expected output when the system allows case-sensitive duplicates
        self.manager.Model._rename_class.return_value = "Class renamed"

        # Call the method to rename the class
        result = self.manager.rename_class(old_name, new_name)

        # Verify that the model's _rename_class method was called with the correct arguments
        self.manager.Model._rename_class.assert_called_once_with(old_name, new_name)

        # Assert that the method's return value indicates the class was renamed successfully
        self.assertEqual(result, "Class renamed")

    def test_rename_class_to_empty_name(self):
        """Test renaming a class to an empty string."""
        old_name = "TestClass"
        new_name = ""

        # Simulate the expected output when trying to rename to an empty string
        self.manager.Model._rename_class.return_value = "Invalid class name"

        # Call the method
        result = self.manager.rename_class(old_name, new_name)

        # Verify that the model's _rename_class method was called with the correct arguments
        self.manager.Model._rename_class.assert_called_once_with(old_name, new_name)

        # Assert that the method's return value indicates an invalid class name
        self.assertEqual(result, "Invalid class name")


if __name__ == "__main__":
    unittest.main()
