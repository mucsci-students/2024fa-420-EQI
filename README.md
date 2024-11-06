# 2024fa-420-EQI

A project developed by team EQI for the 2024 Fall semester course.

## Team

### EQI

**Team Members:**
- **Emily Riley ([GitHub Profile](https://github.com/emilyyr55))** - Developer
- **Quang Bui ([GitHub Profile](https://github.com/QUANGBUI24))** - Developer
- **Israel Gonzalez ([GitHub Profile](https://github.com/xhatd))** - Developer

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Instructions](#instructions)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Set Up a Virtual Environment](#step-2-set-up-a-virtual-environment)
  - [Step 3: Run the Build Script](#step-3-run-the-build-script)
- [Running Tests](#running-tests)
- [Design Pattern Implementation](#design-patterns)

## Introduction

This project is a collaborative effort developed by Team EQI for the Fall 2024 semester as part of the CSCI 420 course. The primary focus of the course is to encourage collaboration, teamwork, and the principles of software development in a group setting. Throughout the semester, the team will work together to design, build, and refine a functional software program.

Our project aims to showcase the collective skills of the team by integrating individual contributions into a cohesive system. By leveraging version control, effective communication, and shared responsibility, this project emphasizes the importance of collaboration in modern software development. The program's final product will demonstrate core programming concepts while fostering an environment of continuous learning and teamwork.
## Requirements

- **Python version**: To ensure compatibility, the Python version must be **3.12.x** (where 'x' can be any sub-version). You can download and install the latest version of Python 3.12 from the official website here [Download Python 3.12](https://www.python.org/downloads/). 

- **pip**: Ensure that `pip` is installed, as it is required to create the virtual environment and install dependencies. If `pip` is not installed, follow the instructions on how to install it [here](https://pip.pypa.io/en/stable/installation/).

Please make sure to update your environment accordingly.

## Instructions

Follow these steps to set up and run the project on your local machine:

### Step 1: Clone the Repository

Clone the project repository from GitHub to your local machine using the appropriate command for your operating system:

- **Windows (Powershell):**    
  ```bash
  git clone https://github.com/mucsci-students/2024fa-420-EQI.git; cd 2024fa-420-EQI

- **macOS and Linux:**
  ```bash
  git clone https://github.com/mucsci-students/2024fa-420-EQI.git && cd 2024fa-420-EQI
 
### Step 2: Set Up a Virtual Environment

- **Then create the virtual environment by typing the commands below:**

- **Windows (Powershell):**  
  ```bash
  python -m venv venv

- **macOS and Linux:** 
  ```bash
  python3 -m venv venv

### Step 3: Run the Build Script**
- **To run GUI**
- **Windows (Powershell):**  
  ```bash
  python build.py

- **macOS and Linux:** 
  ```bash
  python3 build.py

- **To run CLI**
- **Windows (Powershell):**  
  ```bash
  python build.py --cli

- **macOS and Linux:** 
  ```bash
  python3 build.py --cli

## Running Tests

To run all tests and generate a coverage report in XML format, use the following command:

  #### Note: If you haven't run build.py, ensure that dependencies like pytest and coverage are installed by running:

    pip install -r requirements.txt

Then, to execute tests and create a coverage report:

1. Run tests and create a coverage report:
  
        python run_tests.py

## Design Patterns

This project utilizes several design patterns to promote efficient, maintainable, and scalable code. Below is an outline of the main patterns implemented:

### 1. Model-View-Controller (MVC) Pattern
- **Purpose**: Separates the application into three interconnected components, allowing for modularity and separation of concerns.

- **Components**:
  - Model: Handles core data structures and business logic, including class and relationship management.
  - View: Manages user interface elements and displays data to the user. Both GUI and CLI views are provided.
  - Controller: Acts as an intermediary between Model and View, processing input and updating the Model and View accordingly.

### 2. Observer Pattern
- **Purpose**: Implements a publish-subscribe model where observers are notified of changes in the subject they are observing. This allows for automatic updates across components.

- **Components**:
  - Observable (Subject): UMLModel — Notifies observers when changes are made to the model.
  - Observers: Defined in uml_observer.py located at **2024fa-420-EQI/UML_MVC/uml_observer.py** .Various classes subscribe to UMLModel to respond to updates, ensuring synchronized changes.

### 3. Command Pattern
- **Purpose**: Provides a way to encapsulate actions (commands) as objects, allowing for operations such as undo and redo. This design pattern is especially useful for maintaining an action history.

- **Components**:

    - **Invoker**: Manages executing commands and handling the history stack for undo/redo.
    - **Command Interface**: Each action (like adding, deleting, or modifying elements) implements this interface, making these operations reversible.
    - **Concrete Commands**: Specific command objects for each action, holding the necessary data for undoing and redoing operations.

  - Location in Code: The Command Pattern for undo and redo is implemented within **2024fa-420-EQI/UML_MVC/uml_command_pattern.py**

### 4. Singleton
- **Purpose**: Ensures a class has only one instance and provides a global point of access to that instance

- **Components**:

    - **MainWindow**: The MainWindow class uses the Singleton pattern to limit the application to a single main window instance. This centralizes all GUI interactions, preventing multiple conflicting windows and ensuring unified control over the interface.

- **Implementation**:

    - **Private Instance Variable**: _instance holds the single instance of MainWindow.
    - **Custom __new__ Method**: Overrides the default constructor to check if _instance is None before creating a new instance, raising an error if a second instance is attempted.
    - path: 2024FA-420-EQI/UML_MVC/UML_VIEW/uml_gui_view.py