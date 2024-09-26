class UMLParameter:
    # UML class attribute constructor
    # Create an attribute to add to the UML Class
    def __init__(
        self,
        parameter_name: str,
    ):
        self.__parameter_name = parameter_name

    def __str__(self):
        return f"{self.__parameter_name}"
        
    #################################################################
    # Method to get attribute's data members #
    def _get_parameter_name(self) -> str:
        return self.__parameter_name

    #################################################################
    # Method to modify attribute's data members #
    def _set_parameter_name(self, new_name: str):
        self.__parameter_name = new_name

    #################################################################
    # Method to convert parameter to json format #
    def _convert_to_json_parameter(self) -> dict[str, str]:
        return {"name": self.__parameter_name}