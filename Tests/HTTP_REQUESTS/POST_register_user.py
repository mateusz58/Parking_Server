import requests


data={
    "username": "user20@mail.com",
    "email": "user20@mail.com",
    "password1": "matp17954",
    "password2": "matp17954",
}
base="http://127.0.0.1:8000"



# end_point_standard='/api/rest-auth/registration/'
end_point_custom='/api/registration_custom/'

url = base+end_point_custom
response = requests.post(url, json=data, headers=None)
print(response)
print(response.json())