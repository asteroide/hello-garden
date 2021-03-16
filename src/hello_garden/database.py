import json
import yaml


def save(filename, data):
    if filename.endswith("json"):
        return save_json(filename, data)
    elif filename.endswith("yaml"):
        return save_yaml(filename, data)
    else:
        raise Exception(f"Cannot find the file type ({filename})")


def save_json(filename, data):
    print(f"saving to json {filename}")
    open(filename, "w").write(json.dumps(data))


def save_yaml(filename, data):
    print(f"saving to yaml {filename}")
    with open(filename, "w") as file:
        yaml.dump(data, file)
