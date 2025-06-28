import json,pickle

# Handles loading and unloading of .sav and .json files
def loadFile(path,tag):
    """Loads specified file"""
    with open(path,tag) as file:
        if path.endswith(".json"):
            return json.load(file)
        elif path.endswith(".sav"):
            return pickle.load(file)

def dumpFile(path,data,tag):
    """"Dumps data into specified file"""
    with open(path,tag) as file:
        if path.endswith(".json"):
            json.dump(data,file,indent=4)
        elif path.endswith(".sav"):
            pickle.dump(data,file)

