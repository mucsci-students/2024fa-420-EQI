import os
import platform
import subprocess
import sys
import argparse

REQUIRED_PYTHON_MAJOR = 3
REQUIRED_PYTHON_MINOR = 12


def check_python_version():
    """Checks if the Python version matches the required major and minor versions."""
    print(
        "=========================================================================================================================================================================================="
    )
    current_version = platform.python_version()
    major, minor, _ = map(int, current_version.split("."))
    if major == REQUIRED_PYTHON_MAJOR and minor == REQUIRED_PYTHON_MINOR:
        print(f"Python version: {current_version}\n")
    else:
        print(
            f"Error: This project requires Python 3.12.*, but you're using Python {current_version}.\n"
        )
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
        print(
            f"Error: pip executable not found at {pip_path}. Ensure the virtual environment is created correctly.\n"
        )
        return

    # Run the command to install requirements
    result = subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    if result.returncode != 0:
        print("Failed to install dependencies.\n")
    else:
        print("\nDependencies installed successfully.\n")


def run_program(cli_mode=False):
    """Runs the main program using the virtual environment's Python."""
    print("Running main.py...\n")

    # Determine the correct path to the Python executable based on the operating system
    if platform.system() == "Windows":
        python_executable = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_executable = os.path.join("venv", "bin", "python3")

    # Ensure the Python executable exists
    if not os.path.isfile(python_executable):
        print(
            f"Error: Python executable not found at {python_executable}. Ensure the virtual environment is created correctly.\n"
        )
        return

    print(f"Using Python executable at: {python_executable}\n")
    print("Program beginning...\n")
    print(
        "==========================================================================================================================================================================================\n"
    )

    # Build the command to run the program
    command = [python_executable, "main.py"]
    
    # Add the --cli argument if cli_mode is True
    if cli_mode:
        command.append("--cli")

    result = subprocess.run(command)
    if result.returncode != 0:
        print("\nFailed to run the program.")
    else:
        print("\nProgram ran successfully.")


if __name__ == "__main__":
    # Set up argument parser to handle the --cli argument
    parser = argparse.ArgumentParser(description="Build and run the UML application.")
    parser.add_argument('--cli', action='store_true', help="Run the program in CLI mode")
    args = parser.parse_args()

    check_python_version()
    activate_venv()

    # Pass the --cli argument to the main program if provided
    run_program(cli_mode=args.cli)
