import json
import os.path


class JsonManager:
    def __init__(self, filename):
        try:
            filer = open(filename + ".json", "r")
        except EnvironmentError:
            print("Erro ao abrir contador para leitura.")
            return False

        self.data = {}
        try:
            if filer:
                self.data = json.load(filer)
                filer.close()
        except json.JSONDecodeError as e:
            print("JSON parse error: " + e.msg)
            return False

        self.file = None

        try:
            self.file = open(filename + ".json", "w")
        except EnvironmentError:
            print("Erro ao abrir contador para escrita.")
            return False
        

    def get(self, key):
        if key in self.data:
            return self.data[key]
        else:
            print("Chave não está no contador.")
            return None

    def set(self, key, value):
        self.data[key] = value

        try:
            json.dump(self.data, self.file)
            self.file.flush()
            return True
        except TypeError:
            print("Error saving to file.")
            return False