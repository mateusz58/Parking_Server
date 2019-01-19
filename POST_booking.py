import requests

auth_token='0b8c3f040c0703fea24743824793dacb23f0c496'
hed = {'Authorization': 'Token ' + auth_token}
data={
    "Date_From": "2019-01-13T16:46:19Z",
    "Date_To": "2019-01-13T16:46:20Z",
    "parking": 1,
    "registration_plate": "plate1234",
    "user": '3'
}

url = 'http://127.0.0.1:8000/api/booking/'
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())



##user1- 0b8c3f040c0703fea24743824793dacb23f0c496