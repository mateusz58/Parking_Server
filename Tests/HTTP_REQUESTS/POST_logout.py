import requests
user="user1@mail.com"
auth_token='ac0d1629c8e02089b303e1e2d87c9215cea35f74'
hed = {'Authorization': 'Token ' + auth_token}


base="http://127.0.0.1:8000"
end_point='/api/rest-auth/logout/'
url = base+end_point
response = requests.post(url,headers=hed)
print(response)
print(response.json())