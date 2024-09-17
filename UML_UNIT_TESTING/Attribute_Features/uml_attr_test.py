import os
import sys
import unittest
from unittest.mock import patch

# Add the root directory of the project to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

import UML_CORE.UML_CLASS.uml_class as UMLClass
import UML_CORE.UML_ATTRIBUTE.uml_attribute as UMLAttribute

######################################################################
# TEST CASES FOR CLASS FUNCTIONS #
######################################################################


class TestUMLAttributeAdd(unittest.TestCase):

    ######################################################################
    # TEST ADDING CLASS #
    
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_valid_attribute(self, mock_user_choice):
        """Test Case 1: Add a valid attribute to class with no attributes"""
        # Expected: Added attribute 'beak' successfully to class 'chicken!
        class_name = "chicken"
        attr_name = "beak"
        UMLAttribute.add_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertIn({'attr_name': attr_name}, attr_list)

    
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_valid_attribute2(self, mock_user_choice):
        """Test Case 2: Add a valid attribute to class with existing attributes"""
        # Expected: Added attribute 'eyes' successfully to class 'chicken!
        class_name = "chicken"
        attr_name = "eyes"
        UMLAttribute.add_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertIn({'attr_name': attr_name}, attr_list)


    @patch("UML_CORE.UML_CLASS.uml_class.user_choice", return_value=True)
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=False)
    def test_add_attr_cancel(self, mock_user_choice, mock_user_choice2):
        UMLClass.add_class("chicken")
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
        # Expected: Invalid format. Only alphabet characters are allowed.
        class_name = "chicken"
        attr_name = "123beak"
        UMLAttribute.add_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_invalid_attribute2(self, mock_user_choice):
        """Test Case 5: Try to add attribute with invalid characters (special characters)"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        class_name = "chicken"
        attr_name = "!beak@$#"
        UMLAttribute.add_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_invalid_attribute3(self, mock_user_choice):
        """Test Case 6: Try to add attribute with invalid characters (numbers and special characters)"""
        # Expected: Invalid format. Only alphabet characters are allowed.
        class_name = "chicken"
        attr_name = "!@$beak125"
        UMLAttribute.add_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_attr_exist_already(self, mock_user_choice, mock_user_choice2):
        """Test Case 7: Try to add an attribute that already exists"""
        class_name = "chicken"
        attr_name = "feathers"
        UMLAttribute.add_attr(class_name, attr_name)
        # Expected: Attribute 'feathers' already existed in class 'chicken'.
        UMLAttribute.add_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_add_attr_class_not_exist(self, mock_user_choice):
        """Test Case 8: Try to add attribute to a class that doesn't exist"""
        # Expected: Class 'chick' not found!
        class_name = "chick"
        attr_name = "tail"
        UMLAttribute.add_attr(class_name, attr_name)
        self.assertNotIn(class_name, UMLClass.class_list)

    ######################################################################
    ######################################################################
    # TEST DELETE ATTRIBUTE #
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_that_exists(self, mock_user_choice):
        """Test Case 9: Delete a valid attribute"""
        # Expected: Successfully removed attribute 'beak' was successfully deleted from class 'chicken'!
        class_name = "chicken"
        attr_name = "beak"
        UMLAttribute.delete_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_invalid(self, mock_user_choice):
        """Test Case 10: Delete an attribute with invalid characters (numbers and special characters)"""
        # Expected: Invalid format. Only lowercase alphabet characters are allowed.
        class_name = "chicken"
        attr_name = "123beak$@#"
        UMLAttribute.delete_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_not_exist(self, mock_user_choice):
        """Test Case 11: Try to delete an attribute that does not exist inside a class"""
        # Expected: Attribute 'feather' not found in class 'chicken'!
        class_name = "chicken"
        attr_name = "feather"
        UMLAttribute.delete_attr(class_name, attr_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({'attr_name': attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_delete_attr_class_not_exist(self, mock_user_choice):
        """Test Case 12: Try to delete an attribute from a class that does not exist"""
        # Expected: Class 'chick' not found!
        class_name = "chick"
        attr_name = "feather"
        UMLAttribute.delete_attr(class_name, attr_name)
        self.assertNotIn(class_name, UMLClass.class_list)


    ######################################################################
    # TEST RENAME CLASS #
    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_rename_attr_that_exists(self, mock_user_choice):
        """Test Case 13: Rename an existing valid attribute to a new valid attribute"""
        # Expected: Attribute 'feathers' was renamed to 'tail' in class 'chicken'!
        class_name = "chicken"
        attr_name = "feathers"
        new_name = "tail"
        UMLAttribute.rename_attr(class_name, attr_name, new_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertIn({"attr_name": new_name}, attr_list)
        self.assertNotIn({"attr_name": attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_rename_attr_that_not_exist(self, mock_user_choice):
        """Test Case 14: Try to rename a non-existent attribute to a new name"""
        # Expected: Attribute 'feathers' not found in class 'chicken'!
        class_name = "chicken"
        attr_name = "feathers"
        new_name = "heart"
        UMLAttribute.rename_attr(class_name, attr_name, new_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertNotIn({"attr_name": new_name}, attr_list)
        self.assertNotIn({"attr_name": attr_name}, attr_list)

    @patch("UML_CORE.UML_ATTRIBUTE.uml_attribute.user_choice", return_value=True)
    def test_rename_attr_to_already_exist(self, mock_user_choice):
        """Test Case 15: Try to rename an existing attribute to a name that already exists"""
        # Expected: Attribute 'tail' already existed in class 'chicken'!
        class_name = "chicken"
        attr_name = "eyes"
        new_name = "tail"
        UMLAttribute.rename_attr(class_name, attr_name, new_name)
        attr_list = UMLAttribute.get_attr_list(class_name)
        self.assertIn({"attr_name": new_name}, attr_list)
        self.assertIn({"attr_name": attr_name}, attr_list)


if __name__ == "__main__":
    unittest.main()
