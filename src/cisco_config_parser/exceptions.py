class FileReadError(Exception):
    """Error, Wrong File Extension, make sure the file is txt file"""

    def __init__(self, file, message="Error, Wrong File Extension, make sure the file is .txt file"):
        self.file = file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.file} -> {self.message}'