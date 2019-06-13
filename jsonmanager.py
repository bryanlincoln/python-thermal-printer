import json
import os.path


class JsonManager:
    def __init__(self, filename):
        try:
            filer = open(filename + ".json", "r")
        except EnvironmentError:
            print("Erro ao abrir contador para leitura.")
            return

        self.data = {}
        try:
            if filer:
                self.data = json.load(filer)
                filer.close()
        except json.JSONDecodeError as e:
            print("JSON parse error: " + e.msg)
            return

        self.filename = filename
        
    def get(self, key):
        if key in self.data:
            return self.data[key]
        else:
            print("Chave não está no contador.")
            return None

    def set(self, key, value):
        self.data[key] = value

        try:
            file = open(self.filename + ".json", "w")
        except EnvironmentError:
            print("Erro ao abrir contador para escrita.")
            return False

        try:
            json.dump(self.data, file)
            file.close()
            return True
        except TypeError:
            print("Error saving to file.")
            return False