# Custom exceptions
class MainGameExistException(Exception):
    def __init__(self, message='Main Game Exist'):
        # Call the base class constructor with the parameters it needs
        super(MainGameExistException, self).__init__(message)
