import json
from pprint import pprint

with open('data.json') as f:
    data = json.load(f)

print(data["planetas"][1]["radio"])
