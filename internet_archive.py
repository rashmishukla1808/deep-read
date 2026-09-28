import requests


identifier = "manssearchformea0000fran_l6z8"

url = f"https://archive.org/metadata/{identifier}"

response = requests.get(url)

response.raise_for_status()

data = response.json()


print("Title:")
print(data["metadata"].get("title"))

print("\nIdentifier:")
print(data["metadata"].get("identifier"))

print("\nAvailable files:\n")

for file in data.get("files", []):

    name = file.get("name")

    if name:
        print(name)
