import requests

# Get the latest session key
url = "https://api.openf1.org/v1/sessions?session_key=latest"
response = requests.get(url).json()
print("Session:", response)

# Get live driver positions
positions = requests.get(
    "https://api.openf1.org/v1/position?session_key=latest"
).json()
print("Positions:", positions[:3])  # print first 3