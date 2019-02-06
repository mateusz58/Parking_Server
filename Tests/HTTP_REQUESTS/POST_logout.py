import requests
user="user1@mail.com"
auth_token='a45217fc6005f8e0d5b56d0fe09374240bbc9d45'
hed = {'Authorization': 'Token ' + auth_token}


base="http://192.168.8.106:8000"
end_point='/api/rest-auth/logout/'
url = base+end_point
response = requests.post(url,headers=hed)
print(response)
print(response.json())