import os

import requests


# base="http://192.168.8.106:8000"
# # # end_point1='api/rest-auth/'
# end_point2='/api-token-auth/'
# url = base+end_point2
# #
# # TOKEN="ac0d1629c8e02089b303e1e2d87c9215cea35f74"
# #
# print(os.popen("http POST "+url+" username=user2@mail.com  password=matp17954").read())
# # # http POST  http://127.0.0.1:8000/api/rest-auth/login/ username=user3@mail.com  email="user3@mail.com" password="matp17954"
#
#


# hed={
#     "username": "user2@mail.com",
#     "email": "user2@mail.com",
#     "password": "matp17954"
# }
data={
    'username': 'user2@mail.com',
    'email': 'user2@mail.com',
    'password': "matp17954"
}
base="http://192.168.8.106:8000"
end_point='/api-token-auth/'
url = base+end_point
response = requests.post(url, json=data, headers=None)
print(response)
print(response.json())


