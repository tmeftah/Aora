class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = "Incorrect username or password"
        super().__init__(self.message)


class NoValidPermissionsException(Exception):
    def __init__(self):
        self.message = "Only admin users can view all users"
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self):
        self.message = "User does not exist"
        super().__init__(self.message)


class DuplicateUserException(Exception):
    def __init__(self):
        self.message = "User with same name exists"
        super().__init__(self.message)


class NoDocumentsFoundException(Exception):
    def __init__(self):
        self.message = "No documents found in DB"
        super().__init__(self.message)
