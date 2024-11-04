from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from UML_ENUM_CLASS.uml_enum import InterfaceOptions

class InterfaceCompleter(Completer):
    def __init__(self):
        super().__init__()
        self.last_completion_text = None  # Track the last completion

    def get_completions(self, document, complete_event):
        # Get the text before the cursor and check for spaces
        text = document.text_before_cursor.strip()

        # Only provide completions if there's no space at all
        if " " not in document.text_before_cursor:
            # Check if the current text matches the last completion to stop further completions after a space
            if text == self.last_completion_text:
                return  # Stop further completions if last word was completed

            # Set the last completion to the current text before providing completions
            self.last_completion_text = text
            for cmd in InterfaceOptions:
                if cmd.value.startswith(text):
                    yield Completion(cmd.value, start_position=-len(text))

        else:
            # Clear the last completion when a space is detected
            self.last_completion_text = None

# Function to create the prompt session with the modified completer
def create_prompt_session():
    return PromptSession(completer=InterfaceCompleter())
