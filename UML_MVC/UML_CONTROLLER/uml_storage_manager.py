###################################################################################################

# IMPORTED MODULES #
import json
import os
from typing import List, Dict

###################################################################################################

class UMLStorageManager:
    
    """
    A class to manage the storage of UML data by saving, loading, and updating JSON files.
    It handles the management of saved UML diagram files and their associated metadata.
    """

    # This function loads the saved file name list at the beginning of the program #
    @staticmethod
    def load_name():
        """
        Load the list of saved file names from 'NAME_LIST.json' at the start of the program.
        
        Returns:
            list: A list of dictionaries containing saved file names and their status ('on'/'off').
            None: If there is a file not found error or JSON decoding error.
        """
        file_path = "UML_UTILITY/SAVED_FILES/NAME_LIST.json"
        try:
            # Check if the file is empty
            if os.stat(file_path).st_size == 0:
                return []
            # Load data from the JSON file
            with open(file_path, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            # Handle the case where the file is not found
            print(f"\nFile {file_path} not found.")
            return None
        except json.JSONDecodeError:
            # Handle JSON decoding errors (e.g., if the file is not in proper JSON format)
            print(f"\nError decoding JSON from {file_path}.")
            return None
        
    #################################################################
    
    # UML storage manager constructor #
    def __init__(self):
        """
        Initializes the UMLStorageManager by loading the saved file name list into memory.
        """
        self.__saved_file_name_list: List[Dict] = self.load_name()
        
    # Getter to retrieve the list of saved file names #
    def _get_saved_list(self) -> List[Dict]:
        """
        Retrieve the current list of saved file names and their statuses ('on'/'off').

        Returns:
            List[Dict]: A list of dictionaries with file names and their statuses.
        """
        return self.__saved_file_name_list
        
    #################################################################
    ### MEMBER FUNCTIONS ###
    
    ## SAVE/LOAD RELATED ##
    
    # Save the current UML data to a JSON file #
    def _save_data_to_json(self, file_name: str, main_data: Dict):
        """
        Save the current UML data (main_data) to a specified JSON file.

        Args:
            file_name (str): The name of the file to save.
            main_data (Dict): The UML data to be saved in JSON format.

        Returns:
            None
        """
        file_path = f"UML_UTILITY/SAVED_FILES/{file_name}.json"
        try:
            # If the file does not exist, create and write the data
            if not os.path.exists(file_path):
                with open(file_path, "w") as json_file:
                    json.dump(main_data, json_file, indent=4)
                    return
            # If file exists, update its data if the file name is in the saved list
            for dictionary in self.__saved_file_name_list:
                if file_name in dictionary:
                    # Open the file and overwrite the current data with the new data
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        data = main_data  # Overwrite with new data
                    with open(file_path, "w") as json_file:
                        json.dump(data, json_file, indent=4)
        except json.JSONDecodeError:
            # Handle JSON decoding errors
            print(f"\nError decoding JSON from {file_path}.")
            return None
    
    # Save data specifically for GUI-based interactions #
    def _save_data_to_json_gui(self, file_name: str, file_path: str, main_data: Dict):
        """
        Save the UML data (main_data) to a specified file path for GUI operations.

        Args:
            file_name (str): The name of the file to save.
            file_path (str): The file path where the data will be saved.
            main_data (Dict): The UML data to be saved in JSON format.

        Returns:
            None
        """
        try:
            # If the file does not exist, create and write the data
            if not os.path.exists(file_path):
                with open(file_path, "w") as json_file:
                    json.dump(main_data, json_file, indent=4)
                    return
            # If file exists, update its data if the file name is in the saved list
            for dictionary in self.__saved_file_name_list:
                if file_name in dictionary:
                    # Open the file and overwrite the current data with the new data
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        data = main_data  # Overwrite with new data
                    with open(file_path, "w") as json_file:
                        json.dump(data, json_file, indent=4)
        except json.JSONDecodeError:
            # Handle JSON decoding errors
            print(f"\nError decoding JSON from {file_path}.")
            return None
        
    # Load UML data from a specified JSON file #
    def _load_data_from_json(self, file_name: str):
        """
        Load UML data from a specified JSON file.

        Args:
            file_name (str): The name of the file to load data from.

        Returns:
            dict: The UML data loaded from the JSON file.
            None: If there is a file not found error or JSON decoding error.
        """
        file_path = f"UML_UTILITY/SAVED_FILES/{file_name}.json"
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            # Handle the case where the file is not found
            print(f"File {file_path} not found.")
            return None
        except json.JSONDecodeError:
            # Handle JSON decoding errors
            print(f"\nError decoding JSON from {file_path}.")
            return None
        
    # Add a new file name to the saved file list #
    def _add_name_to_saved_file(self, file_name: str):
        """
        Add a new file name to the saved file name list and store it in 'NAME_LIST.json'.

        Args:
            file_name (str): The name of the file to be added to the saved list.

        Returns:
            None
        """
        file_path = "UML_UTILITY/SAVED_FILES/NAME_LIST.json"
        saved_list = self.__saved_file_name_list
        # Avoid duplicate file names
        for pair in saved_list:
            if file_name in pair:
                return
        saved_list.append({file_name: "off"})
        try:
            # Write the updated saved list to the file
            with open(file_path, "w") as file:
                json.dump(saved_list, file, indent=4)
        except FileNotFoundError:
            print(f"\nFile {file_path} not found.")
            return None
        except json.JSONDecodeError:
            print(f"\nError decoding JSON from {file_path}.")
            return None
        
    # Update the saved file list with new information #
    def _update_saved_list(self, saved_list: List[Dict]):
        """
        Update the saved file name list and store it in 'NAME_LIST.json'.

        Args:
            saved_list (List[Dict]): The updated list of saved files.

        Returns:
            None
        """
        file_path = "UML_UTILITY/SAVED_FILES/NAME_LIST.json"
        try:
            # Write the updated saved list to the file
            with open(file_path, "w") as file:
                json.dump(saved_list, file, indent=4)
        except FileNotFoundError:
            print(f"\nFile {file_path} not found.")
            return None
        except json.JSONDecodeError:
            print(f"\nError decoding JSON from {file_path}.")
            return None

###################################################################################################