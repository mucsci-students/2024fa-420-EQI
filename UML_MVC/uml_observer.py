class UMLObserver:
    """
    A base class for implementing the Observer in the Observer Design Pattern.
    This class defines an interface for objects that should be notified of changes
    in the UML model, such as changes to classes, fields, methods, parameters, or relationships.
    
    Methods:
        _update(event_type, data, is_loading):
            A method that will be called when the subject (UML model) changes.
            Subclasses should override this method to handle specific update behaviors.
    """

    def update(self, event_type=None, data=None, is_loading: bool = None):
        """
        A method to handle updates from the UML model. This method will be called
        whenever the model changes, such as when classes, fields, methods, or relationships
        are added, modified, or deleted.

        Args:
            event_type (str, optional): Describes the type of event that triggered the update 
                                        (e.g., 'ADD_CLASS', 'DELETE_FIELD'). 
                                        Defaults to None.
            data (dict, optional): Contains relevant data for the event (e.g., the class name, method name). 
                                   This will vary based on the event type. Defaults to None.
            is_loading (bool, optional): Indicates whether the event occurred during loading of a saved file. 
                                         True if the update is part of a loading operation, 
                                         False if it’s a regular user operation. Defaults to None.

        Subclasses should override this method to implement specific behaviors
        when the model is updated, such as updating the user interface, logging changes,
        or triggering related functionality.
        """
        pass  # Subclasses will implement the actual update handling.