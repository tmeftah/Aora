class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = "Incorrect username or password"
        super().__init__(self.message)
