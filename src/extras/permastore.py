import json

def save(store: dict):
    with open("store.json", "w") as file:
        file.write(json.dumps(store))

def load():
    with open("store.json", "r") as file:
        return json.loads(file.read())