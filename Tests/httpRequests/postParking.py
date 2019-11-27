import requests

auth_token='7fc5f4b07051e59162494b80f94ea5ede72906ef'
hed = {'Authorization': 'Token ' + auth_token}
data={
    "parking_name": "Parking1",
    "parking_Street": "Street1",
    "parking_City": "City1",
    "x": 121.0,
    "y": 271.0,
}
url = 'http://127.0.0.1:8000/api/parking/'
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())