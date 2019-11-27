import requests

auth_token='f4398f50af0af87c6cf460cd354ef834517ebdd4'
hed = {'Authorization': 'Token ' + auth_token}
user="matp321@mail.com"
data={
    "new_password1": "m",
    "new_password2": "m",
    "old_password": "m"
}
base="http://192.168.8.103:8000"
end_point='/api/rest-auth/password/change/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())
