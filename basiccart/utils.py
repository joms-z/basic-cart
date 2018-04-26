import json
import collections



def to_json(value):
    return json.dumps(value)


def from_json(json_str):
    return json.loads(json_str.decode('utf-8'))

