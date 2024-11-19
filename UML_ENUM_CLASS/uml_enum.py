###################################################################################################

from enum import Enum

###################################################################################################

### ENUM VALUES FOR THE INTERFACE ###

class InterfaceOptions(Enum):
    MOVE_UNIT = "move_unit" # This is created  for factory command
    ADD_CLASS = "add_class"
    DELETE_CLASS = "delete_class"
    RENAME_CLASS = "rename_class"
    ADD_FIELD = "add_field"
    DELETE_FIELD = "delete_field"
    RENAME_FIELD = "rename_field"
    EDIT_FIELD_TYPE = "edit_field_type"
    ADD_METHOD = "add_method"
    DELETE_METHOD = "delete_method"
    RENAME_METHOD = "rename_method"
    EDIT_METHOD_TYPE = "edit_method_type"
    ADD_PARAM = "add_param"
    DELETE_PARAM = "delete_param"
    RENAME_PARAM = "rename_param"
    EDIT_PARAM_TYPE = "edit_param_type"
    REPLACE_PARAM = "replace_param"
    PARAM_TYPE = "param_type"
    ADD_REL = "add_rel"
    DELETE_REL = "delete_rel"
    EDIT_REL_TYPE = "edit_rel_type"
    UNDO = "undo"
    REDO = "redo"
    LIST_CLASS = "list_class"
    CLASS_DETAIL = "class_detail"
    CLASS_REL = "class_rel"
    SAVED_LIST = "saved_list"
    SAVE = "save"
    LOAD = "load"
    DELETE_SAVED = "delete_saved"
    CLEAR_DATA = "clear_data"
    NEW = "new"
    SORT = "sort"
    HELP = "help"
    EXIT = "exit"    
    
class RelationshipType(Enum):
    """
    Enum for specifying different types of UML relationships.
    The values represent the kind of relationship between classes in a UML diagram.
    """
    AGGREGATION = "Aggregation"
    COMPOSITION = "Composition"
    INHERITANCE = "Inheritance"
    REALIZATION = "Realization"
    
class BoxDefaultStat(Enum):
    BOX_DEFAULT_WIDTH = 170
    BOX_DEFAULT_HEIGHT = 50
    BOX_DEFAULT_X = 0
    BOX_DEFAULT_Y = 0
    BOX_DEFAULT_MARGIN = 10
    
###################################################################################################