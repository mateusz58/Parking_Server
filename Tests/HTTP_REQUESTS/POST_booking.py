import requests

auth_token='4fb390b82071a40eff6719e7b0d84d72c600ab0f'
hed = {'Authorization': 'Token ' + auth_token}
user="matp321@mail.com"
data={
    "parking": 2,
    "Date_From": "2019-01-10 16:46:19",
    "Date_To": "2019-01-25 16:46:20",
    "registration_plate": "plate1234",
    "user":5
}
base="http://192.168.8.106:8000"
end_point='/api/booking/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())



##user1- 0b8c3f040c0703fea24743824793dacb23f0c496