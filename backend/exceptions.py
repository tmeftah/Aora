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


class ModelsNotRetrievedException(Exception):
    def __init__(self):
        self.message = "No Ollama Models found"
        super().__init__(self.message)


class NoTopicFoundException(Exception):
    def __init__(self):
        self.message = "No Topic found"
        super().__init__(self.message)


class DuplicateTopicException(Exception):
    def __init__(self):
        self.message = "Topic with same name exists"
        super().__init__(self.message)
