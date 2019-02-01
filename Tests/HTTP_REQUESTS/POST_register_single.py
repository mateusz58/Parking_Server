import requests


data={
        "username": "user2@mail1.com",
    "email": "user2@mail1.com",
    "password1": "matp17954",
    "password2": "matp17954",
}

base="http://192.168.8.106:8000"
end_point='/api/rest-auth/registration/'
url = base+end_point
response = requests.post(url, json=data, headers=None)
print(response)
print(response.json())