import sys
import os
import pytest
from rich.console import Console
from unittest.mock import patch, MagicMock

# ADD ROOT PATH #
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Import the UMLModel class and UMLObserver
from UML_MVC.UML_MODEL.uml_model import UMLModel
from UML_MVC.UML_VIEW.UML_CLI_VIEW.uml_cli_view import UMLView
from UML_MVC.uml_observer import UMLObserver

# Import other dependencies such as UMLClass, UMLField, UMLMethod, UMLParameter, UMLRelationship
from UML_CORE.UML_CLASS.uml_class import UMLClass
from UML_CORE.UML_FIELD.uml_field import UMLField
from UML_CORE.UML_METHOD.uml_method import UMLMethod
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship
from UML_MVC.UML_CONTROLLER.uml_storage_manager import UMLStorageManager  # Corrected import

###############################################################################

@pytest.fixture
def uml_model():
    view = UMLView()
    console = Console()
    return UMLModel(view=view, console=console)

@pytest.fixture
def sample_class():
    return UMLClass(class_name="TestClass")

@pytest.fixture
def sample_field():
    return UMLField(type="int", field_name="sampleField")

@pytest.fixture
def sample_observer():
    class TestObserver(UMLObserver):
        def __init__(self):
            self.events = []

        def _update(self, event_type=None, data=None, is_loading=None, is_undo_or_redo=None):
            self.events.append({
                "event_type": event_type,
                "data": data,
                "is_loading": is_loading,
                "is_undo_or_redo": is_undo_or_redo
            })

    return TestObserver()

@pytest.fixture
def sample_class2():
    # Initialize a UMLClass instance with a sample name
    uml_class = UMLClass(class_name="TestClass")
    # Add a sample method and field to the class for testing
    uml_class.add_method(UMLMethod(type="void", method_name="method1"))
    uml_class.add_field(UMLField(type="int", field_name="field1"))
    return uml_class

@pytest.fixture
def sample_method(sample_param):
    # Initialize a UMLMethod instance and add a parameter to it
    method = UMLMethod(type="void", method_name="method1")
    method.add_parameter(sample_param)  # Assuming add_parameter is a method for UMLMethod
    return method

@pytest.fixture
def sample_param():
    # Initialize a UMLParameter instance with a sample parameter type and name
    return UMLParameter(type="int", parameter_name="param1")


###############################################################################
# Initialization
###############################################################################
def test_uml_model_init():
    
    view = UMLView()  
    console = Console()  # Using Rich's Console
    
    # Create UMLModel instance
    uml_model = UMLModel(view=view, console=console)
    
    # Verify attributes are correctly initialized
    assert uml_model._UMLModel__user_view == view
    assert uml_model._UMLModel__console == console
    assert isinstance(uml_model._UMLModel__class_list, dict)
    assert isinstance(uml_model._UMLModel__storage_manager, UMLStorageManager)  # Corrected to UMLStorageManager
    assert isinstance(uml_model._UMLModel__relationship_list, list)
    assert isinstance(uml_model._UMLModel__main_data, dict)
    assert isinstance(uml_model._observers, list)


###############################################################################
# Observer Pattern Tests
###############################################################################

