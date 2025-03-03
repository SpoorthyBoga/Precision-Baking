import requests

url = "http://127.0.0.1:5000/search_recipes"
payload = {"ingredients": ["flour", "sugar"]}

response = requests.post(url, json=payload)
if response.status_code == 200:
    print("Recipe Search Response:", response.json())
else:
    print("Error:", response.text)
