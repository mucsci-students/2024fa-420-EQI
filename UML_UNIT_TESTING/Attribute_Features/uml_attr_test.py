import os
import sys
import io
import unittest
from unittest.mock import patch

# Add the root directory of the project to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

import UML_CORE.UML_ATTRIBUTE.uml_attribute as UMLAttribute

######################################################################
# TEST CASES FOR CLASS FUNCTIONS #
######################################################################


class TestUMLAttributeAdd(unittest.TestCase):

    def setUp(self):
        """
        This method runs before each test. It automatically sets up some default classes
        and clears the relationship list.
        """
        # Mock the relationship_list and class_and_attr_list
        UMLAttribute.class_list = ["chicken", "person"]
        UMLAttribute.class_and_attr_list = [
            {"class_name": "chicken", 
             "attr_list": [
                 {"attr_name": "heart"},
                 {"attr_name": "lungs"}]},
            {"class_name": "person",
             "attr_list": []}
        ]

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_empty_class_name(self, mock_user_choice):
        """Test case for empty class name"""
        class_name = "chicken"
        attr_name = ""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.add_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, "Invalid length. Must be between 2 and 50 characters.")

    ######################################################################
    # TEST ADDING CLASS #
    
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_valid_attribute(self, mock_user_choice):
        """Test Case 1: Add a valid attribute to class with no attributes"""
        # Expected: Attribute 'heart' was successfully added to class 'person'!
        class_name = "person"
        attr_name = "heart"
        # Check if correct messaged printed
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.add_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Attribute '{attr_name}' was successfully added to class '{class_name}'!")
        attr_list = UMLAttribute.get_attr_list(class_name)
        # Check if attribute exists in list
        self.assertIn({'attr_name': attr_name}, attr_list)

    
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_valid_attribute2(self, mock_user_choice):
        """Test Case 2: Add a valid attribute to class with existing attributes"""
        # Expected: Attribute 'eyes' was successfully added to class 'chicken'!
        class_name = "chicken"
        attr_name = "eyes"
        # Check if correct messaged printed
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.add_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Attribute '{attr_name}' was successfully added to class '{class_name}'!")
        attr_list = UMLAttribute.get_attr_list(class_name)
        # Check if attribute is in attr_list
        self.assertIn({'attr_name': attr_name}, attr_list)


    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=False)
    def test_add_attr_cancel(self, mock_user_choice):
        """Test Case 3: Cancel adding a valid attribute"""
        # Expected: No output, attribute should not be in class
        class_name = "chicken"
        attr_name = "tail"
        UMLAttribute.add_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_invalid_attribute(self, mock_user_choice):
        """Test Case 4: Try to add attribute with invalid characters (numbers)"""
        # Expected: Invalid format. Only lowercase alphabet characters are allowed.
        class_name = "chicken"
        attr_name = "123beak"
        # Check if correct messaged printed
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.add_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, "Invalid format. Only lowercase alphabet characters are allowed.")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_invalid_attribute2(self, mock_user_choice):
        """Test Case 5: Try to add attribute with invalid characters (special characters)"""
        # Expected: Invalid format. Only lowercase alphabet characters are allowed.
        class_name = "chicken"
        attr_name = "!beak@$#"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.add_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, "Invalid format. Only lowercase alphabet characters are allowed.")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_invalid_attribute3(self, mock_user_choice):
        """Test Case 6: Try to add attribute with invalid characters (numbers and special characters)"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        class_name = "chicken"
        attr_name = "!@$beak125"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.add_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, "Invalid format. Only lowercase alphabet characters are allowed.")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_attr_exist_already(self, mock_user_choice, mock_user_choice2):
        """Test Case 7: Try to add an attribute that already exists"""
        class_name = "chicken"
        attr_name = "heart"
        # Expected: Attribute 'feathers' already existed in class 'chicken'.
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.add_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Attribute '{attr_name}' already existed in class '{class_name}'!")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_attr_class_not_exist(self, mock_user_choice):
        """Test Case 8: Try to add attribute to a class that doesn't exist"""
        # Expected: Class 'chick' not found!
        class_name = "chick"
        attr_name = "tail"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.add_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Class '{class_name}' not found!")
        self.assertNotIn(class_name, UMLAttribute.class_list)

    ######################################################################
    ######################################################################
    # TEST DELETE ATTRIBUTE #
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_that_exists(self, mock_user_choice):
        """Test Case 9: Delete a valid attribute"""
        # Expected: Attribute 'heart' was successfully deleted from class 'chicken'!
        class_name = "chicken"
        attr_name = "heart"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.delete_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Attribute '{attr_name}' was successfully deleted from class '{class_name}'!")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_invalid(self, mock_user_choice):
        """Test Case 10: Delete an attribute with invalid characters (numbers and special characters)"""
        # Expected: Invalid format. Only lowercase alphabet characters are allowed.
        class_name = "chicken"
        attr_name = "123beak$@#"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.delete_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, "Invalid format. Only lowercase alphabet characters are allowed.")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_not_exist(self, mock_user_choice):
        """Test Case 11: Try to delete an attribute that does not exist inside a class"""
        # Expected: Attribute 'feather' not found in class 'chicken'!
        class_name = "chicken"
        attr_name = "feather"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.delete_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Attribute '{attr_name}' not found in class '{class_name}'!")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_class_not_exist(self, mock_user_choice):
        """Test Case 12: Try to delete an attribute from a class that does not exist"""
        # Expected: Class 'chick' not found!
        class_name = "chick"
        attr_name = "feather"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.delete_attr(class_name, attr_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Class '{class_name}' not found!")
        self.assertNotIn(class_name, UMLAttribute.class_list)


    ######################################################################
    # TEST RENAME CLASS #
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_rename_attr_that_exists(self, mock_user_choice):
        """Test Case 13: Rename an existing valid attribute to a new valid attribute"""
        # Expected: Attribute 'feathers' was renamed to 'tail' in class 'chicken'!
        class_name = "chicken"
        attr_name = "heart"
        new_name = "tail"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.rename_attr(class_name, attr_name, new_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Attribute '{attr_name}' was renamed to '{new_name}' in class '{class_name}'!")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertIn({"attr_name": new_name}, attr_list)
        self.assertNotIn({"attr_name": attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_rename_attr_that_not_exist(self, mock_user_choice):
        """Test Case 14: Try to rename a non-existent attribute to a new name"""
        # Expected: Attribute 'feathers' not found in class 'chicken'!
        class_name = "chicken"
        attr_name = "feathers"
        new_name = "beak"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.rename_attr(class_name, attr_name, new_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Attribute '{attr_name}' not found in class '{class_name}'!")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({"attr_name": new_name}, attr_list)
        self.assertNotIn({"attr_name": attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_rename_attr_to_already_exist(self, mock_user_choice):
        """Test Case 15: Try to rename an existing attribute to a name that already exists"""
        # Expected: Attribute 'tail' already existed in class 'chicken'!
        class_name = "chicken"
        attr_name = "heart"
        new_name = "lungs"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            UMLAttribute.rename_attr(class_name, attr_name, new_name)
            printed_output = mock_stdout.getvalue().strip()
        self.assertEqual(printed_output, f"Attribute '{new_name}' already existed in class '{class_name}'!")
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertIn({"attr_name": new_name}, attr_list)
        self.assertIn({"attr_name": attr_name}, attr_list)


if __name__ == "__main__":
    unittest.main()
