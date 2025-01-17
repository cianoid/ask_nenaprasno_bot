class EnvVariablesError(Exception):
    """Exception class for errors caused by type conversion of environment variables."""

    def __init__(self, setting, message="The value of setting is not converted to the expected type."):
        self.setting = setting
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.setting} -> {self.message}"
