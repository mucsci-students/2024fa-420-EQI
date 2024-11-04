import sys
import os
import pytest
from typing import List, Dict

###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_CORE.UML_CLASS.uml_class import UMLClass
from UML_CORE.UML_FIELD.uml_field import UMLField as Field
from UML_CORE.UML_METHOD.uml_method import UMLMethod as Method
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter as Parameter

###############################################################################

@pytest.fixture
def uml_class():
    # Fixture to set up an instance of UMLClass for testing
    return UMLClass("TestClass")

@pytest.fixture
def sample_field():
    # Fixture to create a UMLField object
    return Field(type="int", field_name="sample_field")

@pytest.fixture
def sample_method():
    # Fixture to create a UMLMethod object
    return Method(type="void", method_name="sampleMethod")

@pytest.fixture
def sample_parameter():
    # Fixture to create a UMLParameter object
    return Parameter(type="int", parameter_name="sampleParam")

###############################################################################

def test_get_class_name(uml_class):
    # Test getting the class name
    assert uml_class._get_class_name() == "TestClass"

def test_set_class_name(uml_class):
    # Test setting a new class name
    uml_class._set_class_name("NewClassName")
    assert uml_class._get_class_name() == "NewClassName"

def test_get_class_field_list(uml_class):
    # Test getting the class field list (initially empty)
    assert uml_class._get_class_field_list() == []

def test_set_class_field_list(uml_class, sample_field):
    # Test setting a new class field list
    uml_class._set_class_field_list([sample_field])
    assert uml_class._get_class_field_list() == [sample_field]

def test_get_method_and_parameters_list(uml_class):
    # Test getting the method and parameters list (initially empty)
    assert uml_class._get_method_and_parameters_list() == []

def test_get_position():
    # Reset position to ensure consistent test results
    UMLClass._UMLClass__last_x = 0
    UMLClass._UMLClass__last_y = 0

    # Create an instance of UMLClass with default position
    uml_class = UMLClass(class_name="TestClass")

    # Check if the position is as expected
    expected_position = {'x': 0, 'y': 0}  # Starting position after reset
    assert uml_class._get_position() == expected_position


def test_convert_to_json_uml_class():
    # Reset position to ensure consistent test results
    UMLClass._UMLClass__last_x = 0
    UMLClass._UMLClass__last_y = 0

    # Create an instance of UMLClass with known data
    uml_class = UMLClass(class_name="TestClass")

    # Test conversion of UMLClass to JSON format
    json_data = uml_class._convert_to_json_uml_class()

    # Expected JSON structure
    expected_json = {
        "name": "TestClass",
        "fields": [],
        "methods": [],
        "position": {'x': 0, 'y': 0}  # Starting position after reset
    }

    assert json_data == expected_json

def test_str(uml_class):
    # Test string representation of the class
    assert str(uml_class) == "Class name: TestClass"

###############################################################################
# Additional Tests for Comprehensive Coverage

def test_add_field_to_class_field_list(uml_class, sample_field):
    # Test adding a single field to class field list
    uml_class._set_class_field_list([sample_field])
    assert len(uml_class._get_class_field_list()) == 1
    assert uml_class._get_class_field_list()[0]._get_name() == "sample_field"

def test_clear_class_field_list(uml_class):
    # Test clearing the class field list
    uml_class._set_class_field_list([])
    assert uml_class._get_class_field_list() == []

def test_modify_class_name_after_initialization(uml_class):
    # Test modifying the class name after initialization
    uml_class._set_class_name("ModifiedClassName")
    assert uml_class._get_class_name() == "ModifiedClassName"

def test_empty_class_json_conversion():
    # Reset position to ensure consistent test results
    UMLClass._UMLClass__last_x = 0
    UMLClass._UMLClass__last_y = 0

    # Test JSON conversion for an empty UMLClass instance
    empty_class = UMLClass()
    json_data = empty_class._convert_to_json_uml_class()
    expected_json = {
        "name": "",
        "fields": [],
        "methods": [],
        "position": {'x': 0, 'y': 0}  # Adjust to the expected initial position
    }
    assert json_data == expected_json

def test_add_multiple_fields(uml_class, sample_field):
    field2 = Field(type="string", field_name="sample_field_2")
    uml_class._set_class_field_list([sample_field, field2])
    assert len(uml_class._get_class_field_list()) == 2
    assert uml_class._get_class_field_list()[1]._get_name() == "sample_field_2"

def test_set_empty_class_name(uml_class):
    uml_class._set_class_name("")
    assert uml_class._get_class_name() == ""

def test_set_empty_field_name(uml_class, sample_field):
    sample_field._set_name("")
    uml_class._set_class_field_list([sample_field])
    assert uml_class._get_class_field_list()[0]._get_name() == ""

def test_set_position():
    # Create an instance of UMLClass with default position
    uml_class = UMLClass(class_name="TestClass")

    # Set a new position
    new_x, new_y = 50, 100
    uml_class._set_position(new_x, new_y)

    # Verify that the position has been updated
    expected_position = {'x': new_x, 'y': new_y}
    assert uml_class._get_position() == expected_position

