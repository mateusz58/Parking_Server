import requests

auth_token='e2dcc0104592247e950fc7c072bc60303cef4acc'
hed = {'Authorization': 'Token ' + auth_token}
user="matp321@mail.com"
data={
    "new_password1": "m",
    "new_password2": "m",
    "old_password": "m"
}
base="http://192.168.8.106:8000"
end_point='/api/rest-auth/password/change/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())



##user1- 0b8c3f040c0703fea24743824793dacb23f0c496