# Because UML_UNIT_TESTING directory is at the same level as UML_CORE, so I had some problem
# with importing UML_CORE.UML_CLASS.uml_class.
# Then I had to ask ChatGPT how to access, and below is how it shows me how to solve this problem
# This is the only file that we need to do this because of the two reasons below:
#
# 1/ We are not going to run the program in UML_ATTRIBUTE, UML_CLASS,  UML_RELATIONSHIP and UML_MANAGEMENT
# 2/ We only run the test inside UML_UNIT_TESTING.uml_unit_test.py

import os
import sys
import unittest

# Add the project root directory to sys.path (ChatGPT instruction)
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # This must be placed first before importing
from UML_CORE.UML_CLASS.uml_class import UMLClass


class TestUMLClass(unittest.TestCase):
    def test_create_uml_class(self):
        # Test case: Create a UMLClass object and check if it is created successfully
        class_name = "Person"
        uml_class = UMLClass(class_name)

        # Print expected and result
        self.__print_class_creation_message(class_name, uml_class)

        # Check if the class is created successfully
        self.assertIsNotNone(uml_class, "Failed to create UMLClass object.")

        # Check if the object is of type UMLClass
        self.assertIsInstance(uml_class, UMLClass, "Object is not of type UMLClass.")

    def test_class_name(self):
        # Test case: Create a UMLClass and verify the class name
        class_name = "Person"
        uml_class = UMLClass(class_name)

        # Print expected and result
        self.__print_class_name_message(class_name, uml_class)

        # Check if the class name is set correctly
        self.assertEqual(
            uml_class._get_class_name(), class_name, "Class name is incorrect."
        )

    def test_initial_empty_attribute_list(self):
        # Test case: Check that attribute list is initially empty
        class_name = "Person"
        uml_class = UMLClass(class_name)

        # Print expected and result
        self.__print_empty_attribute_list_message(class_name, uml_class)

        # Check if attribute list is empty
        self.assertEqual(
            uml_class._get_class_attribute_list(),
            [],
            "Attribute list is not empty initially.",
        )

    def test_initial_empty_relationship_list(self):
        # Test case: Check that relationship list is initially empty
        class_name = "Person"
        uml_class = UMLClass(class_name)

        # Print expected and result
        self.__print_empty_relationship_list_message(class_name, uml_class)

        # Check if relationship list is empty
        self.assertEqual(
            uml_class._get_class_relationship_list(),
            [],
            "Relationship list is not empty initially.",
        )

    # Print Message Methods #
    def __print_class_creation_message(self, class_name: str, class_object: UMLClass):
        expected_class_type = "<class 'UML_CORE.UML_CLASS.uml_class.UMLClass'>"
        print("\nTesting Class Creation")
        print(f"Expected Class Type: {expected_class_type}")
        print(f"Result Class Type: {type(class_object)}")

    def __print_class_name_message(self, class_name: str, class_object: UMLClass):
        print("\nTesting Class Name")
        print(f"Expected Class Name: {class_name}")
        print(f"Result Class Name: {class_object._get_class_name()}")

    def __print_empty_attribute_list_message(
        self, class_name: str, class_object: UMLClass
    ):
        empty_list_sign = "[]"
        print("\nTesting Class Initial Empty Attribute List")
        print(f"Expected Initial Attribute List: {empty_list_sign}")
        print(
            f"Result Initial Attribute List: {class_object._get_class_attribute_list()}"
        )

    def __print_empty_relationship_list_message(
        self, class_name: str, class_object: UMLClass
    ):
        empty_list_sign = "[]"
        print("\nTesting Class Initial Empty Relationship List")
        print(f"Expected Initial Relationship List: {empty_list_sign}")
        print(
            f"Result Initial Relationship List: {class_object._get_class_relationship_list()}"
        )


# Run the tests
if __name__ == "__main__":
    # The main() function here is a function in "unittest" module
    unittest.main()
