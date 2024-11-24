from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from UML_ENUM_CLASS.uml_enum import InterfaceOptions
from UML_ENUM_CLASS.uml_enum import RequireClassFirstInput, RequireSecondInput, RequireClassSecondInput, RequireFieldSecondInput, RequireMethodNumSecondInput, RequireParamThirdInput, RequireRelTypeThirdInput, RelationshipType
from UML_MVC.UML_MODEL.uml_model import UMLModel as Model


class InterfaceCompleter(Completer):
    def __init__(self, model):
        super().__init__()
        self.last_completion_text = None  # Track the last completion
        self.Model = model

    def get_completions(self, document, complete_event):
        # Get the text before the cursor
        text = document.text_before_cursor.strip()
        
        # Split the text into words to determine the context for completion
        words = text.split()

        # print("self", self)

        # First-level completion (InterfaceOptions)
        if len(words) == 1:
            # Only complete if no space or just the first word is being typed
            if " " not in document.text_before_cursor or words[0] != self.last_completion_text:
                self.last_completion_text = words[0]
                for cmd in InterfaceOptions:
                    if cmd.value.startswith(words[0]):
                        yield Completion(cmd.value, start_position=-len(words[0]))

        # Second-level completion based on class completion
        elif len(words) == 2:
            # Only try to complete on commands that require an input that is an existing class
            if (words[0] in RequireClassFirstInput):
                # Get the current classes
                main_data = self.Model._get_main_data()
                fullClasses = main_data["classes"]
                classes = []
                # Get a list of just the class names
                for cls in fullClasses:
                    classes.append(cls["name"])
                
                # Second-level completion
                if " " not in document.text_before_cursor or words[1] != self.last_completion_text:
                    self.last_completion_text = words[1]
                    # Only complete for the classes that exist
                    for option in classes:
                        if option.startswith(words[1]):
                            yield Completion(option, start_position=-len(words[1]))
        
        # Third-level of completion based on second parameter
        # Which could be method number, field name or class name
        elif len(words) == 3:
            # Only complete if the command requires a second input
            if (words[0] in RequireSecondInput):
                # Get class and list of just class names
                currentClassName = words[1]
                main_data = self.Model._get_main_data()
                fullClasses = main_data["classes"]
                currentFullClass = {}
                classes = []
                for cls in fullClasses:
                    classes.append(cls["name"])
                    if cls["name"] == currentClassName:
                        currentFullClass = cls

                validSecondInput = []
                # Only try to complete if the class name does exist
                if currentFullClass != {}:
                    # Get the correct possible numbers for the specific class 
                    # Example: if there are 3 methods for class "Car", then the possible method numbers are ["1", "2", "3"]
                    if (words[0] in RequireMethodNumSecondInput):
                        methodList = currentFullClass["methods"]
                        validSecondInput = []
                        i = 1
                        for method in methodList:
                            validSecondInput.append(f"{i}")
                            i = i + 1

                    # Get the possible field names for the specific class
                    if  (words[0] in RequireFieldSecondInput):
                        fieldList = currentFullClass["fields"]
                        validSecondInput = []
                        for field in fieldList:
                            validSecondInput.append(field["name"])

                    # Set the class names to be the second input wanted
                    if (words[0] in RequireClassSecondInput):
                        validSecondInput = classes
                    
                    # Third level of completion
                    if " " not in document.text_before_cursor or words[2] != self.last_completion_text:
                        self.last_completion_text = words[2]
                        # Only complete for the specific valid input based on the above steps
                        for option in validSecondInput:
                            if option.startswith(words[2]):
                                yield Completion(option, start_position=-len(words[2]))
        
        # Fourth level of completion
        # For parameter name or relationship type
        elif len(words) == 4:
            # Only complete for commands that require a 3rd input
            if (words[0] in RequireParamThirdInput or words[0] in RequireRelTypeThirdInput):
                # Get the current class and current method based on the class and number given
                # Will be empty if there is no class with the inputted name or method with the inputted value
                currentClassName = words[1]
                currentMethodNum = words[2]
                main_data = self.Model._get_main_data()
                fullClasses = main_data["classes"]
                currentFullClass = {}
                currentFullMethod = {}
                for cls in fullClasses:
                    if cls["name"] == currentClassName:
                        currentFullClass = cls
                if currentFullClass != {}:
                    methodList = currentFullClass["methods"]
                    # Check to see if the method number inputted is numeric, if it is not the method will be empty
                    if currentMethodNum.isnumeric():
                        currentMethodNum = int(currentMethodNum)
                        i = 1
                        for method in methodList:
                            if i == currentMethodNum:
                                currentFullMethod = method
                            i = i + 1
                validThirdInput = []
                
                # Check to see if the method exists and the command requires a parameter name as the next input
                if (words[0] in RequireParamThirdInput and currentFullMethod != {}):
                    params = currentFullMethod["params"]
                    validThirdInput = []
                    # Get list of parameters in the method
                    for param in params:
                        validThirdInput.append(param["name"])

                # Check to see if the class exists and the command requires a relationship type
                if  (words[0] in RequireRelTypeThirdInput and currentFullClass != []):
                    validThirdInput = {"Aggregation", "Composition", "Inheritance", "Realization"}
                
                # Fourth level of completion
                if " " not in document.text_before_cursor or words[3] != self.last_completion_text:
                    self.last_completion_text = words[3]
                     # Only complete for the specific valid input based on the above steps
                    if validThirdInput:
                        for option in validThirdInput:
                            if option.startswith(words[3]):
                                yield Completion(option, start_position=-len(words[3]))
        
        else:
            # Clear the last completion when no match is found
            self.last_completion_text = None


# Function to create the prompt session with the modified completer
def create_prompt_session(model):
    return PromptSession(completer=InterfaceCompleter(model))