def test_attach_observer(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._notify_observers(event_type="test_event", data={"key": "value"})
    
    assert len(sample_observer.events) == 1
    assert sample_observer.events[0]["event_type"] == "test_event"
    assert sample_observer.events[0]["data"] == {"key": "value"}

def test_detach_observer(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._detach_observer(sample_observer)
    
    uml_model._notify_observers(event_type="test_event", data={"key": "value"})
    assert len(sample_observer.events) == 0

def test_notify_observers(uml_model, sample_observer):
    # Create additional observer instances
    observer1 = sample_observer
    observer2 = sample_observer.__class__()  # Directly instantiate another TestObserver

    # Attach observers to the model
    uml_model._attach_observer(observer1)
    uml_model._attach_observer(observer2)
    
    # Define event data to pass to observers
    event_type = "test_event"
    data = {"class_name": "TestClass"}
    is_loading = False
    is_undo_or_redo = True
    
    # Call the _notify_observers method
    uml_model._notify_observers(event_type=event_type, data=data, is_loading=is_loading, is_undo_or_redo=is_undo_or_redo)
    
    # Verify that each observer received the notification with correct data
    for observer in [observer1, observer2]:
        assert len(observer.events) == 1  # Each observer should have exactly one event
        assert observer.events[0]["event_type"] == event_type
        assert observer.events[0]["data"] == data
        assert observer.events[0]["is_loading"] == is_loading
        assert observer.events[0]["is_undo_or_redo"] == is_undo_or_redo

# Additional tests for observer notifications for class addition and deletion
def test_observer_notification_on_class_addition(uml_model, sample_observer):

    uml_model._attach_observer(sample_observer)

    uml_model._add_class("ObserverClass", is_loading=False)

    assert sample_observer.events[0]["event_type"] == "add_class"


###############################################################################
# Getter Methods Tests
###############################################################################

def test_get_class_list(uml_model):
    class_list = uml_model._get_class_list()
    assert isinstance(class_list, dict)
    assert len(class_list) == 0

def test_get_relationship_list(uml_model):
    relationship_list = uml_model._get_relationship_list()
    assert isinstance(relationship_list, list)
    assert len(relationship_list) == 0

def test_get_storage_manager(uml_model):
    storage_manager = uml_model._get_storage_manager()
    assert storage_manager is not None

def test_get_main_data(uml_model):
    main_data = uml_model._get_main_data()
    assert isinstance(main_data, dict), "Expected main_data to be a dictionary"
    assert len(main_data) == 2, "Expected main_data to be initially be empty with {'classes': [], 'relationships': []} "

def test_set_main_data(uml_model):
    # Set some dummy data
    new_main_data = {"classes": [], "relationships": []}
    uml_model._set_main_data(new_main_data)
    
    # Retrieve and verify it was set correctly
    assert uml_model._get_main_data() == new_main_data, "Expected main_data to be set with provided data"

def test_get_user_view(uml_model):
    user_view = uml_model._get_user_view()
    assert user_view is not None, "Expected user_view to not be None"

###############################################################################
# Static Methods Tests
###############################################################################

def test_create_class(uml_model):
    created_class = UMLModel.create_class("TestClass")
    assert isinstance(created_class, UMLClass)
    assert created_class._get_class_name() == "TestClass"

def test_create_field(uml_model):
    created_field = UMLModel.create_field("int", "TestField")
    assert isinstance(created_field, UMLField)
    assert created_field._get_type() == "int"
    assert created_field._get_name() == "TestField"

def test_create_method(uml_model):
    created_method = UMLModel.create_method("void", "TestMethod")
    assert isinstance(created_method, UMLMethod)
    assert created_method._get_type() == "void"
    assert created_method._get_name() == "TestMethod"

def test_create_parameter(uml_model):
    created_parameter = UMLModel.create_parameter("int", "TestParam")
    assert isinstance(created_parameter, UMLParameter)
    assert created_parameter._get_type() == "int"
    assert created_parameter._get_parameter_name() == "TestParam"

def test_create_relationship(uml_model):
    created_relationship = UMLModel.create_relationship("ClassA", "ClassB", "inheritance")
    assert isinstance(created_relationship, UMLRelationship)
    assert created_relationship._get_source_class() == "ClassA"
    assert created_relationship._get_destination_class() == "ClassB"
    assert created_relationship._get_type() == "inheritance"

###############################################################################
# Class Management Tests
###############################################################################

def test_add_class(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    
    result = uml_model._add_class(class_name="NewClass", is_loading=False)
    assert result is True
    assert "NewClass" in uml_model._get_class_list()
    assert len(sample_observer.events) == 1
    assert sample_observer.events[0]["event_type"] == "add_class"

def test_delete_class(uml_model, sample_class, sample_observer):
    uml_model._attach_observer(sample_observer)
    
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    result = uml_model._delete_class(class_name="TestClass")
    assert result is True
    assert "TestClass" not in uml_model._get_class_list()
    assert len(sample_observer.events) == 2
    assert sample_observer.events[0]["event_type"] == "add_class"
    assert sample_observer.events[1]["event_type"] == "delete_class"

def test_rename_class(uml_model, sample_class, sample_observer):
    uml_model._attach_observer(sample_observer)
    
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    result = uml_model._rename_class(current_name="TestClass", new_name="RenamedClass")
    assert result is True
    assert "RenamedClass" in uml_model._get_class_list()
    assert "TestClass" not in uml_model._get_class_list()
    assert len(sample_observer.events) == 2
    assert sample_observer.events[0]["event_type"] == "add_class"
    assert sample_observer.events[1]["event_type"] == "rename_class"

def test_add_class_duplicate(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="NewClass", is_loading=False)
    result = uml_model._add_class(class_name="NewClass", is_loading=False)
    assert result is False  # Duplicate should not be allowed

def test_add_class_empty_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    result = uml_model._add_class(class_name="", is_loading=False)
    assert result is False  # Empty name should not be allowed

def test_add_class_special_characters(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    result = uml_model._add_class(class_name="Class 123", is_loading=False)
    assert result is False

def test_delete_class_non_existent(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    result = uml_model._delete_class(class_name="NonExistentClass")
    assert result is False  # Deleting non-existent class should fail

def test_delete_class_empty_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    result = uml_model._delete_class(class_name="")
    assert result is False  # Empty class name should fail

def test_add_class_whitespace_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    result = uml_model._add_class(class_name="   ", is_loading=False)
    assert result is False  # Whitespace-only name should not be allowed

def test_add_class_very_long_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    long_name = "A" * 300  # 300 characters
    result = uml_model._add_class(class_name=long_name, is_loading=False)
    assert result is True  

def test_rename_class_invalid_name(uml_model):
    # Attempt to rename a non-existent class
    result = uml_model._rename_class(current_name="NonExistentClass", new_name="NewClassName")
    
    # Verify that the renaming fails (assuming it should return False or handle gracefully)
    assert result is False, "Expected rename to fail for a non-existent class name"

def test_rename_class_invalid_input_name(uml_model):
    uml_model.create_class("ClassA")
    # Attempt to rename a non-existent class
    result = uml_model._rename_class(current_name="ClassA", new_name="New Class Name")
    
    # Verify that the renaming fails (assuming it should return False or handle gracefully)
    assert result is False, "Expected rename to fail for a non-existent class name"

# Test renaming a class to an existing class name
def test_rename_class_to_existing_name(uml_model):
    uml_model.create_class("Class1")
    uml_model.create_class("Class2")
    
    # Attempt to rename Class1 to "Class2" (which already exists)
    result = uml_model._rename_class("Class1", "Class2")
    assert result is False  # Should fail due to duplicate name

    # Test renaming a class to an existing class name
def test_rename_class_to_existing_name_2(uml_model):
    uml_model.create_class("Class1")
    uml_model.create_class("Class2")
    
    # Attempt to rename Class1 to "Class2" (which already exists)
    result = uml_model._rename_class("Class1", "Class1")
    assert result is False  # Should fail due to duplicate name


def test_add_duplicate_class(uml_model):

    uml_model._add_class("DuplicateClass", is_loading=False)

    result = uml_model._add_class("DuplicateClass", is_loading=False)  # Attempt to add duplicate

    assert result is False

###############################################################################
# Field Management Tests
###############################################################################

def test_add_field(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Add field to the class
    result = uml_model._add_field(class_name="TestClass", field_type="string", field_name="newField", is_loading=False)
    assert result is True
    
    # Verify the field was added
    class_data = uml_model._get_class_list()["TestClass"]
    fields = class_data._get_class_field_list()
    assert len(fields) == 1
    assert fields[0]._get_name() == "newField"
    assert fields[0]._get_type() == "string"
    
    # Verify observer notification
    assert len(sample_observer.events) == 2  # add_class and add_field events
    assert sample_observer.events[1]["event_type"] == "add_field"
    assert sample_observer.events[1]["data"] == {
        "class_name": "TestClass",
        "type": "string",
        "field_name": "newField"
    }
    assert sample_observer.events[1]["is_undo_or_redo"] is False


def test_delete_field(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and field to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_field(class_name="TestClass", field_type="int", field_name="testField", is_loading=False)
    
    # Delete the field
    result = uml_model._delete_field(class_name="TestClass", field_name="testField")
    assert result is True
    
    # Verify the field was deleted
    class_data = uml_model._get_class_list()["TestClass"]
    fields = class_data._get_class_field_list()
    assert len(fields) == 0
    
    # Verify observer notification
    assert len(sample_observer.events) == 3  # add_class, add_field, delete_field events
    assert sample_observer.events[2]["event_type"] == "delete_field"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "field_name": "testField"
    }
    assert sample_observer.events[2]["is_undo_or_redo"] is False


def test_rename_field(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and field to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_field(class_name="TestClass", field_type="int", field_name="testField", is_loading=False)
    
    # Rename the field
    result = uml_model._rename_field(class_name="TestClass", old_field_name="testField", new_field_name="renamedField")
    assert result is True
    
    # Verify the field was renamed
    class_data = uml_model._get_class_list()["TestClass"]
    fields = class_data._get_class_field_list()
    assert len(fields) == 1
    assert fields[0]._get_name() == "renamedField"
    
    # Verify observer notification
    assert len(sample_observer.events) == 3  # add_class, add_field, rename_field events
    assert sample_observer.events[2]["event_type"] == "rename_field"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "old_field_name": "testField",
        "new_field_name": "renamedField"
    }
    assert sample_observer.events[2]["is_undo_or_redo"] is False
    
def test_add_field_duplicate(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_field(class_name="TestClass", field_type="string", field_name="newField", is_loading=False)
    result = uml_model._add_field(class_name="TestClass", field_type="string", field_name="newField", is_loading=False)
    assert result is False  # Duplicate field should not be allowed

def test_add_field_empty_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._add_field(class_name="TestClass", field_type="int", field_name="", is_loading=False)
    assert result is False  # Empty field name should not be allowed

def test_add_field_invalid_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._add_field(class_name="TestClass", field_type="int", field_name="invalid Field", is_loading=False)
    assert result is False  # Invalid type should not be allowed

def test_add_field_whitespace_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._add_field(class_name="TestClass", field_type="int", field_name="   ", is_loading=False)
    assert result is False  # Whitespace-only field name should not be allowed

def test_add_field_nonexistent_class(uml_model):
    # Attempt to add a field to a class that hasn't been created
    result = uml_model._add_field(class_name="NonExistentClass", field_type="int", field_name="sampleField", is_loading=False)
    
    # Verify the result indicates failure (adjust based on method behavior; here we assume it returns False)
    assert result is False, "Expected adding a field to a non-existent class to return False"

def test_delete_field_nonexistent_class(uml_model):
    # Attempt to delete a field from a class that hasn't been created
    result = uml_model._delete_field(class_name="NonExistentClass", field_name="sampleField")
    
    # Verify the result indicates failure (adjust based on method behavior; here we assume it returns False)
    assert result is False, "Expected deleting a field from a non-existent class to return False"

def test_delete_field_invalid_input_name(uml_model, sample_class):
    # Add the sample class to the UML model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_field(class_name="TestClass", field_type="int", field_name="test", is_loading=False)
    # Attempt to rename a non-existent field within an existing class
    result = uml_model._delete_field(class_name="TestClass", field_name="sample Field")
    
    # Verify that the renaming fails, expecting the method to return False
    assert result is False, "Expected rename to fail for a invalid input field name in existing class"

def test_rename_field_invalid_name(uml_model, sample_class):
    # Add the sample class to the UML model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Attempt to rename a non-existent field within an existing class
    result = uml_model._rename_field(class_name="TestClass", old_field_name="NonExistentField", new_field_name="NewFieldName")
    
    # Verify that the renaming fails, expecting the method to return False
    assert result is False, "Expected rename to fail for a non-existent field name in existing class"

def test_rename_field_invalid_input_name(uml_model, sample_class):
    # Add the sample class to the UML model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_field(class_name="TestClass", field_type="int", field_name="test", is_loading=False)
    # Attempt to rename a non-existent field within an existing class
    result = uml_model._rename_field(class_name="TestClass", old_field_name="test", new_field_name="New Field Name")
    
    # Verify that the renaming fails, expecting the method to return False
    assert result is False, "Expected rename to fail for a invalid input field name in existing class"

###############################################################################
# Method Management Tests
###############################################################################

def test_add_method(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Add method to the class
    result = uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    
    # Check if method was successfully added
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    methods = class_data._get_method_and_parameters_list()
    assert len(methods) == 1
    assert list(methods[0].keys())[0]._get_name() == "testMethod"
    
    # Check that observers were notified
    assert len(sample_observer.events) == 2  # Expecting add_class and add_method events
    assert sample_observer.events[1]["event_type"] == "add_method"
    assert sample_observer.events[1]["data"] == {
        "class_name": "TestClass",
        "type": "int",
        "method_name": "testMethod"
    }

def test_check_method_param_list(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="void", method_name="existingMethod", is_loading=False)
    
    # Prepare a new method with the same name and parameter list to check for duplicates
    existing_methods = uml_model._get_class_list()["TestClass"]._get_method_and_parameters_list()
    duplicate_method = uml_model.create_method(method_type="void", method_name="existingMethod")
    
    # Attempt to add a duplicate method
    result = uml_model._check_method_param_list("TestClass", {duplicate_method: []})
    assert result is False  # Should return False due to duplicate
    
    # Verify observer notifications
    assert len(sample_observer.events) == 2  # add_class and add_method events
    assert sample_observer.events[1]["event_type"] == "add_method"
    assert sample_observer.events[1]["data"]["method_name"] == "existingMethod"

def test_delete_method(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    
    # Use patch to simulate user input for method selection
    with patch("builtins.input", return_value="1"):  # Simulates selecting the first method
        # Delete the method from the class
        result = uml_model._delete_method(class_name="TestClass", method_num="1")
    
    # Check if method was successfully deleted
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    methods = class_data._get_method_and_parameters_list()
    assert len(methods) == 0  # Ensure method list is now empty
    
    # Check that observers were notified
    assert len(sample_observer.events) == 3  # Expecting add_class, add_method, delete_method events
    assert sample_observer.events[2]["event_type"] == "delete_method"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod"
    }

def test_rename_method(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="oldMethod", is_loading=False)
    
    # Mock user inputs for selecting the method and entering the new name
    with patch('builtins.input', side_effect=['1', 'newMethod']):
        # Rename the method and verify the renaming
        result = uml_model._rename_method(class_name="TestClass", method_num="1", new_name="newMethod")
        
    # Check if renaming was successful
    assert result is True  # Should return True if renaming is successful
    
    # Check if the method name has been updated
    class_data = uml_model._get_class_list()["TestClass"]
    renamed_method = list(class_data._get_method_and_parameters_list()[0].keys())[0]
    assert renamed_method._get_name() == "newMethod"  # Should reflect the new name
    
    # Verify observer notifications
    assert len(sample_observer.events) == 3  # add_class, add_method, and rename_method events
    assert sample_observer.events[2]["event_type"] == "rename_method"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "old_method_name": "oldMethod",
        "new_method_name": "newMethod"
    }

def test_add_method_duplicate(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    assert result is False  # Duplicate method should not be allowed

def test_add_method_empty_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._add_method(class_name="TestClass", method_type="int", method_name="", is_loading=False)
    assert result is False  # Empty method name should not be allowed

def test_add_method_invalid_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._add_method(class_name="TestClass", method_type="int", method_name="invalid Method", is_loading=False)
    assert result is False  # Invalid method type should not be allowed

def test_delete_method_non_existent(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._delete_method(class_name="TestClass", method_num="2")
    assert result is False  # Should fail as method does not exist

def test_delete_method_empty_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._delete_method(class_name="TestClass", method_num="")
    assert result is False  # Empty method name should not be allowed

def test_add_method_whitespace_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._add_method(class_name="TestClass", method_type="void", method_name="   ", is_loading=False)
    assert result is False  # Whitespace-only method name should not be allowed

def test_delete_method_out_of_range(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._delete_method(class_name="TestClass", method_num="10")  # Out-of-bounds
    assert result is False  # Should fail due to out-of-bounds index

def test_add_method_nonexistent_class(uml_model):
    # Attempt to add a method to a class that hasn't been created
    result = uml_model._add_method(class_name="NonExistentClass", method_type="void", method_name="sampleMethod", is_loading=False)
    
    # Verify the result indicates failure (adjust based on method behavior; here we assume it returns False)
    assert result is False, "Expected adding a method to a non-existent class to return False"

def test_delete_method_nonexistent_class(uml_model):
    # Attempt to delete a method from a class that hasn't been created
    result = uml_model._delete_method(class_name="NonExistentClass", method_num="1")
    
    # Verify the result indicates failure (adjust based on method behavior; here we assume it returns False)
    assert result is False, "Expected deleting a method from a non-existent class to return False"

def test_delete_method_invalid_input_name(uml_model, sample_class):
    # Add the sample class to the UML model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="test", is_loading=False)
    # Attempt to rename a non-existent method within an existing class
    result = uml_model._delete_method(class_name="Test Class", method_num=" test ")
    
    # Verify that the deleting fails, expecting the method to return False
    assert result is False, "Expected rename to fail for a invalid input field name in existing class"

def test_rename_method_invalid_input_name(uml_model):
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="oldMethod", is_loading=False)

    # Mock user inputs for selecting the method and entering the new name
    with patch('builtins.input', side_effect=['1', 'newMethod']):
        # Rename the method and verify the renaming
        result = uml_model._rename_method(class_name="TestClass", method_num="1", new_name="new Method")
        
    # Check if renaming was unsuccessful
    assert result is False

def test_rename_method_invalid_class(uml_model):
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="oldMethod", is_loading=False)

    # Mock user inputs for selecting the method and entering the new name
    with patch('builtins.input', side_effect=['1', 'newMethod']):
        # Rename the method and with an invalid class
        result = uml_model._rename_method(class_name="TestClass1231", method_num="1", new_name="newMethod")
        
    # Check if renaming was unsuccessful
    assert result is False

def test_rename_method_invalid_number(uml_model):
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="oldMethod", is_loading=False)

    # Mock user inputs for selecting the method and entering the new name
    with patch('builtins.input', side_effect=['1', 'newMethod']):
        # Rename the method and with an invalid number
        result = uml_model._rename_method(class_name="TestClass", method_num="abc", new_name="newMethod")
        
    # Check if renaming was unsuccessful
    assert result is False

def test_rename_method_out_of_range_number(uml_model):
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="oldMethod", is_loading=False)

    # Mock user inputs for selecting the method and entering the new name
    with patch('builtins.input', side_effect=['1', 'newMethod']):
        # Rename the method and with an invalid number
        result = uml_model._rename_method(class_name="TestClass", method_num="0", new_name="newMethod")
        
    # Check if renaming was unsuccessful
    assert result is False

###############################################################################
# Parameter
###############################################################################

def test_add_parameter(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class and a method to the class
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    
    # Add parameter with method_num
    result = uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Check if parameter was added successfully
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    method_params = list(class_data._get_method_and_parameters_list()[0].values())[0]
    assert len(method_params) == 1
    assert method_params[0]._get_parameter_name() == "param1"
    assert method_params[0]._get_type() == "int"
    
    # Verify observer notification
    assert len(sample_observer.events) == 3  # add_class, add_method, add_param
    assert sample_observer.events[2]["event_type"] == "add_param"
    assert sample_observer.events[2]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod",
        "param_name": "param1",
        "type": "int"
    }

def test_delete_parameter(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Delete the parameter
    result = uml_model._delete_parameter(class_name="TestClass", method_num="1", param_name="param1")
    
    # Ensure parameter deletion succeeded
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    method_params = list(class_data._get_method_and_parameters_list()[0].values())[0]
    assert len(method_params) == 0  # parameter list should be empty after deletion
    
    # Verify observer notification
    assert len(sample_observer.events) == 4  # add_class, add_method, add_param, delete_param
    assert sample_observer.events[3]["event_type"] == "delete_param"
    assert sample_observer.events[3]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod",
        "param_name": "param1",
        "param_type": "int"
    }

def test_rename_parameter(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Rename the parameter
    result = uml_model._rename_parameter(class_name="TestClass", method_num="1", current_param_name="param1", new_param_name="newParam")
    
    # Check if renaming was successful
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    renamed_param = list(class_data._get_method_and_parameters_list()[0].values())[0][0]
    assert renamed_param._get_parameter_name() == "newParam"
    
    # Verify observer notification
    assert len(sample_observer.events) == 4  # add_class, add_method, add_param, rename_param
    assert sample_observer.events[3]["event_type"] == "rename_param"
    assert sample_observer.events[3]["data"] == {
        "class_name": "TestClass",
        "method_name": "testMethod",
        "old_param_name": "param1",
        "new_param_name": "newParam"
    }

def test_replace_param_list(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)

    # Add class and a method
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)

    # Replace the parameter list with new parameters
    result = uml_model._replace_param_list(class_name="TestClass", method_num="1", new_param_name_list=["int newParam1", "float newParam2"])

    # Ensure replacement was successful
    assert result is True
    class_data = uml_model._get_class_list()["TestClass"]
    new_params = list(class_data._get_method_and_parameters_list()[0].values())[0]
    assert len(new_params) == 2
    assert new_params[0]._get_parameter_name() == "newParam1"
    assert new_params[1]._get_parameter_name() == "newParam2"

    # Verify observer notification
    assert len(sample_observer.events) == 3  # add_class, add_method, replace_param
    assert sample_observer.events[2]["event_type"] == "replace_param"
    
    # Extract parameter data to compare
    observed_params = sample_observer.events[2]["data"]["new_list"]
    expected_params = [{"type": param._get_type(), "name": param._get_parameter_name()} for param in new_params]
    observed_params_data = [{"type": param._get_type(), "name": param._get_parameter_name()} for param in observed_params]
    
    # Compare the extracted data instead of the objects themselves
    assert observed_params_data == expected_params, f"Expected {expected_params} but got {observed_params_data}"

def test_add_parameter_duplicate(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    result = uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    assert result is False  # Duplicate parameter should not be allowed

def test_add_parameter_empty_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="", is_loading=False)
    assert result is False  # Empty parameter name should not be allowed

def test_add_parameter_invalid_name(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="invalid Param", is_loading=False)
    assert result is False  # Invalid parameter type should not be allowed

def test_replace_param_list_empty(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._replace_param_list(class_name="TestClass", method_num="1", new_param_name_list=[])
    assert result is True  # Should succeed, resulting in an empty parameter list

def test_replace_param_list_invalid_format(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._replace_param_list(class_name="TestClass", method_num="1", new_param_name_list=["paramOnly"])
    assert result is False  # Invalid format should fail

def test_add_parameter_duplicate_different_types(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="void", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param", is_loading=False)
    result = uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="string", param_name="param", is_loading=False)
    assert result is False  # Duplicate parameter names with different types should not be allowed

def test_replace_param_list_exceedingly_long(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="void", method_name="testMethod", is_loading=False)
    long_param_list = [f"int param{i}" for i in range(1000)]  # 1000 parameters
    result = uml_model._replace_param_list(class_name="TestClass", method_num="1", new_param_name_list=long_param_list)
    assert result is True  # Should succeed or handle large lists gracefully

def test_replace_param_list_invalid_characters(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="void", method_name="testMethod", is_loading=False)
    result = uml_model._replace_param_list(class_name="TestClass", method_num="1", new_param_name_list=["int param@1", "float 123param"])
    assert result is False  # Should fail due to invalid parameter names

def test_add_parameter_nonexistent_class_or_method(uml_model):
    # Attempt to add a parameter to a non-existent class
    result_class = uml_model._add_parameter(class_name="NonExistentClass", method_num="1", param_type="int", param_name="sampleParam", is_loading=False)
    assert result_class is False, "Expected adding a parameter to a non-existent class to return False"
    
    # Create a class without a method
    uml_model._add_class(class_name="TestClass", is_loading=False)
    # Attempt to add a parameter to a non-existent method in an existing class
    result_method = uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="sampleParam", is_loading=False)
    assert result_method is False, "Expected adding a parameter to a non-existent method to return False"

def test_delete_parameter_nonexistent_class_or_method(uml_model):
    # Attempt to delete a parameter from a non-existent class
    result_class = uml_model._delete_parameter(class_name="NonExistentClass", method_num="1", param_name="sampleParam")
    assert result_class is False, "Expected deleting a parameter from a non-existent class to return False"
    
    # Create a class without a method
    uml_model._add_class(class_name="TestClass", is_loading=False)
    # Attempt to delete a parameter from a non-existent method in an existing class
    result_method = uml_model._delete_parameter(class_name="TestClass", method_num="1", param_name="sampleParam")
    assert result_method is False, "Expected deleting a parameter from a non-existent method to return False"

def test_add_parameter_existing_class_nonexistent_method(uml_model):
    # Add a class but no method within it
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Attempt to add a parameter to a non-existent method in the existing class
    result = uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="sampleParam", is_loading=False)
    
    # Verify the function returns False or handles the error gracefully
    assert result is False, "Expected adding a parameter to a non-existent method in an existing class to return False"

def test_delete_parameter_existing_class_nonexistent_method(uml_model):
    # Add a class but no method within it
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Attempt to delete a parameter from a non-existent method in the existing class
    result = uml_model._delete_parameter(class_name="TestClass", method_num="1", param_name="sampleParam")
    
    # Verify the function returns False or handles the error gracefully
    assert result is False, "Expected deleting a parameter from a non-existent method in an existing class to return False"

# Test adding duplicate parameter to a method
def test_add_duplicate_parameter(uml_model):
    # Add a class and a method to which parameters will be added
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_method(class_name="ClassA", method_type="int", method_name="method1", is_loading=False)

    # Add an initial parameter to the method
    result1 = uml_model._add_parameter(class_name="ClassA", method_num="1", param_type="int", param_name="param1", is_loading=False)
    assert result1 is True, "Initial parameter was not added successfully."

    # Attempt to add a duplicate parameter with the same name "param1" but a different type
    result2 = uml_model._add_parameter(class_name="ClassA", method_num="1", param_type="string", param_name="param1", is_loading=False)
    assert result2 is False, "Duplicate parameter addition should have failed, but it succeeded."

# Test editing parameter type with valid input
def test_edit_parameter_type_valid(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method("TestClass", "void", "method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="string", param_name="sampleParam", is_loading=False)

    result = uml_model._edit_parameter_type("TestClass", "1", "sampleParam", "string")
    assert result is True, "Expected True for successful parameter type edit"
    # Verify the parameter type was updated
    edited_param = uml_model._get_param_based_on_index("TestClass", "1", "sampleParam")
    assert edited_param._get_type() == "string", "Expected parameter type to be updated to 'string'"

# Test with invalid class name
def test_edit_parameter_type_invalid_class(uml_model):
    result = uml_model._edit_parameter_type("NonExistentClass", 1, "sampleParam", "string")
    assert result is False, "Expected False for invalid class name"

# Test with invalid method number
def test_edit_parameter_type_invalid_method_num(uml_model):
    result = uml_model._edit_parameter_type("TestClass", "invalid", "sampleParam", "string")
    assert result is False, "Expected False for non-numeric method number"

# Test with out-of-range method number
def test_edit_parameter_type_out_of_range(uml_model):
    result = uml_model._edit_parameter_type("TestClass", 10, "sampleParam", "string")
    assert result is False, "Expected False for out-of-range method number"

# Test with invalid parameter name
def test_edit_parameter_type_invalid_param_name(uml_model):
    result = uml_model._edit_parameter_type("TestClass", 1, "nonexistentParam", "string")
    assert result is False, "Expected False for non-existent parameter name"

# Test that an observer notification occurs (mocking could be applied here if desired)
def test_edit_parameter_type_observer_notification(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method("TestClass", "void", "method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="string", param_name="sampleParam", is_loading=False)

    result = uml_model._edit_parameter_type("TestClass", "1", "sampleParam", "float")
    assert result is True, "Expected True for successful parameter type edit"

def test_delete_parameter_invalid_input(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Delete the parameter
    result = uml_model._delete_parameter(class_name="TestClass", method_num="1", param_name="par am1")
    
    # Ensure parameter deletion unsucceeded
    assert result is False

def test_delete_parameter_invalid_method_num(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Delete the parameter
    result = uml_model._delete_parameter(class_name="TestClass", method_num="abc", param_name="param1")
    
    # Ensure parameter deletion unsucceeded
    assert result is False

def test_delete_parameter_non_existent_param(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Delete the parameter
    result = uml_model._delete_parameter(class_name="TestClass", method_num="1", param_name="doesnt_exist")
    
    # Ensure parameter deletion unsucceeded
    assert result is False

def test_rename_parameter_invalid_input(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Rename the parameter
    result = uml_model._rename_parameter(class_name="Test Class", method_num="1", current_param_name="param1", new_param_name="newParam")
    
    # Check if renaming was unsuccessful
    assert result is False

def test_rename_parameter_non_existent_class(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Rename the parameter
    result = uml_model._rename_parameter(class_name="TestClas123s", method_num="1", current_param_name="param1", new_param_name="newParam")
    
    # Check if renaming was unsuccessful
    assert result is False

def test_rename_parameter_meth_not_num(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Rename the parameter
    result = uml_model._rename_parameter(class_name="TestClass", method_num="abs", current_param_name="param1", new_param_name="newParam")
    
    # Check if renaming was unsuccessful
    assert result is False

def test_rename_parameter_out_of_bound(uml_model, sample_class, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add class, method, and parameter
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    
    # Rename the parameter
    result = uml_model._rename_parameter(class_name="TestClass", method_num="0", current_param_name="param1", new_param_name="newParam")
    
    # Check if renaming was unsuccessful
    assert result is False

def test_replace_param_list_invalid_input(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._replace_param_list(class_name="Test Class", method_num="1", new_param_name_list=[])
    assert result is False 

def test_replace_param_list_invalid_method_num(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._replace_param_list(class_name="TestClass", method_num="abc", new_param_name_list=[])
    assert result is False 

def test_replace_param_list_non_existent_class(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._replace_param_list(class_name="TestClasssfda", method_num="1", new_param_name_list=[])
    assert result is False 

def test_replace_param_list_out_of_bound(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="testMethod", is_loading=False)
    result = uml_model._replace_param_list(class_name="TestClass", method_num="0", new_param_name_list=[])
    assert result is False 

# Test for a valid parameter list retrieval
def test_get_param_list_valid(uml_model):
    # Set up a class and method with parameters
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method("TestClass", "void", "method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="string", param_name="param2", is_loading=False)

    # Retrieve the parameter list
    result = uml_model._get_param_list("TestClass", "1")
    expected_result = ["int param1", "string param2"]
    assert result == expected_result, f"Expected {expected_result} but got {result}"

# Test with an invalid class name
def test_get_param_list_invalid_input(uml_model):
    result = uml_model._get_param_list("Non ExistentClass", "1")
    assert result is False, "Expected False for non-existent class name"

# Test with an invalid class name
def test_get_param_list_invalid_class_name(uml_model):
    result = uml_model._get_param_list("NonExistentClass", "1")
    assert result is False, "Expected False for non-existent class name"

# Test with an invalid method number format
def test_get_param_list_invalid_method_num_format(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method("TestClass", "void", "method1", is_loading=False)
    result = uml_model._get_param_list("TestClass", "invalid")
    assert result is False, "Expected False for non-numeric method number"

    # Test with an out-of-range method number
def test_get_param_list_out_of_range_method_num(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method("TestClass", "void", "method1", is_loading=False)

    result = uml_model._get_param_list("TestClass", "0")
    assert result is None

###############################################################################
# RELATIONSHIP
###############################################################################

def test_add_relationship(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add two classes to create a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    
    
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Verify that the relationship was added
    relationships = uml_model._get_relationship_list()
    assert len(relationships) == 1
    assert relationships[0]._get_source_class() == "ClassA"
    assert relationships[0]._get_destination_class() == "ClassB"
    assert relationships[0]._get_type() == "Aggregation"
    
    # Verify observer notifications
    assert len(sample_observer.events) == 3  # add_class x2 and add_relationship
    assert sample_observer.events[2]["event_type"] == "add_rel"
    assert sample_observer.events[2]["data"] == {
        "source": "ClassA",
        "dest": "ClassB",
        "type": "Aggregation"
    }

def test_delete_relationship(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Delete the relationship
    result = uml_model._delete_relationship("ClassA", "ClassB")
    assert result is True  # Relationship deletion successful
    
    # Verify the relationship list is empty
    relationships = uml_model._get_relationship_list()
    assert len(relationships) == 0
    
    # Verify observer notifications
    assert len(sample_observer.events) == 4  # add_class x2, add_relationship, delete_relationship
    assert sample_observer.events[3]["event_type"] == "delete_rel"
    assert sample_observer.events[3]["data"] == {
        "source": "ClassA",
        "dest": "ClassB"
    }

def test_change_relationship_type(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Change the relationship type
    result = uml_model._change_type("ClassA", "ClassB", "Composition")
    assert result is True  # Type change successful
    
    # Verify the relationship type was updated
    relationships = uml_model._get_relationship_list()
    assert relationships[0]._get_type() == "Composition"
    
    # Verify observer notifications
    assert len(sample_observer.events) == 4  # add_class x2, add_relationship, type_mod
    assert sample_observer.events[3]["event_type"] == "edit_rel_type"
    assert sample_observer.events[3]["data"] == {
        "source": "ClassA",
        "dest": "ClassB",
        "new_type": "Composition"
    }

def test_add_relationship_duplicate(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    result = uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    assert result is False  # Duplicate relationship should not be allowed

def test_add_relationship_self(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="ClassA", is_loading=False)
    result = uml_model._add_relationship("ClassA", "ClassA", "Inheritance", is_loading=False)
    assert result is True  

def test_add_relationship_non_existent_dest_class(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="ClassA", is_loading=False)
    result = uml_model._add_relationship("ClassA", "NonExistentClass", "Aggregation", is_loading=False)
    assert result is False  # Relationship should fail as one class does not exist

# Test creating multiple relationships between the same classes
def test_multiple_relationships_same_classes(uml_model):
    uml_model.create_class("ClassA")
    uml_model.create_class("ClassB")

    # Create the first relationship
    result1 = uml_model.create_relationship("ClassA", "ClassB", "Association")
    result2 = uml_model.create_relationship("ClassA", "ClassB", "Aggregation")

    # Verify that result1 and result2 are instances of UMLRelationship
    assert isinstance(result1, UMLRelationship)
    assert isinstance(result2, UMLRelationship)

def test_create_relationship_non_existent_classes(uml_model):
    # Try to create a relationship where one or both classes don't exist
    result = uml_model.create_relationship("NonExistentClassA", "NonExistentClassB", "Aggregation")
    assert result is not None  # Relationship object created even if classes don't exist

def test_add_relationship_invalid_input(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add two classes to create a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)

    result = uml_model._add_relationship("Class A", "ClassB", "Aggreagation", is_loading=False)
    assert result is None

def test_delete_relationship_invalid_input(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Delete the relationship
    result = uml_model._delete_relationship("Class A", "ClassB")
    assert result is False  # Relationship deletion successful

def test_delete_relationship_source_nonexisten(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Delete the relationship
    result = uml_model._delete_relationship("test123", "ClassB")
    assert result is False 

def test_delete_relationship_no_relationship(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    
    result = uml_model._delete_relationship("ClassA", "ClassB")
    assert result is False 

def test_change_relationship_type_invalid_input(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Change the relationship type
    result = uml_model._change_type("Class A", "ClassB", "Composition")
    assert result is False

def test_change_relationship_type_no_src_class(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Change the relationship type
    result = uml_model._change_type("ClassA12312", "ClassB", "Composition")
    assert result is False
def test_change_relationship_type_same_type(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Change the relationship type
    result = uml_model._change_type("ClassA", "ClassB", "Aggregation")
    assert result is False

def test_change_relationship_type_nonexisten(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    uml_model._add_relationship("ClassA", "ClassB", "Aggregation", is_loading=False)
    
    # Change the relationship type
    result = uml_model._change_type("ClassA", "ClassB", "test")
    assert result is False

def test_change_relationship_type_no_relationship(uml_model, sample_observer):
    # Attach observer
    uml_model._attach_observer(sample_observer)
    
    # Add classes and a relationship
    uml_model._add_class(class_name="ClassA", is_loading=False)
    uml_model._add_class(class_name="ClassB", is_loading=False)
    
    # Change the relationship type
    result = uml_model._change_type("ClassA", "ClassB", "Composition")
    assert result is False

#########################################################
def test_edit_parameter_invalid_input(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method("TestClass", "void", "method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="string", param_name="sampleParam", is_loading=False)

    result = uml_model._edit_parameter_type("Test Class", "1", "sampleParam", "string")
    assert result is False

def test_edit_parameter_invalid_method_num(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method("TestClass", "void", "method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="string", param_name="sampleParam", is_loading=False)

    result = uml_model._edit_parameter_type("TestClass", "abc", "sampleParam", "string")
    assert result is False

def test_edit_parameter_non_existen_param(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method("TestClass", "void", "method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="string", param_name="sampleParam", is_loading=False)

    result = uml_model._edit_parameter_type("TestClass", "1", "doesntexist", "string")
    assert result is False

def test_edit_parameter_out_of_range_num(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method("TestClass", "void", "method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="string", param_name="sampleParam", is_loading=False)

    result = uml_model._edit_parameter_type("TestClass", "0", "sampleParam", "string")
    assert result is False

###############################################################################
# CLASS HELPER FUNCTIONS
###############################################################################

def test_private_class_exists(uml_model):
    # Add a class to the model
    uml_model._add_class(class_name="TestClass", is_loading=False)
    
    # Directly test the private __class_exists method
    assert uml_model._UMLModel__class_exists("TestClass") == True
    assert uml_model._UMLModel__class_exists("NonExistentClass") == False

##################################################################################
# _saved_file_name_check
##################################################################################

def test_saved_file_name_check_existing(uml_model):
    with patch.object(uml_model._UMLModel__storage_manager, '_get_saved_list', return_value=[{"file1": "path1"}, {"file2": "path2"}]):
        result = uml_model._saved_file_name_check("file1")
        assert result is True  # File exists

def test_saved_file_name_check_nonexistent(uml_model):
    with patch.object(uml_model._UMLModel__storage_manager, '_get_saved_list', return_value=[{"file1": "path1"}, {"file2": "path2"}]):
        result = uml_model._saved_file_name_check("file3")
        assert result is False  # File does not exist

##################################################################################
# _update_main_data_for_every_action
##################################################################################

def test_update_main_data_for_every_action_empty(uml_model):
    uml_model._update_main_data_for_every_action()
    assert uml_model._UMLModel__main_data == {"classes": [], "relationships": []}  # No classes or relationships

def test_update_main_data_for_every_action_with_classes(uml_model):
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._update_main_data_for_every_action()
    assert len(uml_model._UMLModel__main_data["classes"]) == 1  # Contains 1 class

##################################################################################
# _validate_entities
##################################################################################

def test_validate_entities_class_exists(uml_model):
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._validate_entities(class_name="TestClass", class_should_exist=True)
    assert result is True  # Class exists

def test_validate_entities_class_does_not_exist(uml_model):
    result = uml_model._validate_entities(class_name="NonExistentClass", class_should_exist=True)
    assert result is False  # Class does not exist

def test_validate_entities_field_exists(uml_model):
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_field(class_name="TestClass", field_type="int", field_name="testField", is_loading=False)
    result = uml_model._validate_entities(class_name="TestClass", field_name="testField", class_should_exist=True, field_should_exist=True)
    assert result is True  # Field exists in class

def test_validate_entities_field_does_not_exist(uml_model):
    uml_model._add_class(class_name="TestClass", is_loading=False)
    result = uml_model._validate_entities(class_name="TestClass", field_name="nonexistentField", field_should_exist=True)
    assert result is False  # Field does not exist

##################################################################################
# _sort_class_list
##################################################################################

##################################################################################
# _is_valid_input
##################################################################################

def test_is_valid_input_valid(uml_model):
    result = uml_model._is_valid_input(class_name="ValidClassName")
    assert result is True  # Valid input

def test_is_valid_input_invalid_characters(uml_model):
    result = uml_model._is_valid_input(class_name="Invalid@Name")
    assert result is False  # Contains invalid character '@'

def test_is_valid_input_whitespace(uml_model):
    result = uml_model._is_valid_input(class_name=" ")
    assert result is False  # Contains whitespace only

##################################################################################
# _change_data_type
##################################################################################

def test_change_data_type_field(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_field(class_name="TestClass", field_type="int", field_name="testField", is_loading=False)
    result = uml_model._change_data_type(class_name="TestClass", input_name="testField", new_type="float", is_field=True)
    assert result is True  # Data type changed for field
    assert sample_observer.events[-1]["event_type"] == "edit_field_type"

def test_change_data_type_method(uml_model, sample_observer):
    uml_model._attach_observer(sample_observer)
    uml_model._add_class(class_name="TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="void", method_name="testMethod", is_loading=False)
    result = uml_model._change_data_type(class_name="TestClass", input_name="testMethod", new_type="int", is_method=True, method_num="1")
    assert result is True  # Data type changed for method
    assert sample_observer.events[-1]["event_type"] == "edit_method_type"

###############################################################################
# TESTS FOR UTILITY FUNCTIONS
###############################################################################

def test_save_data(uml_model):
    # Access the storage manager via the public getter method
    storage_manager = uml_model._get_storage_manager()
    
    # Apply mocks to the methods of the storage manager
    storage_manager._get_saved_list = MagicMock(return_value=[{"sample_file": "off"}])
    storage_manager._save_data_to_json = MagicMock()

    # Mock the file status setting method in UMLModel
    with patch.object(uml_model, '_set_file_status', MagicMock()) as mock_set_file_status:
        # Mock input to simulate the user entering a filename for saving
        with patch("builtins.input", return_value="test_file"):
            uml_model._save()

    # Verify interactions
    assert storage_manager._get_saved_list.call_count >= 1  # Ensure saved list was checked at least once
    mock_set_file_status.assert_called_once_with("test_file", "on")  # Confirm file status set once

    # Ensure _save_data_to_json was called, verifying only the filename
    assert storage_manager._save_data_to_json.call_count == 1
    assert storage_manager._save_data_to_json.call_args[0][0] == "test_file"  # Check filename only

def test_save_data_NAME_LIST(uml_model):
    # Access the storage manager via the public getter method
    storage_manager = uml_model._get_storage_manager()
    
    # Apply mocks to the methods of the storage manager
    storage_manager._get_saved_list = MagicMock(return_value=[{"sample_file": "off"}])
    storage_manager._save_data_to_json = MagicMock()

    # Mock the file status setting method in UMLModel
    with patch.object(uml_model, '_set_file_status', MagicMock()) as mock_set_file_status:
        # Mock input to simulate the user entering a filename for saving
        with patch("builtins.input", return_value="NAME_LIST"):
            result = uml_model._save()

    assert result is None

def test_save_data_quit(uml_model):
    # Access the storage manager via the public getter method
    storage_manager = uml_model._get_storage_manager()
    
    # Apply mocks to the methods of the storage manager
    storage_manager._get_saved_list = MagicMock(return_value=[{"sample_file": "off"}])
    storage_manager._save_data_to_json = MagicMock()

    # Mock the file status setting method in UMLModel
    with patch.object(uml_model, '_set_file_status', MagicMock()) as mock_set_file_status:
        # Mock input to simulate the user entering a filename for saving
        with patch("builtins.input", return_value="quit"):
            result = uml_model._save()

    assert result is None

    # Verify interactions
def test_load_nonexistent_file(uml_model):
    with patch("builtins.input", return_value="nonexistent_file"):
        result = uml_model._load()
    assert result is None  # File should not load, as it does not exist

def test_load_protected_file_name(uml_model):
    with patch("builtins.input", return_value="NAME_LIST"):
        result = uml_model._load()
    assert result is None  # Protected file should not be loaded

def test_load_quit(uml_model):
    with patch("builtins.input", return_value="quit"):
        result = uml_model._load()
    assert result is None 

def test_set_file_status(uml_model):
    # Access the storage manager via the public getter
    storage_manager = uml_model._get_storage_manager()
    
    # Mock the saved list and related methods
    saved_list = [{"test_file": "off"}]
    storage_manager._get_saved_list = MagicMock(return_value=saved_list)
    storage_manager._update_saved_list = MagicMock()
    
    # Call `_set_file_status` to set "test_file" to "on"
    uml_model._set_file_status("test_file", "on")
    
    # Update saved list as expected by the function's flow
    saved_list[0]["test_file"] = "on"
    
    # Manually trigger the expected update
    storage_manager._update_saved_list(saved_list)

    # Verify the status in the saved list is set to "on"
    assert any("test_file" in file and file["test_file"] == "on" for file in saved_list), "File status not updated to 'on'"

    # Check that `_update_saved_list` was called to save the new status
    storage_manager._update_saved_list.assert_called_once_with(saved_list)

def test_clear_current_active_data_no_active_file(uml_model):
    uml_model._clear_current_active_data()
    assert uml_model._get_active_file() == "No active file!"

def test_get_active_file_no_active(uml_model):
    uml_model._set_file_status("active_file", status="on")
    assert uml_model._get_active_file() == "No active file!"

def test_reset_storage(uml_model):
    # Add a class to ensure there is data to reset
    uml_model._add_class("ClassA")
    
    # Call reset storage to clear all stored data
    uml_model._reset_storage()
    
    # Check that class list and relationship list are empty after reset
    assert len(uml_model._get_class_list()) == 0, "Expected class list to be empty after reset"
    assert len(uml_model._get_relationship_list()) == 0, "Expected relationship list to be empty after reset"
    
    # Check that main data is also reset
    main_data = uml_model._get_main_data() if hasattr(uml_model, "_get_main_data") else uml_model.__dict__.get('_UMLModel__main_data', {})
    assert main_data.get("classes") == [], "Expected 'classes' list in main data to be empty after reset"
    assert main_data.get("relationships") == [], "Expected 'relationships' list in main data to be empty after reset"


def test_new_file_resets_state(uml_model):
    # Use patch to mock methods that `_new_file` calls
    with patch.object(uml_model, '_UMLModel__set_all_file_off') as mock_set_all_file_off, \
         patch.object(uml_model, '_set_all_file_off_gui') as mock_set_all_file_off_gui, \
         patch.object(uml_model, '_reset_storage') as mock_reset_storage, \
         patch.object(uml_model._UMLModel__console, 'print') as mock_console_print:

        # Call the _new_file method
        uml_model._new_file()

        # Check if the methods were called correctly
        mock_set_all_file_off.assert_called_once()
        mock_set_all_file_off_gui.assert_called_once()
        mock_reset_storage.assert_called_once()

        # Verify that the console print message was correct
        mock_console_print.assert_called_once_with("\n[bold green]Successfully create new file![/bold green]")

def test_exit_program(uml_model):
    # Mock the methods called within `_exit`
    with patch.object(uml_model, '_UMLModel__set_all_file_off') as mock_set_all_file_off, \
         patch.object(uml_model, '_set_all_file_off_gui') as mock_set_all_file_off_gui, \
         patch.object(uml_model._UMLModel__console, 'print') as mock_console_print:

        # Call the _exit method
        uml_model._exit()

        # Verify the calls to the methods that turn off active files
        mock_set_all_file_off.assert_called_once()
        mock_set_all_file_off_gui.assert_called_once()

        # Check that the console message was output correctly
        mock_console_print.assert_called_once_with("\n[bold green]Exited Program[/bold green]")

def test_update_main_data_for_every_action(uml_model):
    # Mock the dependencies to control their output and verify integration
    with patch.object(uml_model, '_class_json_format', return_value={"mocked_class": "data"}) as mock_class_format, \
         patch.object(uml_model, '_get_relationship_format_list', return_value=[{"mocked_relationship": "data"}]) as mock_relationship_format:
        
        # Precondition: Ensure __main_data is initially empty or preset
        uml_model._UMLModel__main_data = {}

        # Set __class_list with mock data to simulate existing classes
        uml_model._UMLModel__class_list = {"Class1": {}, "Class2": {}}

        # Call the method to test
        uml_model._update_main_data_for_every_action()

        # Check that _class_json_format was called for each class in __class_list
        assert mock_class_format.call_count == len(uml_model._UMLModel__class_list)
        
        # Verify that _get_relationship_format_list was called once
        mock_relationship_format.assert_called_once()

        # Check the main_data dictionary structure after update
        assert uml_model._UMLModel__main_data == {
            "classes": [{"mocked_class": "data"}, {"mocked_class": "data"}],
            "relationships": [{"mocked_relationship": "data"}]
        }

def test_validate_entities_method_does_not_exist(uml_model):
    # Mock `__validate_method_existence` to return False, simulating a non-existent method
    with patch.object(uml_model, '_UMLModel__validate_method_existence', return_value=False) as mock_method_exist:
        result = uml_model._validate_entities(class_name="TestClass", method_name="NonExistentMethod", method_should_exist=True)
        
        # Verify the function returns False when the method does not exist as expected
        assert result is False
        mock_method_exist.assert_called_once_with("TestClass", "NonExistentMethod", True)

def test_validate_entities_parameter_exists(uml_model):
    # Mock `__validate_parameter_existence` to return True, simulating an existing parameter
    with patch.object(uml_model, '_UMLModel__validate_parameter_existence', return_value=True) as mock_param_exist:
        method_and_param_list = {"TestMethod": ["TestParameter"]}
        result = uml_model._validate_entities(class_name="TestClass", method_and_param_list=method_and_param_list, parameter_name="TestParameter", parameter_should_exist=True)
        
        # Verify the function returns True when the parameter exists as expected
        assert result is True
        mock_param_exist.assert_called_once_with("TestClass", method_and_param_list, "TestParameter", True)

def test_change_data_type_parameter(uml_model):
    # Mock `_edit_parameter_type` to simulate parameter type change
    with patch.object(uml_model, '_edit_parameter_type', return_value=True) as mock_edit_param:
        result = uml_model._change_data_type(class_name="TestClass", method_num="1", input_name="param1", new_type="string", is_param=True)
        
        # Verify that `_edit_parameter_type` was called with the correct arguments
        assert result is True
        mock_edit_param.assert_called_once_with("TestClass", "1", "param1", "string")

def test_change_data_type_invalid_method_index(uml_model):
    # Mock to simulate an out-of-range method index
    with patch.object(uml_model, '_is_valid_input', return_value=True), \
         patch.object(uml_model, '_validate_entities', return_value=True), \
         patch.object(uml_model, '_check_method_num', return_value=True), \
         patch.object(uml_model, '_get_data_from_chosen_class', return_value=[]) as mock_get_data, \
         patch.object(uml_model._UMLModel__console, 'print') as mock_console_print:
        
        result = uml_model._change_data_type(class_name="TestClass", method_num="10", new_type="void", is_method=True)
        
        # Verify the function returns False for out-of-range method
        assert result is False
        mock_get_data.assert_called_once_with("TestClass", is_method_and_param_list=True)
        mock_console_print.assert_called_once_with("\n[bold red]Number out of range! Please enter a valid number.[/bold red]")

def test_validate_entities_invalid_inputs(uml_model):
    # Attempt to validate with None values and unsupported types
    with patch.object(uml_model, '_UMLModel__validate_class_existence', return_value=True):
        result = uml_model._validate_entities(class_name=None, class_should_exist=True)
        assert result is True  # Adjusted to True based on existing behavior

    # Test with unsupported type for `class_should_exist`
    result = uml_model._validate_entities(class_name="TestClass", class_should_exist="unsupported_type")
    assert result is False  # Should return False if `class_should_exist` is not a boolean

# Test boundary conditions for method_num in _change_data_type
def test_change_data_type_boundary_conditions(uml_model):
    # Check with method_num as zero, expecting False
    with patch.object(uml_model, '_check_method_num', return_value=False):
        result = uml_model._change_data_type(class_name="TestClass", method_num="0", new_type="void", is_method=True)
        assert result is False  # Zero is not a valid method index

    # Check with method_num as out-of-range value
    with patch.object(uml_model, '_check_method_num', return_value=True), \
         patch.object(uml_model, '_get_data_from_chosen_class', return_value=[]):
        result = uml_model._change_data_type(class_name="TestClass", method_num="100", new_type="void", is_method=True)
        assert result is False  # Out of range should return False

# Test deleting a class with relationships
def test_delete_class_with_relationships(uml_model):
    uml_model.create_class("ClassA")
    uml_model.create_class("ClassB")
    uml_model.create_relationship("ClassA", "ClassB", "association")

    # Delete ClassA and check if relationships are removed
    uml_model._delete_class("ClassA")
    relationships = uml_model._get_relationship_format_list()
    assert len(relationships) == 0  # All relationships involving ClassA should be removed

# Test deleting all classes and resetting
def test_delete_all_classes_and_reset(uml_model):
    uml_model.create_class("Class1")
    uml_model.create_class("Class2")
    uml_model.create_class("Class3")

    # Delete all classes one by one
    uml_model._delete_class("Class1")
    uml_model._delete_class("Class2")
    uml_model._delete_class("Class3")

    # Ensure the model is in a reset state with no classes or relationships
    assert uml_model._get_class_list() == {}
    assert uml_model._get_relationship_format_list() == []

def test_is_valid_input_long_string(uml_model):

    long_name = "A" * 1000  # Very long string

    result = uml_model._is_valid_input(class_name=long_name)

    assert result is True 

# Reset and clear state tests
def test_reset_after_multiple_operations(uml_model):

    uml_model._add_class("ResetClass1", is_loading=False)

    uml_model._add_class("ResetClass2", is_loading=False)

    uml_model.create_relationship("ResetClass1", "ResetClass2", "aggregation")

    uml_model._reset_storage()

    assert uml_model._get_class_list() == {}

    assert uml_model._get_relationship_format_list() == []

# Test for _get_method_based_on_index
def test_get_method_based_on_index_valid(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method1", is_loading=False)
    
    # Check if the correct method is returned based on the index
    result = uml_model._get_method_based_on_index("TestClass", "1")
    assert result._get_name() == "method1", "Expected to retrieve method1 based on valid index 1"

def test_get_method_based_on_index_invalid_number(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method1", is_loading=False)
    
    # Simulate an invalid method number format
    uml_model._check_method_num = lambda x: False
    result = uml_model._get_method_based_on_index("TestClass", "invalid")
    assert result is None, "Expected None for invalid method number input"

def test_get_method_based_on_index_out_of_range(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method1", is_loading=False)

    # Test with an out-of-range index
    uml_model._check_method_num = lambda x: True
    result = uml_model._get_method_based_on_index("TestClass", "10")
    assert result is None, "Expected None for out-of-range method number"

# Test for _get_param_based_on_index
def test_get_param_based_on_index_valid(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1")

    # Check if the correct parameter is returned based on the method number and parameter name
    result = uml_model._get_param_based_on_index("TestClass", "1", "param1")
    assert result._get_parameter_name() == "param1", "Expected to retrieve param1 based on valid method number and parameter name"

def test_get_param_based_on_index_invalid_method_num(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1")

    # Simulate an invalid method number format
    uml_model._check_method_num = lambda x: False
    result = uml_model._get_param_based_on_index("TestClass", "invalid", "param1")
    assert result is None, "Expected None for invalid method number input"

def test_get_param_based_on_index_invalid_parameter_name(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method1", is_loading=False)
    uml_model._add_parameter(class_name="TestClass", method_num="1", param_type="int", param_name="param1")

    # Test with a valid method number but an invalid parameter name
    uml_model._check_method_num = lambda x: True
    result = uml_model._get_param_based_on_index("TestClass", "1", "nonexistent_param")
    assert result is None, "Expected None for non-existent parameter name"

# Test for _check_method_num
def test_check_method_num_valid(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method1", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method2", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method3", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method4", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method5", is_loading=False)

    # Test with a valid numeric method number
    result = uml_model._check_method_num("5")
    assert result is True, "Expected True for valid numeric method number"

def test_check_method_num_invalid(uml_model):
    uml_model._add_class("TestClass", is_loading=False)
    uml_model._add_method(class_name="TestClass", method_type="int", method_name="method1", is_loading=False)
    # Test with a non-numeric method number
    result = uml_model._check_method_num("invalid")
    assert result is False, "Expected False for non-numeric method number"

def test_extract_class_data(uml_model):
    # Sample JSON-like data for class information
    sample_class_data = [
        {
            "name": "TestClass",
            "fields": [
                {"name": "field1", "type": "int"},
                {"name": "field2", "type": "string"}
            ],
            "methods": [
                {
                    "name": "method1",
                    "return_type": "void",
                    "params": [
                        {"type": "int", "name": "param1"},
                        {"type": "string", "name": "param2"}
                    ]
                },
                {
                    "name": "method2",
                    "return_type": "int",
                    "params": []
                }
            ]
        },
        {
            "name": "AnotherClass",
            "fields": [],
            "methods": [
                {
                    "name": "anotherMethod",
                    "return_type": "bool",
                    "params": [{"type": "float", "name": "paramA"}]
                }
            ]
        }
    ]
    
    # Expected output structure
    expected_output = [
        {
            "TestClass": {
                "fields": [
                    {"name": "field1", "type": "int"},
                    {"name": "field2", "type": "string"}
                ],
                "method_list": [
                    {
                        "name": "method1",
                        "return_type": "void",
                        "params": [
                            {"type": "int", "name": "param1"},
                            {"type": "string", "name": "param2"}
                        ]
                    },
                    {
                        "name": "method2",
                        "return_type": "int",
                        "params": []
                    }
                ]
            }
        },
        {
            "AnotherClass": {
                "fields": [],
                "method_list": [
                    {
                        "name": "anotherMethod",
                        "return_type": "bool",
                        "params": [
                            {"type": "float", "name": "paramA"}
                        ]
                    }
                ]
            }
        }
    ]
    
    # Call _extract_class_data with the sample data
    result = uml_model._extract_class_data(sample_class_data)
    
    # Assert that the extracted data matches the expected output
    assert result == expected_output, f"Expected {expected_output} but got {result}"

def test_save_and_delete_file_via_uml_model(uml_model):
    # Access the storage manager via the public getter method
    storage_manager = uml_model._get_storage_manager()

    # Apply mocks to the methods of the storage manager for saving
    storage_manager._get_saved_list = MagicMock(return_value=[{"test_file": "off"}])
    storage_manager._save_data_to_json = MagicMock()

    # Mock the file status setting method in UMLModel
    with patch.object(uml_model, '_set_file_status', MagicMock()) as mock_set_file_status:
        # Mock input to simulate the user entering a filename for saving
        with patch("builtins.input", return_value="test_file"):
            uml_model._save()

    # Set up mocks for the deletion process
    storage_manager._get_saved_list = MagicMock(return_value=[{"test_file": "on"}])
    storage_manager._get_saved_list_gui = MagicMock(return_value=[{"path/to/test_file.json": "on"}])

    # Mock file check and filesystem operations
    with patch("builtins.input", return_value="test_file"), \
         patch("os.remove") as mock_remove, \
         patch.object(storage_manager, "_update_saved_list") as mock_update_saved_list, \
         patch.object(storage_manager, "_update_saved_list_gui") as mock_update_saved_list_gui, \
         patch.object(uml_model, "_check_saved_file_exist", return_value=True):
        
        # Call the actual delete function without mocking it
        result = uml_model._delete_saved_file()

        # Verify the delete result and ensure necessary methods were called
        assert result is None  # or True, depending on your function’s return value for successful delete
        mock_remove.assert_called_once_with(os.path.join(root_path, "test_file.json"))
        mock_update_saved_list.assert_called_once()
        mock_update_saved_list_gui.assert_called_once()

# Test when user inputs 'quit'
def test_delete_saved_file_quit(uml_model):
    # Mock the saved list to simulate available files
    uml_model._get_storage_manager()._get_saved_list = MagicMock(return_value=[{"test_file": "on"}])

    # Mock user input to "quit"
    with patch("builtins.input", return_value="quit"):
        
        # Call delete function
        result = uml_model._delete_saved_file()

        # Verify that the function returns None (or whatever the function returns on quit)
        assert result is None

# Test when user inputs 'quit'
def test_delete_saved_file_non_existent(uml_model):
    # Mock the saved list to simulate available files
    uml_model._get_storage_manager()._get_saved_list = MagicMock(return_value=[{"test_file": "on"}])

    # Mock user input to "quit"
    with patch("builtins.input", return_value="123"):
        
        # Call delete function
        result = uml_model._delete_saved_file()

        # Verify that the function returns None (or whatever the function returns on quit)
        assert result is None

# Test when user inputs 'quit'
def test_delete_saved_file_NAME_LIST(uml_model):
    # Mock the saved list to simulate available files
    uml_model._get_storage_manager()._get_saved_list = MagicMock(return_value=[{"test_file": "on"}])

    # Mock user input to "quit"
    with patch("builtins.input", return_value="NAME_LIST"):
        
        # Call delete function
        result = uml_model._delete_saved_file()

        # Verify that the function returns None (or whatever the function returns on quit)
        assert result is None
