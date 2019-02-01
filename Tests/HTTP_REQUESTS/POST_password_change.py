import requests

auth_token='ad4fa74c251636021cdcd08d233b8a3b21ecc856'
hed = {'Authorization': 'Token ' + auth_token}
user="matp321@mail.com"
data={
    "new_password1": "matp1795",
    "new_password2": "matp1795",
    "old_password": "matp17954"
}
base="http://192.168.8.106:8000"
end_point='/api/rest-auth/password/change/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())



##user1- 0b8c3f040c0703fea24743824793dacb23f0c496