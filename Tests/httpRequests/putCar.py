import requests


value='123'
auth_token='f4398f50af0af87c6cf460cd354ef834517ebdd4'
hed = {'Authorization': 'Token ' + auth_token}

data={
        "status":"CANCELLED"
}
base="http://192.168.8.103:8000"
end_point='/api/booking/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())
