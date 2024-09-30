###################################################################################################

import os
from enum import Enum
from typing import Dict, List
from UML_CORE.UML_CLASS.uml_class import UMLClass as Class
from UML_CORE.UML_FIELD.uml_field import UMLField as Field
from UML_CORE.UML_METHOD.uml_method import UMLMethod as Method
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship as Relationship
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter as Parameter
from UML_MANAGER.uml_storage_manager import UMLStorageManager as Storage
from UML_MANAGER.uml_cli_view import UMLView as View

###################################################################################################
### ENUM VALUES FOR THE INTERFACE ###

class InterfaceOptions(Enum):
    ADD_CLASS = "add_class"
    DELETE_CLASS = "delete_class"
    RENAME_CLASS = "rename_class"
    ADD_FIELD = "add_field"
    DELETE_FIELD = "delete_field"
    RENAME_FIELD = "rename_field"
    ADD_METHOD = "add_method"
    DELETE_METHOD = "delete_method"
    RENAME_METHOD = "rename_method"
    ADD_PARAM = "add_param"
    DELETE_PARAM = "delete_param"
    RENAME_PARAM = "rename_param"
    REPLACE_PARAM = "replace_param"
    ADD_REL = "add_rel"
    DELETE_REL = "delete_rel"
    TYPE_MOD = "type_mod"
    LIST_CLASS = "list_class"
    CLASS_DETAIL = "class_detail"
    CLASS_REL = "class_rel"
    SAVED_LIST = "saved_list"
    SAVE = "save"
    LOAD = "load"
    DELETE_SAVED = "delete_saved"
    CLEAR_DATA = "clear_data"
    DEFAULT = "default"
    SORT = "sort"
    HELP = "help"
    EXIT = "exit"    
    
###################################################################################################

