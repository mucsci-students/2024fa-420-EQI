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

###############################################################################

@pytest.fixture
def uml_class():
    # Fixture to set up an instance of UMLClass for testing
    return UMLClass("TestClass")

@pytest.fixture
def sample_field():
    # Fixture to create a UMLField object
    return Field(type="int", field_name="sample_field")

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

def test_set_class_method_list(uml_class):
    # Create a sample method to add to the method list
    sample_method = Method(type="void", method_name="sampleMethod")
    
    # Set the method list
    uml_class._set_class_method_list([sample_method])
    
    # Since the method list is stored as a dictionary with parameters, check the method name
    assert sample_method._get_name() == "sampleMethod"

def test_convert_to_json_uml_class(uml_class):
    # Test conversion of UMLClass to JSON format
    json_data = uml_class._convert_to_json_uml_class()
    
    # Verify the structure and contents of the JSON
    expected_json = {
        "name": "TestClass",
        "fields": [],
        "methods": []
    }
    
    assert json_data == expected_json

def test_str(uml_class):
    # Test string representation of the class
    assert str(uml_class) == "Class name: TestClass"