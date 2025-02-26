import os


class Resume:
    as_embeddings: list[float]
    resume = ""

    def __init__(self, resume_file_path):
        self.resume = self.read_file(resume_file_path)

    def get_resume(self):
        return self.resume

    def file_exists(self, file_path):
        return os.path.exists(file_path)

    def read_file(self, filename):
        try:
            with open(filename, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return None
