import os



import os

import requests


user="user2@mail.com"
auth_token='47a64c5cff5735dc4d215f4c3601ea5c63446251'
hed = {'Authorization': 'Token ' + auth_token}

base="http://192.168.8.106:8000"
end_point='/api/booking/logged'
url = base+end_point
response = requests.get(url,headers=hed)
print(response)
print(response.json())

