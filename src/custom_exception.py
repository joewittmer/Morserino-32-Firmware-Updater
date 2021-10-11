# https://stackoverflow.com/questions/49224770/default-message-in-custom-exception-python


class CustomException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = "This is a default message!"

        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else:  # else, the exception was raised without arguments ...
            # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)
