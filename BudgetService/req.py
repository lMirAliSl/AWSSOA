import requests

BASE = "http://192.168.1.123:5002/"

response = requests.get(BASE + "calculate/1/55.5")
print(response.json())