import os



import os

import requests


user="user1@mail.com"
auth_token='636f03e05a1f40c7fc9f6150d7d690c35b39a087'
hed = {'Authorization': 'Token ' + auth_token}

base="http://192.168.8.106:8000"
end_point='/api/booking/login'
url = base+end_point
response = requests.get(url,headers=hed)
print(response)
print(response.json())

