import sys
import os
import pytest

###############################################################################
# ADD ROOT PATH #
# Adjusting the path to allow imports from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Testing Module
from UML_CORE.UML_METHOD.uml_method import UMLMethod

###############################################################################

@pytest.fixture
def uml_method():
    # Fixture to set up an instance of UMLMethod for testing
    return UMLMethod(type="void", method_name="testMethod")

def test_get_method_name(uml_method):
    # Test getting the method name
    assert uml_method._get_name() == "testMethod"

def test_set_method_name(uml_method):
    # Test setting a new method name
    uml_method._set_name("newMethodName")
    assert uml_method._get_name() == "newMethodName"

def test_get_method_type(uml_method):
    # Test getting the method type
    assert uml_method._get_type() == "void"

def test_set_method_type(uml_method):
    # Test setting a new method type
    uml_method._set_type("int")
    assert uml_method._get_type() == "int"

def test_str(uml_method):
    # Test string representation of the method
    assert str(uml_method) == "void testMethod"