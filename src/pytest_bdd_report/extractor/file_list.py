class FileListRepo:
    def __init__(self):
        self.files: list[str] = []

    def add(self, filename: str) -> None:
        if not filename:
            return
        if filename in self.files:
            return

        self.files.append(filename)

    def get(self) -> list[str]:
        return self.files
