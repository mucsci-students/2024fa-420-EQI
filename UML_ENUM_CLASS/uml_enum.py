###################################################################################################

from enum import Enum

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
    
class RelationshipType(Enum):
    """
    Enum for specifying different types of UML relationships.
    The values represent the kind of relationship between classes in a UML diagram.
    """
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"
    INHERITANCE = "inheritance"
    REALIZATION = "realization"
    
###################################################################################################