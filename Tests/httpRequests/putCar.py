import requests


value='123'
auth_token='2edb54b1e8124ece31e6414e5228ee7ce512a6c2'
hed = {'Authorization': 'Token ' + auth_token}

data={
        "status":"CANCELLED"
}
base="http://127.0.0.1:8000"
end_point='/api/booking/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())


