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
- [Unit Tests](#unit-tests)
- [Note](#note)

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
  git clone https://github.com/QUANGBUI24/Prototype4.git; cd Prototype4

- **macOS and Linux:**
  ```bash
  git clone https://github.com/QUANGBUI24/Prototype4.git && cd Prototype4
 
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

## Note:
- **If you want to run the program using Visual Studio Code:**
    - 1 - Open the program folder
    - 2 - Follow step 2 in the instruction on VSCode terminal
    - 3 - Follow step 3 in the instruction on VSCode terminal or 
open **build.py** file, then hit the run button