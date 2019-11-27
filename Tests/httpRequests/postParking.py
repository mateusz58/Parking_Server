import requests

auth_token='f4398f50af0af87c6cf460cd354ef834517ebdd4'
hed = {'Authorization': 'Token ' + auth_token}
data={
    "parking_name": "Parking1",
    "parking_Street": "Street1",
    "parking_City": "City1",
    "x": 121.0,
    "y": 271.0,
}
base = "http://192.168.8.103:8000"
end_point = '/api/parking/'
response = requests.post(base+end_point, json=data, headers=hed)
print(response)
print(response.json())