class UMLCoreManager:
    
    #################################################################
    
    # UML Class Manager Constructor #
    
    def __init__(self):        
        self.__class_list: Dict[str, Class] = {}
        self.__storage_manager: Storage = Storage()
        self.__relationship_list: List[Relationship] = []
        self.__main_data: Dict = {"classes":[], "relationship":[]}
        self.__user_view: View = View()
        
    # Getters #
        
    def _get_class_list(self) -> Dict[str, Class]:
        return self.__class_list
    
    def _get_main_data(self) -> Dict:
        return self.__main_data
    
    def _get_relationship_list(self) -> List[Relationship]:
        return self.__relationship_list
    
    def _get_storage_manager(self) -> Storage:
        return self.__storage_manager
        
    #################################################################
    ### STATIC FUNCTIONS ###

    # Class creation method #
    @staticmethod
    def create_class(class_name: str) -> Class:
        return Class(class_name)
    
    # Field creation method #
    @staticmethod
    def create_field(field_name: str) -> Field:
        return Field(field_name)
    
    # Method creation method #
    @staticmethod
    def create_method(method_name: str) -> Method:
        return Method(method_name)
    
    # Parameter creation method #
    @staticmethod
    def create_parameter(parameter_name: str) -> Parameter:
        return Parameter(parameter_name)
    
    # Relationship creation method #
    @staticmethod
    def create_relationship(source_class: str, destination_class: str, rel_type: str) -> Relationship:
        return Relationship(source_class, destination_class, rel_type)
    
    #################################################################
    ### MEMBER FUNCTIONS ###
    
    ## CLASS RELATED ##
    
    # Add class #
    def _add_class(self, class_name: str, is_loading: bool):
        # Check if class exists or not
        is_class_exist = self._validate_entities(class_name=class_name, class_should_exist=False)
        # If the class has already existed, stop
        if not is_class_exist:
            return
        # Else, add the class
        new_class = self.create_class(class_name)
        self.__class_list[class_name] = new_class
        if not is_loading:
            print(f"\nSuccessfully added class '{class_name}'!")
        
    # Delete class #
    def _delete_class(self, class_name: str):
        # Check if class exists or not
        is_class_exist = self._validate_entities(class_name=class_name, class_should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Else, delete class
        self.__class_list.pop(class_name)
        # Clean up connected relationship
        self.__clean_up_relationship(class_name)
        print(f"\nSuccessfully removed class '{class_name}'!")
        
    # Rename class #
    def _rename_class(self, current_name: str, new_name: str):
        # Check if we are able to rename
        is_able_to_rename = self.__check_class_rename(current_name, new_name)
        # If not, stop
        if not is_able_to_rename:
            return
        # Update the real class
        class_object = self.__class_list[current_name]
        class_object._set_class_name(new_name) 
        # Update the key
        self.__class_list[new_name] = self.__class_list.pop(current_name)
        # Update name in relationship list
        self.__update_name_in_relationship(current_name, new_name)
        print(f"\nSuccessfully renamed from class '{current_name}' to class '{new_name}'!")
        
    ## FIELD RELATED ##
    
    # Add field #
    def _add_field(self, class_name: str, field_name: str, is_loading: bool):        
        # Check if class and field exist
        is_class_and_field_exist = self._validate_entities(class_name=class_name, field_name=field_name, class_should_exist=True, field_should_exist=False)
        if not is_class_and_field_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get field list
        field_list = class_object._get_class_field_list()
        # Create new field
        new_field = self.create_field(field_name)
        # Add field
        field_list.append(new_field)
        if not is_loading:
            print(f"\nSuccessfully added field '{field_name}'!")
        
    # Delete field #
    def _delete_field(self, class_name: str, field_name: str):
        # Check if class and field exist
        is_class_and_field_exist = self._validate_entities(class_name=class_name, field_name=field_name, class_should_exist=True, field_should_exist=True)
        if not is_class_and_field_exist:
            return
         # Get class object
        class_object = self.__class_list[class_name]
        # Get field list
        field_list = class_object._get_class_field_list()
        # Get the field
        chosen_field = self.__get_chosen_field_or_method(class_name, field_name, is_field=True)
        # Remove the chosen field 
        field_list.remove(chosen_field)
        print(f"\nSuccessfully removed field '{field_name}'!")
        
    # Rename field #
    def _rename_field(self, class_name: str, current_field_name: str, new_field_name: str):
        is_able_to_rename = self.__check_field_or_method_rename(class_name, current_field_name, new_field_name, is_field=True)
        if not is_able_to_rename:
            return
        # Get the field
        chosen_field = self.__get_chosen_field_or_method(class_name, current_field_name, is_field=True)
        chosen_field._set_name(new_field_name)
        print(f"\nSuccessfully renamed from field '{current_field_name}' to field '{new_field_name}'!")
        
    ## METHOD RELATED ##
    
    # Add method #
    def _add_method(self, class_name: str, method_name: str, is_loading: bool):
        # Check if class and method exist or not
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=False)
        if not is_class_and_method_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get field list
        method_list = class_object._get_class_method_list()
        # Create new method
        new_method = self.create_method(method_name)
        # Add method
        method_list.append(new_method)
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        # Add method with empty list of parameter
        method_and_parameter_list[method_name] = []
        if not is_loading:
            print(f"\nSuccessfully added method '{method_name}'!")
        
    # Delete method #
    def _delete_method(self, class_name: str, method_name: str):
        # Check if class and method exist or not
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=True)
        if not is_class_and_method_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get method list
        method_list = class_object._get_class_method_list()
        # Get method and parameter list and delete the method from it
        method_and_parameter_list = class_object._get_method_and_parameters_list()
        method_and_parameter_list.pop(method_name)
        # Get the method
        chosen_method = self.__get_chosen_field_or_method(class_name, method_name, is_field=False)
        # Remove the chosen method 
        method_list.remove(chosen_method)
        print(f"\nSuccessfully removed method '{method_name}'!")
        
    # Rename method #
    def _rename_method(self, class_name: str, current_method_name: str, new_method_name: str):
        is_able_to_rename = self.__check_field_or_method_rename(class_name, current_method_name, new_method_name, is_field=False)
        if not is_able_to_rename:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get method and parameter list and update the key (method name)
        method_and_parameter_list = class_object._get_method_and_parameters_list()
        method_and_parameter_list[new_method_name] = method_and_parameter_list.pop(current_method_name)
        # Get the method
        chosen_method = self.__get_chosen_field_or_method(class_name, current_method_name, is_field=False)
        chosen_method._set_name(new_method_name)
        print(f"\nSuccessfully renamed from method '{current_method_name}' to method '{new_method_name}'!")
    
    ## PARAMETER RELATED ##
    
    # Add parameter #
    def _add_parameter(self, class_name: str, method_name: str, parameter_name: str, is_loading: bool):
        # Check if class, method and its parameter exist or not
        is_class_and_method_and_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name,parameter_name=parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=False )
        if not is_class_and_method_and_parameter_exist:
            return
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        # Create parameter
        new_parameter = self.create_parameter(parameter_name)
        # Add new parameter
        method_and_parameter_list[method_name].append(new_parameter)
        if not is_loading:
            print(f"\nSuccessfully added parameter '{parameter_name}' to method '{method_name}'!")
            
    # Delete parameter #
    def _delete_parameter(self, class_name: str, method_name: str, parameter_name: str):
        # Check if class, method and its parameter exist or not
        is_class_and_method_and_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name,parameter_name=parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=True )
        if not is_class_and_method_and_parameter_exist:
            return
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        # Get chosen parameter
        chosen_parameter = self.__get_chosen_parameter(class_name, method_name, parameter_name)
        # Remove the chosen parameter
        method_and_parameter_list[method_name].remove(chosen_parameter)
        print(f"\nSuccessfully removed parameter '{parameter_name}' from method '{method_name}'!")
        
    # Rename parameter #
    def _rename_parameter(self, class_name: str, method_name: str, current_parameter_name: str, new_parameter_name: str):
        # Check if class, method and its parameter exist or not
        is_class_and_method_and_current_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name,parameter_name=current_parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=True )
        if not is_class_and_method_and_current_parameter_exist:
            return
        # Check if new parameter exists or not
        is_new_parameter_exist = self._validate_entities(class_name=class_name, method_name=method_name,parameter_name=new_parameter_name, class_should_exist=True, method_should_exist=True, parameter_should_exist=False )
        # If new parameter exist, stop
        if not is_new_parameter_exist:
            return
        # Get chosen parameter
        chosen_parameter = self.__get_chosen_parameter(class_name, method_name, current_parameter_name)
        chosen_parameter._set_parameter_name(new_parameter_name)
        print(f"\nSuccessfully renamed from parameter '{current_parameter_name}' to parameter '{new_parameter_name}'!")
        
    # Replace parameter list, fail if class or method does not exist
    def _replace_param_list(self, class_name: str, method_name: str):
        # Check if class and method exist or not
        is_class_and_method_exist = self._validate_entities(class_name=class_name, method_name=method_name, class_should_exist=True, method_should_exist=True)
        if not is_class_and_method_exist:
            return
        # Get new parameter names from the user
        user_input = input("\nEnter the names for the new parameter list, each name must be separated by spaces:\n\n==> ")
        new_param_name_list = user_input.split()
        # Check for duplicates in the parameter list
        unique_param_names = list(set(new_param_name_list))
        if len(unique_param_names) != len(new_param_name_list):
            print("\nDuplicate parameters detected:")
            duplicates = [param for param in new_param_name_list if new_param_name_list.count(param) > 1]
            print(f"\nDuplicates: {set(duplicates)}")
            print("\nPlease modify the parameter list manually to ensure uniqueness.")
            return
        # Create parameter objects for the specific method
        new_param_list: List[Parameter] = []
        for param_name in new_param_name_list:
            new_param = self.create_parameter(param_name)
            new_param_list.append(new_param)
        # Replace the parameter list in the specified method
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        method_and_parameter_list[method_name] = new_param_list
        print(f"\nSuccessfully replaced parameter list for method '{method_name}'!")

    ## RELATIONSHIP RELATED ##
    
    # Add relationship wrapper #
    def _add_relationship_wrapper(self, is_loading: bool):
        if len(self.__class_list) == 0:
            print("\nNo class exists!")
            return
        print("\nType '<source_class> <destination_class> <type>' or type 'quit' to return to main menu")
        self.__user_view._display_type_enum()
        self.__user_view._display_class_names(self.__main_data)
        self.__user_view._display_relationships(self.__main_data)
        print("\n==> ", end="")
        user_input: str = input()
        if user_input == "quit":
            print("\nCanceled adding relationship")
            return
        # Split the input by space
        user_input_component = user_input.split()
        # Get separate class name part and type part
        source_class_name = user_input_component[0]
        destination_class_name = (user_input_component[1] if len(user_input_component) > 1 else None)
        type = user_input_component[2] if len(user_input_component) > 2 else None
        # Check if user type the correct format
        if source_class_name and destination_class_name and type:
            # Check if source class exists or not
            is_source_class_exist = self.__validate_class_existence(source_class_name, should_exist=True)
            # If the class does not exist, stop
            if not is_source_class_exist:
                return
            # Check if destination class exists or not
            is_destination_class_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
            # If the class does not exist, stop
            if not is_destination_class_exist:
                return
            # Check if the relationship already exist or not
            is_relationship_exist = self.__relationship_exist(source_class_name, destination_class_name)
            if is_relationship_exist:
                print(f"\nRelation ship between class '{source_class_name}' to class '{destination_class_name}' has already existed!")
                return
            # Checking type, 
            is_type_exist = self.__validate_type_existence(type, should_exist=True)
            if not is_type_exist:
                return
            # If exists, then finally add relationship
            self._add_relationship(source_class_name, destination_class_name, type, is_loading)
        else:
            print("\nWrong format! Please try again!")
            
            
    # Add relationship #
    def _add_relationship(self, source_class_name: str, destination_class_name: str, rel_type: str, is_loading: bool):
        # Create new relationship
        new_relationship = self.create_relationship(source_class_name, destination_class_name, rel_type)
        # Add new relationship to the list
        self.__relationship_list.append(new_relationship)
        if not is_loading:
            print(f"\nSuccessfully added relationship from class '{source_class_name}' to class '{destination_class_name}' of type '{rel_type}'!")
        
    # Delete relationship #
    def _delete_relationship(self, source_class_name: str, destination_class_name: str):
        # Check if source class exists or not
        is_source_class_exist = self.__validate_class_existence(source_class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_source_class_exist:
            return
        # Check if destination class exists or not
        is_destination_class_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_destination_class_exist:
            return
        # Check if the relationship already exist or not
        is_relationship_exist = self.__relationship_exist(source_class_name, destination_class_name)
        if not is_relationship_exist:
            print(f"\nRelation ship between class '{source_class_name}' to class '{destination_class_name}' does not exist!")
            return
        # Get chosen relationship
        current_relationship = self.__get_chosen_relationship(source_class_name, destination_class_name)
        # Remove relationship
        self.__relationship_list.remove(current_relationship)
        print(f"\nSuccessfully removed relationship between class '{source_class_name}' to class '{destination_class_name}'!")  
    
    # Change type #
    def _change_type(self, source_class_name: str, destination_class_name: str, new_type: str):
        # Check if class names are identical or not
        if source_class_name == destination_class_name:
            print("\nNo relationship from a class to itself!")
            return
        # Check source class existence
        is_source_class_name_exist = self.__validate_class_existence(source_class_name, should_exist=True)
        if not is_source_class_name_exist:
            return
        # Check destination class existence
        is_destination_class_name_exist = self.__validate_class_existence(destination_class_name, should_exist=True)
        if not is_destination_class_name_exist:
            return
        # Check if new type is identical to current type:
        current_type = self.__get_chosen_relationship_type(source_class_name, destination_class_name)
        if current_type == new_type:
            print(f"\nNew type '{new_type}' is identical to the existing type of the current relationship!")
            return
        # Check if type already existed or not
        is_type_exist = self.__validate_type_existence(new_type, should_exist=True)
        if not is_type_exist:
            return
        current_relationship = self.__get_chosen_relationship(source_class_name, destination_class_name)
        if current_relationship is None:
            return
        current_relationship._set_type(new_type)
        print(f"\nSuccessfully changed the type between class '{source_class_name}' and class '{destination_class_name}' to '{new_type}'!")
            
    #################################################################
    ### HELPER FUNCTIONS ###  
    
    ## CLASS RELATED ## 

    # Validate if the class name exists in the class list #
    def __class_exists(self, class_name: str) -> bool:
        return class_name in self.__class_list
    
    # Validate class name based on whether it should exist or not #
    def __validate_class_existence(self, class_name: str, should_exist: bool) -> bool:
        # When class name should exist but it does not
        is_class_name_exist = self.__class_exists(class_name)
        if should_exist and not is_class_name_exist:
            print(f"\nClass '{class_name}' does not exist!")
            return False
        # When class name should not exist but it does
        elif not should_exist and is_class_name_exist:
            print(f"\nClass '{class_name}' has already existed!")
            return False
        # True in any other cases
        return True

    # Check if we are able to rename class #
    def __check_class_rename(self, current_class_name: str, new_class_name: str) -> bool:
        # Check if current class name exists or not
        is_current_class_name_exist = self.__validate_class_existence(current_class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_current_class_name_exist:
            return False
        # Check if new class name exists or not
        is_new_class_name_exist = self.__validate_class_existence(new_class_name, should_exist=False)
        # If the class has already existed, stop
        if not is_new_class_name_exist:
            return False
        return True
    
    # Clean Up Relationship #
    def __clean_up_relationship(self, class_name: str):
        # Create a new list that excludes relationships with dest or source equal to class_name
        relationship_list = self.__relationship_list
        relationship_list[:] = [
            relationship
            for relationship in relationship_list
            if relationship._get_source_class() != class_name and relationship._get_destination_class() != class_name
        ]
    
    # Update source/destination class name when we rename a class name #
    def __update_name_in_relationship(self, current_name: str, new_name: str):
        # Get relationship list
        relationship_list = self.__relationship_list
        # Loop through the relationship list
        for each_relationship in relationship_list:
            source_name = each_relationship._get_source_class()
            destination_name = each_relationship._get_destination_class()
            if source_name == current_name:
                each_relationship._set_source_class(new_name)
            elif destination_name == current_name:
                each_relationship._set_destination_class(new_name)
                
    # Get method and parameter list of a chosen class #
    def _get_method_and_parameter_list(self, class_name: str) -> Dict[str, List[Parameter]] | None:
        is_class_name_exist = self.__validate_class_existence(class_name, should_exist=True)
        if not is_class_name_exist:
            return None
        return self.__class_list[class_name]._get_method_and_parameters_list()
    
    ## FIELD AND METHOD RELATED ##
    
    # Check field/method name exist or not #
    def __field_or_method_exist(self, class_name: str, input_name: str, is_field: bool) -> bool:
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Select the correct list based on is_field
        if is_field:
            general_list = class_object._get_class_field_list()
        else:
            general_list = class_object._get_class_method_list()
        # Loop through the list to find the field or method name 
        for element in general_list:
            current_name = element._get_name()
            # If exists, return true
            if current_name == input_name:
                return True
        return False
    
    # Validate field name based on whether it should exist or not #
    def __validate_field_existence(self, class_name: str,  field_name: str, should_exist: bool) -> bool:
        # When field name should exist but it does not
        is_field_name_exist = self.__field_or_method_exist(class_name, field_name, is_field=True)
        if should_exist and not is_field_name_exist:
            print(f"\nField '{field_name}' does not exist in class '{class_name}'!")
            return False
        # When field name should not exist but it does
        elif not should_exist and is_field_name_exist:
            print(f"\nField '{field_name}' has already existed in class '{class_name}'!")
            return False
        return True
    
    # Validate method name based on whether it should exist or not #
    def __validate_method_existence(self, class_name: str,  method_name: str, should_exist: bool) -> bool:
        # When method name should exist but it does not
        is_method_name_exist = self.__field_or_method_exist(class_name, method_name, is_field=False)
        if should_exist and not is_method_name_exist:
            print(f"\nMethod '{method_name}' does not exist in class '{class_name}'!")
            return False
        # When method name should not exist but it does
        elif not should_exist and is_method_name_exist:
            print(f"\nMethod '{method_name}' has already existed in class '{class_name}'!")
            return False
        return True
    
    # Check if we are able to rename field/method #
    def __check_field_or_method_rename(self, class_name: str, current_name: str, new_name: str, is_field: bool) -> bool:
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        if not is_class_exist:
            return
        if is_field:
            # Check if current field name exists or not
            is_current_field_name_exist = self.__validate_field_existence(class_name, current_name, should_exist=True)
             # If the field does not exist, stop
            if not is_current_field_name_exist:
                return False
             # Check if new field name exists or not
            is_new_name_exist = self.__validate_field_existence(class_name, new_name, should_exist=False)
            # If the field has already existed, stop
            if not is_new_name_exist:
                return False
        else:
            # Check if current method name exists or not
            is_current_method_name_exist = self.__validate_method_existence(class_name, current_name, should_exist=True)
             # If the method does not exist, stop
            if not is_current_method_name_exist:
                return False
             # Check if new method name exists or not
            is_new_name_exist = self.__validate_method_existence(class_name, new_name, should_exist=False)
            # If the method has already existed, stop
            if not is_new_name_exist:
                return False
        return True
    
    # Get the chosen field #
    def __get_chosen_field_or_method(self, class_name: str,  input_name: str, is_field: bool) -> Field | Method | None:
        # Get class object
        class_object = self.__class_list[class_name]
        # Select the correct list based on is_field
        if is_field:
            general_list = class_object._get_class_field_list()
        else:
            general_list = class_object._get_class_method_list()
        # Find the chosen object
        # Loop through the list to find the object name 
        for element in general_list:
            current_name = element._get_name()
            # If exists, return the field
            if current_name == input_name:
                return element
        return None
    
    ## PARAMETER RELATED ##
    
    # Parameter check #
    def __parameter_exist(self,class_name:str, method_name: str, parameter_name: str) -> bool:
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        if method_name not in method_and_parameter_list:
           print(f"\nMethod '{method_name}' does not exist!")
           return False
        parameter_list = method_and_parameter_list[method_name]
        for parameter in parameter_list:
            if parameter_name == parameter._get_parameter_name():
                return True
        return False
    
    # Validate parameter existence #
    def __validate_parameter_existence(self, class_name: str, method_name: str, parameter_name: str, should_exist: bool) -> bool:
        is_parameter_exist = self.__parameter_exist(class_name, method_name, parameter_name)
        # If should exist but not exist, return false
        if should_exist and not is_parameter_exist:
            print(f"\nParameter '{parameter_name}' does not exist!")
            return False
        # If should not exist but exists, return false
        elif not should_exist and is_parameter_exist:
            print(f"\nParameter '{parameter_name}' has already existed!")
            return False
        return True
    
    # Get chosen parameter #
    def __get_chosen_parameter(self, class_name: str, method_name: str, parameter_name: str) -> Parameter:
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_name)
        parameter_list = method_and_parameter_list[method_name]
        for each_parameter in parameter_list:
            if each_parameter._get_parameter_name() == parameter_name:
                return each_parameter
        return None
           
    ## RELATIONSHIP RELATED ##
    
    # Relationship type check #
    def __type_exist(self, type_name: str) -> bool:
        RelationshipType = self.__user_view._get_enum_list()
        if type_name in RelationshipType._value2member_map_:
            return True
        return False
    
    # Validate type name based on whether it should exist or not #
    def __validate_type_existence(self, type_name: str, should_exist: bool) -> bool:
        is_type_exist = self.__type_exist(type_name)
        if should_exist and not is_type_exist:
            print(f"\nType '{type_name}' does not exist!")
            return False
        return True

    # Check relationship exists or not #
    def __relationship_exist(self, source_class_name: str, destination_class_name: str) -> bool:
        # Get relationship list
        relationship_list = self.__relationship_list
        for each_relationship in relationship_list:
            current_source_class_name = each_relationship._get_source_class()
            current_destination_class_name = each_relationship._get_destination_class()
            if current_source_class_name == source_class_name and current_destination_class_name == destination_class_name:
                return True
        return False
    
    # Get chosen relationship #
    def __get_chosen_relationship(self, source_class_name: str, destination_class_name: str) -> Relationship:
        # Get relationship list
        relationship_list = self.__relationship_list
        for each_relationship in relationship_list:
            current_source_class_name = each_relationship._get_source_class()
            current_destination_class_name = each_relationship._get_destination_class()
            if current_source_class_name == source_class_name and current_destination_class_name == destination_class_name:
                return each_relationship
        return None
    
    # Get chosen relationship type #
    def __get_chosen_relationship_type(self, source_class_name: str, destination_class_name: str) -> str | None:
        current_relationship = self.__get_chosen_relationship(source_class_name, destination_class_name)
        if current_relationship is not None:
            return current_relationship._get_type()
        print(f"\nNo relationship between class '{source_class_name}' and class '{destination_class_name}'!")
        return None
            
    #################################################################
    ### JSON FORMAT ###
    
    # Get field format list #
    def _get_field_format_list(self, class_object: Class) -> List[Dict]:
        # Get field list
        field_list = class_object._get_class_field_list()
         # Field format list
        field_list_format: List[Dict] = []
        for each_field in field_list:
            attr_json_format = each_field._convert_to_json_field()
            field_list_format.append(attr_json_format)
        return field_list_format
    
    # Get method format list #
    def _get_method_format_list(self, class_object: Class) -> List[Dict]:
        # Get field list
        method_list = class_object._get_class_method_list()
        # Field format list
        method_list_format: List[Dict] = []
        # Get method and parameter list
        method_and_parameter_list = self._get_method_and_parameter_list(class_object._get_class_name())
        for each_method in method_list:
            method_json_format = each_method._convert_to_json_method()
            # Get current parameter list of current method
            parameter_list = method_and_parameter_list[each_method._get_name()]
            # Convert parameters to json format and save to a list
            parameter_format_list: List[Dict] = []
            for each_parameter in parameter_list:
                parameter_format_list.append(each_parameter._convert_to_json_parameter())
            # Add method format to the format list
            method_list_format.append(method_json_format)
            # Add parameter list to parameter format list
            for each_method_format in method_list_format:
                if each_method_format["name"] == each_method._get_name():
                    for each_param_format in parameter_format_list:    
                        each_method_format["params"].append(each_param_format)
        return method_list_format
    
    # Get relationship format list #
    def _get_relationship_format_list(self) -> List[Dict]:
        # Get relationship list
        relationship_list = self.__relationship_list
        # Relationship format list
        relationship_list_format: list[Dict] = []
        for each_relationship in relationship_list:
            rel_json_format = each_relationship._convert_to_json_relationship()
            relationship_list_format.append(rel_json_format)
        return relationship_list_format
    
    # Combine class json format #
    def _class_json_format(self, class_name: str) -> Dict:
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get class format
        class_format = class_object._convert_to_json_uml_class()
        # Assign class name
        class_format["name"] = class_object._get_class_name()
        # Field list format
        field_list_format: List[Dict] = self._get_field_format_list(class_object)       
        # Assign field list format
        class_format["fields"] = field_list_format
        # Method list format
        method_list_format: List[Dict] = self._get_method_format_list(class_object)
        # Assign method list format
        class_format["methods"] = method_list_format
        return class_format
    
    #################################################################
    ### SAVE/LOAD ###
    
    # Save data #
    def _save(self):
        # Prompt the user for a file name to save
        print("\nPlease provide a name for the file you'd like to save or choose file from the list to override.")
        print("Type 'quit' to go back to main menu:")
        # Show the list of saved files
        saved_list = self.__storage_manager._get_saved_list()
        self.__user_view._display_saved_list(saved_list)
        print("==> ", end="")
        user_input = input()
        # Prevent user from overriding NAME_LIST.json
        if user_input == "NAME_LIST":
            print(f"\nYou can't save to '{user_input}.json'")
            return 
        if user_input == "quit":
            print("\nCanceled saving!")
            return
        # Class data list to put in the main data
        class_data_list = []
        # Relationship list to put in the main data
        relationship_data_list = []
        main_data = self.__update_main_data_from_loaded_file(user_input, class_data_list, relationship_data_list)
        self.__storage_manager._save_data_to_json(user_input, main_data)
        print(f"\nSuccessfully saved data to '{user_input}.json'!")
        
    # Load data #
    def _load(self):
        # Prompt the user for a file name to save
        print("\nPlease provide a name for the file you'd like to load.")
        print("Type 'quit' to go back to main menu:")
        # Show the list of saved files
        save_list = self.__storage_manager._get_saved_list()
        self.__user_view._display_saved_list(save_list)
        print("==> ", end="")
        user_input = input()
        # Prevent user from loading NAME_LIST.json
        if user_input == "NAME_LIST":
            print(f"\nYou can't load from '{user_input}.json'")
            return 
        if user_input == "quit":
            print("\nCanceled loading!")
            return
        is_loading = self._saved_file_name_check(user_input)
        if not is_loading:
            print(f"\nFile '{user_input}.json' does not exist")
            return
        main_data = self.__main_data = self.__storage_manager._load_data_from_json(user_input)
        self.__update_data_members(main_data)
        self.__check_file_and_set_status(user_input)
        print(f"\nSuccessfully loaded data from '{user_input}.json'!")
        
    # Update main data to store data to json file #
    def __update_main_data_from_loaded_file(self, user_input: str, class_data_list: List, relationship_data_list: List) -> Dict:
        relationship_data_list = self._get_relationship_format_list()
        main_data = self.__main_data
        # Add file name to saved list if it is a new one
        self.__storage_manager._add_name_to_saved_file(user_input)
        for class_name in self.__class_list:
            class_data_format = self._class_json_format(class_name)
            class_data_list.append(class_data_format)
        main_data["classes"] = class_data_list
        main_data["relationships"] = relationship_data_list
        return main_data
    
    # Update UMLCoreManager data after loading a file #
    def __update_data_members(self, main_data: Dict):
        class_data = main_data["classes"]
        relationship_data = main_data["relationships"]
        self.__reset_storage()
        # Set main data again
        self.__main_data = main_data
        # Re-create class, field, method and parameter
        extracted_class_data = self._extract_class_data(class_data)
        for each_pair in extracted_class_data:
            for class_name, data in each_pair.items(): 
                field_list = data['fields']
                method_param_list = data['methods_params']
                # Add the class
                self._add_class(class_name, is_loading=True)
                # Add the fields for the class
                for each_field in field_list:
                    self._add_field(class_name, each_field, is_loading=True)
                # Add the methods and its parameters for the class
                for method_name, param_list in method_param_list.items():
                    self._add_method(class_name, method_name, is_loading=True)
                    for param_name in param_list:
                        self._add_parameter(class_name, method_name, param_name, is_loading=True)
        # Re-create relationship 
        for each_dictionary in relationship_data:
            self._add_relationship(each_dictionary["source"], each_dictionary["destination"], each_dictionary["type"], is_loading=True)
        
    # This function help extracting class, field and method from json file and put into a list #
    def _extract_class_data(self, class_data: List[Dict]) -> List[Dict[str, Dict[str, List | Dict]]]:
        # Create a list of type List[Dict[str, Dict[str, List | Dict]]] (*NOTE* THIS TYPE CAUSED ME SEVERE HEADACHE T_T)
        class_info_list: List[Dict[str, Dict[str, List | Dict]]] = []
        # Loop through each class element
        for class_element in class_data:
            # Create a dictionary to store method name and its litst of parameters
            method_and_param_list = {}
            # Get class name
            class_name = class_element["name"]
            # Get list of field names
            fields = [field["name"] for field in class_element["fields"]]
            # Extract method and its parameters into 'method_and_param_list'
            for method_element in class_element["methods"]:
                temp_param_list: List[str] = []
                for param_element in method_element["params"]:
                    temp_param_list.append(param_element["name"])
                method_and_param_list[method_element["name"]] = temp_param_list
            class_info_list.append({class_name: {'fields': fields, 'methods_params': method_and_param_list}})
        return class_info_list
    
    # Delete Saved File #
    def _delete_saved_file(self):
        print("\nPlease choose a file you want to delete.")
        print("Type 'quit' to go back to main menu:")
        saved_list = self.__storage_manager._get_saved_list()
        self.__user_view._display_saved_list(saved_list)
        user_input = input()
        # Prevent user from loading NAME_LIST.json
        if user_input == "NAME_LIST":
            print(f"\nYou can't delete file '{user_input}.json'")
            return 
        if user_input == "quit":
            print("\nCanceled loading!")
            return
        is_file_exist = self._check_saved_file_exist(user_input)
        if not is_file_exist:
            print(f"File '{user_input}.json' does not exist!")
            return
        # Get saved file's name list
        save_list = self.__storage_manager._get_saved_list()
        for dictionary in save_list:
            if user_input in dictionary:
                save_list.remove(dictionary)
        # Update the saved list 
        self.__storage_manager._update_saved_list(save_list)
        # Physically remove the file   
        file_path = f"UML_UTILITY/SAVED_FILES/{user_input}.json"
        os.remove(file_path)
        print(f"\nSuccessfully removed file '{user_input}.json'")
        
    # Check if a saved file exist #
    def _check_saved_file_exist(self, file_name: str):
        saved_list = self.__storage_manager._get_saved_list()
        for element in saved_list:
            for name in element:
                if file_name == name:
                    return True
        return False
    
    # End Session To Go Back To Blank Program #
    def _end_session(self):
        self.__set_all_file_off()
        self.__reset_storage()
        print("\nSuccessfully back to default program!")
    
    # Get active file #
    def _get_active_file(self) -> str:
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key, val in each_dictionary.items():
                if val == "on":
                    return key
        return "No active file!"
    
    # Clear the current active file #
    def _clear_current_active_data(self):
        saved_list = self.__storage_manager._get_saved_list()
        if len(saved_list) == 0:
            print("\nNo file!")
            return
        current_active_file = self._get_active_file()
        if current_active_file == "No active file!":
            print("\nNo active file!")
            return
        self.__reset_storage()
        self.__storage_manager._save_data_to_json(current_active_file, self.__main_data)
        print(f"\nSuccessfully clear data in file '{current_active_file}.json'")
        
    def _exit(self):
        self.__set_all_file_off()
        print("\nExited Program")
    
    # Set all file status to off #
    def __set_all_file_off(self):
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                each_dictionary[key] = "off"
        self.__storage_manager._update_saved_list(saved_list)
    
    # Set file status #
    def __set_file_status(self, file_name: str, status: str):
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                if key == file_name:
                    each_dictionary[key] = status
    
    # Check file name and set its status #               
    def __check_file_and_set_status(self, file_name: str) -> str:
        saved_list = self.__storage_manager._get_saved_list()
        for each_dictionary in saved_list:
            for key in each_dictionary:
                if each_dictionary[key] == "on":
                    each_dictionary[key] = "off"
        self.__set_file_status(file_name, status="on")
        # Update the saved list 
        self.__storage_manager._update_saved_list(saved_list)
        
    # Reset all storage #
    def __reset_storage(self):
        self.__class_list: Dict[str, Class] = {}
        self.__relationship_list: List = []
        self.__main_data: Dict = {}
    
    #################################################################
    ### INTERFACE ###
    
    ## HANDLE USER INPUT FOR INTERFACE ##

    # Processing main program including user input #
    def _process_command(self, command: str, parameters: List[str]):
        # Paremeter
        first_param = parameters[0] if len(parameters) > 0 else None
        second_param = parameters[1] if len(parameters) > 1 else None
        third_param = parameters[2] if len(parameters) > 2 else None
        fourth_param = parameters[3] if len(parameters) > 3 else None
        # Start the logic
        #######################################################
        
        # Add class
        if command == InterfaceOptions.ADD_CLASS.value and first_param:
            self._add_class(first_param, is_loading=False)
        # Delete class
        elif command == InterfaceOptions.DELETE_CLASS.value and first_param:
            self._delete_class(first_param)
        # Rename class
        elif (
            command == InterfaceOptions.RENAME_CLASS.value
            and first_param
            and second_param
        ):
            self._rename_class(first_param, second_param)

        #######################################################

        # Add parameter #
        elif (
            command == InterfaceOptions.ADD_FIELD.value
            and first_param
            and second_param
        ):
            self._add_field(first_param, second_param, is_loading=False)
        # Delete parameter #
        elif (
            command == InterfaceOptions.DELETE_FIELD.value
            and first_param
            and second_param
        ):
            self._delete_field(first_param, second_param)
        # Rename parameter #
        elif (
            command == InterfaceOptions.RENAME_FIELD.value
            and first_param
            and second_param
            and third_param
        ):
            self._rename_field(first_param, second_param, third_param)

        #######################################################
            
        # Add method #
        elif (
            command == InterfaceOptions.ADD_METHOD.value
            and first_param
            and second_param
        ):
            self._add_method(first_param, second_param, is_loading=False)
        # Delete method #
        elif (
            command == InterfaceOptions.DELETE_METHOD.value
            and first_param
            and second_param
        ):
            self._delete_method(first_param, second_param)
        # Rename method #
        elif (
            command == InterfaceOptions.RENAME_METHOD.value
            and first_param
            and second_param
            and third_param
        ):
            self._rename_method(first_param, second_param, third_param)
            
        #######################################################
            
        # Add parameter #
        elif (
            command == InterfaceOptions.ADD_PARAM.value
            and first_param
            and second_param
            and third_param
        ):
            self._add_parameter(first_param, second_param, third_param, is_loading=False)
        # Delete parameter #
        elif (
            command == InterfaceOptions.DELETE_PARAM.value
            and first_param
            and second_param
            and third_param
        ):
            self._delete_parameter(first_param, second_param, third_param)
        # Rename parameter #
        elif (
            command == InterfaceOptions.RENAME_PARAM.value
            and first_param
            and second_param
            and third_param
            and fourth_param
        ):
            self._rename_parameter(first_param, second_param, third_param, fourth_param)
        # Replace parameter list #
        elif command == InterfaceOptions.REPLACE_PARAM.value and first_param and second_param:
            self._replace_param_list(first_param, second_param)
            
        #######################################################

        # Add relationship
        elif (
            command == InterfaceOptions.ADD_REL.value
        ):
            self._add_relationship_wrapper(is_loading=False)
        # Delete relationship #
        elif (
            command == InterfaceOptions.DELETE_REL.value
            and first_param
            and second_param
        ):
            self._delete_relationship(first_param, second_param)
        # Chang relationship type #
        elif (
            command == InterfaceOptions.TYPE_MOD.value 
            and first_param
            and second_param
            and third_param
        ):
            self._change_type(first_param, second_param, third_param)
                
        #######################################################
                
        # List all the created class names or all class detail #
        elif command == InterfaceOptions.LIST_CLASS.value:
            self.__user_view._display_wrapper(self.__main_data) 
        # Show the details of the chosen class #
        elif command == InterfaceOptions.CLASS_DETAIL.value and first_param:
            self.__user_view._display_single_class(first_param, self.__main_data)
        # Show the relationship of the chosen class with others #
        elif command == InterfaceOptions.CLASS_REL.value:
            self.__user_view._display_relationships(self.__main_data)
        # Show the list of saved files #
        elif command == InterfaceOptions.SAVED_LIST.value:
            saved_list = self.__storage_manager._get_saved_list()
            self.__user_view._display_saved_list(saved_list)
        # Save the data #
        elif command == InterfaceOptions.SAVE.value:
            self._save()
        # Load the data #
        elif command == InterfaceOptions.LOAD.value:
            self._load()
        # Delete saved file #
        elif command == InterfaceOptions.DELETE_SAVED.value:
            self._delete_saved_file()
        # Clear data in current storage #
        elif command == InterfaceOptions.CLEAR_DATA.value:
            self._clear_current_active_data()
        # Go back to blank program #
        elif command == InterfaceOptions.DEFAULT.value:
            self._end_session()
        # Sort the class list #
        elif command == InterfaceOptions.SORT.value:
            self._sort_class_list()
        else:
            print(f"\nUnknown command '{command}'. Type 'help' for a list of commands.")

    # Sorting Class List #
    def _sort_class_list(self):
        class_list = self.__class_list
        if len(class_list) == 0:
            print("\nNo class to sort!")
            return
        self.__class_list = dict(sorted(self.__class_list.items()))
        self._update_main_data_for_every_action()
        self.__user_view._display_uml_data(self.__main_data)
        
    #################################################################
    ### UTILITY FUNCTIONS ###  
        
    # Saved file check #
    def _saved_file_name_check(self, save_file_name: str) -> bool:
        saved_list = self.__storage_manager._get_saved_list()
        for each_pair in saved_list:
            for file_name in each_pair:
                if file_name == save_file_name:
                    return True
        return False
                
    # Update main data wrapper #
    def _update_main_data_for_every_action(self):
        # Class data list to put in the main data
        class_data_list = []
        relationship_data_list = self._get_relationship_format_list()
        main_data = self.__main_data
        # Add file name to saved list if it is a new one
        for class_name in self.__class_list:
            class_data_format = self._class_json_format(class_name)
            class_data_list.append(class_data_format)
        main_data["classes"] = class_data_list
        main_data["relationships"] = relationship_data_list
    
    # Validate entities (Class, Method, Field, Parameter)          
    def _validate_entities(
        self, 
        class_name: str = None, 
        field_name: str = None, 
        method_name: str = None, 
        parameter_name: str = None, 
        class_should_exist: bool = None, 
        field_should_exist: bool = None,
        method_should_exist: bool = None, 
        parameter_should_exist: bool = None
    ) -> bool:
        """
        General validation function for class, field, method, and parameter existence.
        - class_name: Name of the class to check.
        - field_name: Name of the field to check.
        - method_name: Name of the method to check.
        - parameter_name: Name of the parameter to check.
        - class_should_exist: Whether the class should exist (True) or not (False).
        - field_should_exist: Whether the field should exist (True) or not (False).
        - method_should_exist: Whether the method should exist (True) or not (False).
        - parameter_should_exist: Whether the parameter should exist (True) or not (False).
    
        Returns True if all required entities exist (or don't exist) as expected, otherwise False.
        """
        # Check class existence if specified
        if class_name is not None and class_should_exist is not None:
            is_class_exist = self.__validate_class_existence(class_name, class_should_exist)
            if not is_class_exist:
                return False
        # Check field existence if specified
        if field_name is not None and field_should_exist is not None:
            is_field_exist = self.__validate_field_existence(class_name, field_name, field_should_exist)
            if not is_field_exist:
                return False
        # Check method existence if specified
        if method_name is not None and method_should_exist is not None:
            is_method_exist = self.__validate_method_existence(class_name, method_name, method_should_exist)
            if not is_method_exist:
                return False
        # Check parameter existence if specified
        if parameter_name is not None and parameter_should_exist is not None:
            is_parameter_exist = self.__validate_parameter_existence(class_name, method_name, parameter_name, parameter_should_exist)
            if not is_parameter_exist:
                return False
        # All checks passed
        return True
                       
###################################################################################################