import requests

auth_token='7fc5f4b07051e59162494b80f94ea5ede72906ef'
hed = {'Authorization': 'Token ' + auth_token}
data={
    "parking_name": "Parking13",
    "parking_Street": "Street12",
    "parking_City": "City12",
    "x": 120.0,
    "y": 270.0,
}
url = 'http://127.0.0.1:8000/api/parking/'
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())