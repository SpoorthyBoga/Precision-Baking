import requests

# Endpoint URL
url = "http://127.0.0.1:5000/detect"

# Path to the image file
file_path = "C:/Users/Cherry/Downloads/Untitled.jpg"

# Sending the POST request
with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": file})

# Print the response
print("Ingredient Detection Response:", response.json())
