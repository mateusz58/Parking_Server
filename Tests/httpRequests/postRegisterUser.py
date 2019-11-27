import requests


data={
    "username": "user2@mail.com",
    "email": "user2@mail.com",
    "password1": "matp1794",
    "password2": "matp17954",
}
base="http://192.168.8.106:8000"




end_point_custom='/api/registration_custom/'

url = base+end_point_custom
response = requests.post(url, json=data, headers=None)
print(response)
print(response.json())