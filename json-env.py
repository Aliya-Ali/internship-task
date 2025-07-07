import json

with open("credentials.json", "r") as f:
    data = json.load(f)

with open(".env", "w") as f:
    for key, value in data.items():
        if isinstance(value, str):
            # Escape special characters like newlines in private_key
            value = value.replace("\n", "\\n")
        f.write(f"{key.upper()}={value}\n")
