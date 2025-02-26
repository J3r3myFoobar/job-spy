import os


class Env:
    data = {}

    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        self.data = self.read_properties_file(dotenv_path)

    def read_properties_file(self, file_path):
        properties = {}
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore empty lines and comments
                    key, value = line.split("=", 1)  # Split only at the first '='
                    properties[key.strip()] = value.strip()
        return properties

    def get_key(self, key):
        return self.data[key]


if __name__ == "__main__":
    env = Env()
    print(env.get_key("OPENAI_API_KEY"))
