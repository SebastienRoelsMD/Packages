import json

def open_files_to_push():
    with open('files_to_push.json') as json_file:
        files_to_push = json.load(json_file)
    return files_to_push