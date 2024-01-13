import json

# Read raw.txt file
with open("raw.txt", "r") as file:
    content = file.read()

# Separate content by "---"
items = content.split("---")

# Create separate json files for each item
for i, item in enumerate(items):
    data = {"description": item.strip()}
    filename = f"data/index{i}.json"
    with open(filename, "w") as file:
        json.dumps(data, file, indent=4)
