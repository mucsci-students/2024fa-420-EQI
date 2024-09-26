###################################################################################################

import os
from itertools import zip_longest
from enum import Enum
from typing import Dict, List
from UML_CORE.UML_CLASS.uml_class import UMLClass as Class
from UML_CORE.UML_FIELD.uml_field import UMLField as Field
from UML_CORE.UML_METHOD.uml_method import UMLMethod as Method
from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship as Relationship
from UML_CORE.UML_PARAMETER.uml_parameter import UMLParameter as Parameter
from UML_MANAGER.uml_storage_manager import UMLStorageManager as Storage

###################################################################################################
### ENUM FOR RELATIONSHIP TYPE ###

class RelationshipType(Enum):
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"
    INHERITANCE = "inheritance"
    REALIZATION = "realization"
    
###################################################################################################

class UMLCoreManager:
    
    #################################################################
    
    # UML Class Manager Constructor #
    
    def __init__(self):
        # {class_name : Class} pair
        self.__class_list: Dict[str, Class] = {}
        self.__storage_manager: Storage = Storage()
        self.__relationship_list: List[Relationship] = []
        self.__main_data: Dict = {}
        
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
        is_class_exist = self.__validate_class_existence(class_name, should_exist=False)
        # If the class has already existed, stop
        if not is_class_exist:
            return
        # Else, add the class
        new_class = self.create_class(class_name)
        self.__class_list[class_name] = new_class
        if not is_loading:
            print(f"\nSuccessfully added class '{class_name}'!")
        
    # Delete class #
    def _delete_class(self, class_name: str, is_loading: bool):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Else, delete class
        self.__class_list.pop(class_name)
        # Clean up connected relationship
        self.__clean_up_relationship(class_name)
        if not is_loading:
            print(f"\nSuccessfully removed class '{class_name}'!")
        
    # Rename class #
    def _rename_class(self, current_name: str, new_name: str, is_loading: bool):
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
        if not is_loading:
            print(f"\nSuccessfully renamed from class '{current_name}' to class '{new_name}'!")
        
    ## FIELD RELATED ##
    
    # Add field #
    def _add_field(self, class_name: str, field_name: str, is_loading: bool):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Check if field exists or not
        is_field_exist = self.__validate_field_existence(class_name, field_name, should_exist=False)
        # If the field has already existed, stop
        if not is_field_exist:
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
    def _delete_field(self, class_name: str, field_name: str, is_loading):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Check if field exists or not
        is_field_exist = self.__validate_field_existence(class_name, field_name, should_exist=True)
        # If the field does not exist, stop
        if not is_field_exist:
            return
         # Get class object
        class_object = self.__class_list[class_name]
        # Get field list
        field_list = class_object._get_class_field_list()
        # Get the field
        chosen_field = self.__get_chosen_field_or_method(class_name, field_name, is_field=True)
        # Remove the chosen field 
        field_list.remove(chosen_field)
        if not is_loading:
            print(f"\nSuccessfully removed field '{field_name}'!")
        
    # Rename field #
    def _rename_field(self, class_name: str, current_field_name: str, new_field_name: str, is_loading: bool):
        is_able_to_rename = self.__check_field_or_method_rename(class_name, current_field_name, new_field_name, is_field=True)
        if not is_able_to_rename:
            return
        # Get the field
        chosen_field = self.__get_chosen_field_or_method(class_name, current_field_name, is_field=True)
        chosen_field._set_name(new_field_name)
        if not is_loading:
            print(f"\nSuccessfully renamed from field '{current_field_name}' to field '{new_field_name}'!")
        
    ## METHOD RELATED ##
    
    # Add method #
    def _add_method(self, class_name: str, method_name: str, is_loading: bool):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Check if method exists or not
        is_method_exist = self.__validate_method_existence(class_name, method_name, should_exist=False)
        # If the field has already existed, stop
        if not is_method_exist:
            return
        # Get class object
        class_object = self.__class_list[class_name]
        # Get field list
        method_list = class_object._get_class_method_list()
        # Create new method
        new_method = self.create_method(method_name)
        # Add method
        method_list.append(new_method)
        if not is_loading:
            print(f"\nSuccessfully added method '{method_name}'!")
        
    # Delete method #
    def _delete_method(self, class_name: str, method_name: str, is_loading):
        # Check if class exists or not
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        # If the class does not exist, stop
        if not is_class_exist:
            return
        # Check if method exists or not
        is_method_exist = self.__validate_method_existence(class_name, method_name, should_exist=True)
        # If the method does not exist, stop
        if not is_method_exist:
            return
         # Get class object
        class_object = self.__class_list[class_name]
        # Get method list
        method_list = class_object._get_class_method_list()
        # Get the method
        chosen_method = self.__get_chosen_field_or_method(class_name, method_name, is_field=False)
        # Remove the chosen field 
        method_list.remove(chosen_method)
        if not is_loading:
            print(f"\nSuccessfully removed method '{method_name}'!")
        
    # Rename method #
    def _rename_method(self, class_name: str, current_method_name: str, new_method_name: str, is_loading: bool):
        is_able_to_rename = self.__check_field_or_method_rename(class_name, current_method_name, new_method_name, is_field=False)
        if not is_able_to_rename:
            return
        # Get the method
        chosen_method = self.__get_chosen_field_or_method(class_name, current_method_name, is_field=False)
        chosen_method._set_name(new_method_name)
        if not is_loading:
            print(f"\nSuccessfully renamed from method '{current_method_name}' to method '{new_method_name}'!")
    
    ## RELATIONSHIP RELATED ##
    
    # Add relationship wrapper #
    def _add_relationship_wrapper(self, is_loading: bool):
        print("\nType '<source_class> <destination_class> <type>")
        print("\nYou must choose one of the types below:")
        self.__display_type_enum()
        print("Below is class list:")
        self.__display_list_of_only_class_name()
        print("\n==> ", end="")
        user_input: str = input()
        # Split the input by space
        user_input_component = user_input.split()
        # Get separate class name part and type part
        source_class_name = user_input_component[0]
        destination_class_name = (user_input_component[1] if len(user_input_component) > 1 else None)
        type = user_input_component[2] if len(user_input_component) > 2 else None
        # Check if user type the correct format
        if source_class_name and destination_class_name and type:
            # Check if class names are identical or not
            if source_class_name == destination_class_name:
                print("\nYou can't create relationship to the class itself!")
                return
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
    def _delete_relationship(self, source_class_name: str, destination_class_name: str, is_loading: bool):
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
        if not is_loading:
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
    
    ## field AND METHOD RELATED ##
    
    # Check field name exist or not #
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
        # Loop through the list to find the field name 
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
    
    # Check if we are able to rename field #
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
            
    ## RELATIONSHIP RELATED ##
    
    # Relationship type check #
    def __type_exist(self, type_name: str) -> bool:
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
        for each_method in method_list:
            method_json_format = each_method._convert_to_json_method()
            method_list_format.append(method_json_format)
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
        self._display_saved_list()
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
        main_data = self.__update_main_data(user_input, class_data_list, relationship_data_list)
        self.__storage_manager._save_data_to_json(user_input, main_data)
        print(f"\nSuccessfully saved data to '{user_input}.json'!")
        
    # Load data #
    def _load(self):
        # Prompt the user for a file name to save
        print("\nPlease provide a name for the file you'd like to load.")
        print("Type 'quit' to go back to main menu:")
        # Show the list of saved files
        self._display_saved_list()
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
    def __update_main_data(self, user_input: str, class_data_list: List, relationship_data_list: List) -> Dict:
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
        # Re-create class, field, object, and method
        extracted_class_data = self._extract_class_data(class_data)
        for each_pair in extracted_class_data:
            for class_name, data in each_pair.items(): 
                field_list = data['fields']
                method_list = data['methods']
                # Add the class
                self._add_class(class_name, is_loading=True)
                # Add the fields for the class
                for each_field in field_list:
                    self._add_field(class_name, each_field, is_loading=True)
                # Add the methods for the class
                for each_method in method_list:
                    self._add_method(class_name, each_method, is_loading=True)
        # Re-create relationship 
        for each_dictionary in relationship_data:
            self._add_relationship(each_dictionary["source"], each_dictionary["destination"], each_dictionary["type"], is_loading=True)
        
    # This function help extracting class, field and method from json file and put into a list #
    def _extract_class_data(self, class_data: List[Dict]) -> List:
        class_info_list = []
        for ele in class_data:
            class_name = ele["name"]
            fields = [field['name'] for field in ele['fields']]
            methods = [method['name'] for method in ele['methods']]
            class_info_list.append({class_name: {'fields': fields,'methods': methods}})
        return class_info_list
    
    # Delete Saved File #
    def _delete_saved_file(self):
        print("\nPlease choose a file you want to delete.")
        print("Type 'quit' to go back to main menu:")
        self._display_saved_list()
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
    ### DISPLAY CLASS ###
    
    # Display wrapper #
    def _display_wrapper(self):
        if len(self.__class_list) == 0:
            print("\nNo class to display!")
            return
        is_detail = self._ask_user_choices("print all class detail")
        if is_detail:
            self._display_class_list_detail()
        else:
            self.__display_list_of_only_class_name()
    
    # Display class list #
    def _display_class_list_detail(self, classes_per_row=3):
        # Generate class details split into lines
        class_details_list = [
            self.__get_class_detail(class_name).split("\n")
            for class_name in self.__class_list
        ]
        print("\n-------------------------------------------------------------------------------------------------\n")
        # Chunk the class details into groups of `classes_per_row`
        for i in range(0, len(class_details_list), classes_per_row):
            chunk = class_details_list[i : i + classes_per_row]

            # Use zip_longest to align and print side by side
            for lines in zip_longest(*chunk, fillvalue=" " * 20):
                print("   ".join(line.ljust(30) for line in lines))
            print("\n-------------------------------------------------------------------------------------------------\n")
            
    # Display Relationship List #
    def _display_relationship_list(self, classes_per_row=3):
        if len(self.__relationship_list) == 0:
            print("\nNo relationship to display!")
            return
        # Generate class details split into lines
        class_relationship_detail_list = [
            self.__get_relationship_detail(class_name).split("\n")
            for class_name in self.__class_list
        ]
        print("\n-------------------------------------------------------------------------------------------------\n")
        # Chunk the class relationship details into groups of `classes_per_row`
        for i in range(0, len(class_relationship_detail_list), classes_per_row):
            chunk = class_relationship_detail_list[i : i + classes_per_row]

            # Use zip_longest to align and print side by side
            for lines in zip_longest(*chunk, fillvalue=" " * 20):
                print("   ".join(line.ljust(30) for line in lines))
            print("\n-------------------------------------------------------------------------------------------------\n")
    
    # Display only list of class names #
    def __display_list_of_only_class_name(self):
        print("\n|===================|")
        print(f"{"--     Name     --":^20}")
        print("|*******************|")
        class_list = self.__class_list
        for class_name in class_list:
            print(f"{class_name:^20}")
        print("|===================|\n")
        
    # Display Class Details #
    def _display_single_class_detail(self, class_name: str):
        classes_detail_list = self.__get_class_detail(class_name)
        if classes_detail_list is not None:
            print(f"\n{classes_detail_list}")
        
    # Display saved file's names #
    def _display_saved_list(self):
        saved_list = self.__storage_manager._get_saved_list()
        if len(saved_list) == 0:
            print("\nNo saved file exists!")
            return
        print("\n|===================|")
        for dictionary in saved_list:
            for key in dictionary:
                print(f"{key:^20}")
        print("|===================|\n")
        
    
    # Get class detail #
    def __get_class_detail(self, class_name: str) -> str:
        is_class_exist = self.__validate_class_existence(class_name, should_exist=True)
        if not is_class_exist:
            return
        class_object = self.__class_list[class_name]
        output = []
        output.append("|===================|")
        output.append(f"{"--     Name     --":^21}")
        output.append(f"{class_name:^20}")
        output.append("|*******************|")
        output.append(f"{"--  Field  --":^21}")
        field_list = class_object._get_class_field_list()
        for field in field_list:
            output.append(f"{field._get_name():^21}")
        output.append("|*******************|")
        output.append(f"{"--  Method  --":^21}")
        method_list = class_object._get_class_method_list()
        for method in method_list:
            output.append(f"{method._get_name():^21}")
        output.append("|*******************|")
        relationship_list = self.__relationship_list
        output.append(f"{"-- Relationship  --":^21}")
        for element in relationship_list:
            if element._get_source_class() == class_name:
                output.append(f"{"--------------":^20}")
                output.append(f"  Source: {class_name}")
                output.append(f"  Destination: {element._get_destination_class()}")
                output.append(f"  Type: {element._get_type()}")
        output.append("|===================|")
        return "\n".join(output)
    
    # Get Class Relationships #
    def __get_relationship_detail(self, class_name: str) -> str:
        class_object = self.__class_list[class_name]
        if class_object is None:
            print(f"\nClass '{class_name}' does not exist!")
            return
        output = []
        output.append("|===================|")
        output.append(f"{"--     Name     --":^21}")
        output.append(f"{class_name:^20}")
        output.append("|*******************|")
        rel_list = self.__relationship_list
        output.append("|===================|")
        output.append(f"{"-- Relationship  --":^21}")
        for element in rel_list:
            if element._get_source_class() == class_name:
                output.append(f"{"|-----------|":^20}")
                output.append(f"{ element._get_source_class():^20}")
                output.append(f"{ element._get_destination_class():^20}")
                output.append(f"{ element._get_type():^20}")
                output.append(f"{"|-----------|":^20}")
        output.append("|===================|")
        return "\n".join(output)
    
    # Sorting Class List #
    def _sort_class_list(self):
        class_list = self.__class_list
        if len(class_list) == 0:
            print("\nNo class to sort!")
            return
        sorted_class_list = dict(sorted(class_list.items()))
        self.__class_list = sorted_class_list
        self._display_class_list_detail()
        
         
    #################################################################
    ### UTILITY FUNCTIONS ###  
    
    # Display type Enum #
    def __display_type_enum(self):
        print("\n|=================|")
        print(f"{"--     Type    --":^20}")
        print("|*****************|")
        for type in RelationshipType:
            print(f"{type.value:^20}")
        print("|=================|\n")
        
    # Saved file check #
    def _saved_file_name_check(self, save_file_name: str) -> bool:
        saved_list = self.__storage_manager._get_saved_list()
        for each_pair in saved_list:
            for file_name in each_pair:
                if file_name == save_file_name:
                    return True
        return False
    
    # Ask For User Choices #
    def _ask_user_choices(self, action: str) -> bool:
        while True:
            user_input = input(f"\nDo you want to {action}? (Yes/No): ").lower()
            if user_input in ["yes", "y"]:
                return True
            elif user_input in ["no", "n"]:
                return False
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")
                
###################################################################################################