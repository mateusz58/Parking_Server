import requests

user="user2@mail.com"
auth_token='f4398f50af0af87c6cf460cd354ef834517ebdd4'
hed = {'Authorization': 'Token ' + auth_token}

base="http://192.168.8.103:8000"
end_point='/api/booking/logged'
url = base+end_point
response = requests.get(url,headers=hed)
print(response)
print(response.json())

