import requests


data={
        "username": "user13@mail.com",
    "email": "user13@mail.com",
    "password1": "matp17954",
    "password2": "matp17954"
}

url = 'http://127.0.0.1:8000/api/rest-auth/registration/'
response = requests.post(url, json=data, headers=None)
print(response)
print(response.json())