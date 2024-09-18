import unittest
import os
import subprocess
import platform
import sys

# Define the test directories and their corresponding test files
TEST_DIRECTORIES = {
    "Attribute Features": "Attribute_Features/uml_attr_test.py",
    "Class Features": "Class_Features/uml_class_test.py",
    "Relationship Features": "Relationship_Features/test_relationship.py",
    "Formatting Validators": "Formatting/test_validators.py"
}

REQUIRED_PYTHON_MAJOR = 3
REQUIRED_PYTHON_MINOR = 12

def check_python_version():
    """Checks if the Python version matches the required major and minor versions."""
    print("==========================================================================================================================================================================================")
    current_version = platform.python_version()
    major, minor, _ = map(int, current_version.split('.'))
    if major == REQUIRED_PYTHON_MAJOR and minor == REQUIRED_PYTHON_MINOR:
        print(f"Python version: {current_version}\n")
    else:
        print(f"Error: This project requires Python 3.12.*, but you're using Python {current_version}.\n")
        print("Please install the correct Python version and try again.")
        sys.exit(1)

def activate_venv():
    """Installs dependencies from requirements.txt within the virtual environment."""
    print("Activating virtual environment and installing dependencies...\n")

    # Determine the correct path to pip based on the operating system
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip.exe")
    else:
        pip_path = os.path.join("venv", "bin", "pip")

    # Ensure the pip executable exists
    if not os.path.isfile(pip_path):
        print(f"Error: pip executable not found at {pip_path}. Ensure the virtual environment is created correctly.\n")
        return

    # Run the command to install requirements
    result = subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    if result.returncode != 0:
        print("Failed to install dependencies.\n")
    else:
        print("\nDependencies installed successfully.\n")

def run_tests(test_path=None):
    """Run specified tests or all tests if no specific test is mentioned."""
    print("Running tests...\n")
    
    # Determine the correct path to the Python executable based on the operating system
    if platform.system() == "Windows":
        python_executable = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_executable = os.path.join("venv", "bin", "python3")

    # Ensure the Python executable exists
    if not os.path.isfile(python_executable):
        print(f"Error: Python executable not found at {python_executable}. Ensure the virtual environment is created correctly.\n")
        return
    
    # Run specific or all tests
    if test_path:
        suite = unittest.defaultTestLoader.loadTestsFromName(test_path.replace('/', '.').replace('.py', ''))
    else:
        suite = unittest.TestLoader().discover('UML_UNIT_TESTING', pattern='*.py')

    runner = unittest.TextTestRunner()
    runner.run(suite)

def display_test_options():
    """Displays available test files to the user."""
    print("\nAvailable Test Files:")
    for i, (key, value) in enumerate(TEST_DIRECTORIES.items(), start=1):
        print(f"{i}. {key} - ({value})")
    print("0. Run all tests")
    print("-1. Exit the test runner")

def get_user_choice():
    """Gets the user's choice for which test to run."""
    try:
        choice = int(input("\nEnter the number of the test to run, 0 to run all tests, or -1 to exit: "))
        if choice == -1:
            return "exit"  # Exit the runner
        elif choice == 0:
            return None  # Run all tests
        elif 1 <= choice <= len(TEST_DIRECTORIES):
            selected_key = list(TEST_DIRECTORIES.keys())[choice - 1]
            return TEST_DIRECTORIES[selected_key]
        else:
            print("Invalid selection. Please enter a number corresponding to the test options.")
            return get_user_choice()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_user_choice()

if __name__ == "__main__":
    check_python_version()
    activate_venv()

    while True:
        display_test_options()
        test_path = get_user_choice()
        if test_path == "exit":
            print("Exited the test runner!")
            break
        run_tests(test_path)
