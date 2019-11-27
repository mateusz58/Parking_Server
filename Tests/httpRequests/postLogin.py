import requests

data={
    'username': 'user2@mail.com',
    'email': 'user2@mail.com',
    'password': "password"
}
base="http://192.168.8.103:8000"
end_point='/api-token-auth/'
url = base+end_point
response = requests.post(url, json=data, headers=None)
print(response)
print(response.json())
