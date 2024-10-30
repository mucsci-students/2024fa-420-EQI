from UML_INTERFACE.uml_controller_interface import UMLInterface as Interface  
from UML_MVC.UML_VIEW.UML_CLI_VIEW.uml_cli_view import UMLView as CLIView

from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_view import MainWindow as GUIView
from PyQt5.QtWidgets import QApplication
import sys
import argparse

def main():
    # # Set up argument parser to handle the --cli argument
    # parser = argparse.ArgumentParser(description="Run the UML application in GUI or CLI mode.")
    # parser.add_argument('--cli', action='store_true', help="Run the program in CLI mode")
    # args = parser.parse_args()

    # # CLI Mode
    # if args.cli:
    #     cli_view = CLIView()
    #     interface = Interface(cli_view)
    #     interface.attach_observer(cli_view)
    #     interface.main_program_loop()

    # # GUI Mode
    # else:
    #     app = QApplication(sys.argv)
    #     cli_view = CLIView()  # CLI view can still be attached if needed
    #     interface = Interface(cli_view)
        
    #     # GUI View
    #     gui_view = GUIView(interface)  # Pass the interface to the GUI view
        
    #     # Show GUI
    #     gui_view.show()
        
    #     # Start GUI event loop
    #     sys.exit(app.exec_())
    cli_view = CLIView()
    interface = Interface(cli_view)
    interface.attach_observer(cli_view)
    interface.main_program_loop()

if __name__ == "__main__":
    main()
    