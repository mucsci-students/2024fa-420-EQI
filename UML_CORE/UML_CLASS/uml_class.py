from typing import List

from UML_CORE.UML_FIELD.uml_field import UMLField as Field
from UML_CORE.UML_METHOD.uml_method import UMLMethod as Method

class UMLClass:
    #################################################################
    # Uml class constructor
    # Create UML class with a name including:
    def __init__(self, class_name: str):
        self.__class_name = class_name
        # Store field name and the related field object
        # so we can easily access to the its details
        self.__field_list: List[Field] = []
        # Store method name and the related method object
        # so we can easily access to the its details
        self.__method_list: List[Method] = []
        # # Store source class, destination class, and the type of relationship (e.g. Composition, Aggregation, etc.)
        # self.__relationship_list: List[Relationship] = []

    #################################################################
    # Method to get UML class's data members #
    def _get_class_name(self) -> str:
        return self.__class_name

    def _get_class_field_list(self) -> List[Field]:
        return self.__field_list

    def _get_class_method_list(self) -> List[Method]:
        return self.__method_list
    
    def __str__(self):
        return f"Class name: {self.__class_name}"

    #################################################################
    # Method to modify UML class's data members #
    def _set_class_name(self, new_class_name: str):
        self.__class_name = new_class_name

    def _set_class_field_list(self, new_field_list: List[Field]):
        self.__field_list = new_field_list

    def _set_class_method_list(self, new_method_list: List[Method]):
        self.__method_list = new_method_list
        
    #################################################################
    # Method to convert uml class to json format #
    def _convert_to_json_uml_class(self) -> dict[str, list]:
        return {
            "name":self.__class_name,
            "fields":[],
            "methods":[]
        }
    