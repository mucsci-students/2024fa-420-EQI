import sys
import os
import pytest

# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter

###############################################################################

@pytest.fixture
def uml_parameter():
    # Fixture to set up an instance of UMLParameter for testing
    return UMLParameter(type="int", parameter_name="paramA")

def test_get_parameter_name(uml_parameter):
    # Test getting the parameter name
    assert uml_parameter._get_parameter_name() == "paramA"

def test_set_parameter_name(uml_parameter):
    # Test setting a new parameter name
    uml_parameter._set_parameter_name("newParam")
    assert uml_parameter._get_parameter_name() == "newParam"

def test_get_type(uml_parameter):
    # Test getting the parameter type
    assert uml_parameter._get_type() == "int"

def test_set_type(uml_parameter):
    # Test setting a new parameter type
    uml_parameter._set_type("string")
    assert uml_parameter._get_type() == "string"

def test_str(uml_parameter):
    # Test string representation of the parameter
    assert str(uml_parameter) == "int paramA"

def test_convert_to_json_parameter(uml_parameter):
    # Test conversion of UMLParameter to JSON format
    json_data = uml_parameter._convert_to_json_parameter()
    
    expected_json = {
        "name": "paramA",
        "type": "int"
    }
    
    assert json_data == expected_json