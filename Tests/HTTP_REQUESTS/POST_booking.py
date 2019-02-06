import requests

auth_token='636f03e05a1f40c7fc9f6150d7d690c35b39a087'
hed = {'Authorization': 'Token ' + auth_token}
user="user1@mail.com"
data={
        "parking": 1,
        "Date_From": "2019-02-06T16:46:19Z",
        "Date_To": "2019-02-06T17:56:20Z",
        "user": 6,
        "registration_plate": "plate1234",
        "number_of_cars": 120
}
base="http://192.168.8.106:8000"
end_point='/api/booking/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())



##user1- 0b8c3f040c0703fea24743824793dacb23f0c496