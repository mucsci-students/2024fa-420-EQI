import readline
from UML_ENUM_CLASS.uml_enum import InterfaceOptions

def completer(text, state):
    # Get the current input from the readline buffer
    buffer = readline.get_line_buffer().strip()
    
    # Only provide command completion if we’re typing the first word
    if len(buffer.split()) == 1:
        # List of commands that start with the entered text
        options = [cmd.value for cmd in InterfaceOptions if cmd.value.startswith(text)]
    else:
        # No completion for arguments or additional words
        options = []

    # Return the state-th option from the list of matches 1
    if state < len(options):
        return options[state]
    return None

def setup_tab_completion():
    # Set the completer function for readline and bind tab completion
    readline.set_completer(completer)

    # Re-bind tab to complete in case the default binding isn't working
    readline.parse_and_bind("bind ^I rl_complete")

