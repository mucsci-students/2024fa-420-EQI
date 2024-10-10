from UML_INTERFACE.uml_controller_interface import UMLInterface as Interface  
from UML_MVC.UML_VIEW.UML_CLI_VIEW.uml_cli_view import UMLView as CLIView

def main():
    # Console View
    cli_view = CLIView()
    interface = Interface(cli_view)
    interface.attach_observer(cli_view)
    interface.main_program_loop()
    
if __name__ == "__main__":
    main()