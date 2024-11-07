class UMLMethod:
    # UML class method constructor
    # Create a method to add to the UML Class
    def __init__(self,type: str = "", method_name: str = ""):
        self.__type = type
        self.__method_name = method_name
        
    def __str__(self):
        return f"{self.__type} {self.__method_name}"
       
    #################################################################
    # Method to get attribute's data members #

    def _get_name(self):
        return self.__method_name
    
    def _get_type(self) -> str:
        return self.__type

    #################################################################
    # Method to modify attribute's data members #

    def _set_name(self, new_name: str):
        self.__method_name = new_name

    def _set_type(self, new_name: str):
        self.__type = new_name

    #################################################################
    # Method to convert method to json format #
    def _convert_to_json_method(self) -> dict[str, str]:
        return {"name": self.__method_name, 
                "return_type": self.__type, 
                "params":[],}
