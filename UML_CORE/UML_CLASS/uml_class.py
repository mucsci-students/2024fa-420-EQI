from typing import List, Tuple

############################################################################################
# @NOTE: For this class, I will assume that we already had                                 #
# Attribute and Relationship class, which will be imported as below:                       #
#                                                                                          #
# from UML_CORE.UML_ATTRIBUTE.uml_attribute import UMLAttribute as Attribute               #
# from UML_CORE.UML_RELATIONSHIP.uml_relationship import UMLRelationship as Relationship   #
############################################################################################


class UMLClass:
    #################################################################
    # Uml class constructor
    # Create UML class with a name including:
    # @param class_name: Name of the class we want to create
    def __init__(self, class_name: str):
        self.__class_name = class_name

        # Store attribute name and the related attribute object
        # so we can easily access to the its details
        # Official when Attribute class is implemented, for now is 'str' type:
        # => self.__attribute_list: List[Tuple[str, Attribute]] = []
        self.__attribute_list: List[Tuple[str, str]] = []

        # Store source class, destination class, and the type of relationship
        # (e.g. Composition, Aggregation, etc.)
        # Official when Relationship class is implemented, for now is 'str' type:
        # => self.__relationship_list: List[Tuple[str, Relationship]] = []
        self.__relationship_list: List[Tuple[str, str]] = []

    #################################################################
    # Method to get UML class's data members #
    def _get_class_name(self) -> str:
        return self.__class_name

    # Official when Attribute class is implemented, for now is 'str' type:
    # => List[Tuple[str, Attribute]]
    def _get_class_attribute_list(self) -> List[Tuple[str, str]]:
        return self.__attribute_list

    # Official when Attribute class is implemented, for now is 'str' type:
    # => List[Tuple[str, Attribute]]
    def _get_class_relationship_list(self) -> List[Tuple[str, str]]:
        return self.__relationship_list

    #################################################################
    # Method to modify UML class's data members #
    def _set_class_name(self, new_class_name: str):
        self.__class_name = new_class_name

    # Official when Attribute class is implemented, for now is 'str' type:
    # => List[Tuple[str, Attribute]]
    def _set_class_attribute_list(self, new_attribute_list: List[Tuple[str, str]]):
        self.__attribute_list = new_attribute_list

    # Official when Attribute class is implemented, for now is 'str' type:
    # => List[Tuple[str, Attribute]]
    def _set_class_relationship_list(self, new_relationship_list: List[dict[str, str]]):
        self.__relationship_list = new_relationship_list
