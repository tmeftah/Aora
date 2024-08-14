class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = "Incorrect username or password"
        super().__init__(self.message)


class NoValidPermissionsException(Exception):
    def __init__(self):
        self.message = "Only admin users can view all users"
        super().__init__(self.message)
