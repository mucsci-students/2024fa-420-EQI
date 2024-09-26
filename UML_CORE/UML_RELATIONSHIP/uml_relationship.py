class UMLRelationship:
    # UML class relationship constructor
    # Create a relationship between classes
    def __init__(
        self,
        source_class: str,
        destination_class: str,
        rel_type: str
    ):
        self.__source_class = source_class
        self.__destination_class = destination_class
        self.__rel_type = rel_type
        
    def __str__(self):
        return f"Source: {self.__source_class}\nDestination: {self.__destination_class}\nType: {self.__rel_type}"
        

    #################################################################
    # Method to get UML Class Relationship data members #
    def _get_source_class(self) -> str:
        return self.__source_class

    def _get_destination_class(self) -> str:
        return self.__destination_class
    
    def _get_type(self) -> str:
        return self.__rel_type

    #################################################################
    # Method to modify UML Class Relationship data members #
    def _set_source_class(self, new_source: str):
        self.__source_class = new_source

    def _set_destination_class(self, new_destination: str):
        self.__destination_class = new_destination
        
    def _set_type(self, new_type: str):
        self.__rel_type = new_type

    #################################################################
    # Method to convert relationship to json format #
    def _convert_to_json_relationship(self) -> dict[str, str]:
        return {
            "source": self.__source_class,
            "destination": self.__destination_class,
            "type": self.__rel_type
        }
