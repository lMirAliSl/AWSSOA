import requests

BASE = "http://127.0.0.1:5001/"

data = {"email" : "lol1@gmail.com", "password" : "1322", "name" : "Lol2"}

data1 = {"email" : "lol2@gmail.com", "password" : "1322", "name" : "Lol2"}

data2 = {"email" : "lol3@gmail.com", "password" : "1322", "name" : "Lol2"}

# Запит на створення користувача
response = requests.put(BASE + "userDB/0", json = data)
print(response.json())

# Запит на отримання користувача
response = requests.get(BASE + "userDB/1")
print(response.json())
