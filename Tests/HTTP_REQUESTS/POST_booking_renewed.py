import requests
# USER   # "id": 12,

value='123'
auth_token='75a6a637908febb8ecf42b4e2f547a4481fb55e4'
hed = {'Authorization': 'Token ' + auth_token,
        'date-from':'2019-02-18T16:46:19Z',
        "date-to": "2019-02-20T17:56:20Z",
        "registration-plate":"userplate9,userplate7"
       }
data={
        "parking": 1,
        "Date_From": "2019-02-18T16:46:19Z",
        "Date_To": "2019-02-20T17:56:20Z",
        "user": 12,
        "registration_plate": "userplate5",
        "number_of_cars":5
}
base="http://192.168.8.106:8000"
end_point='/api/booking/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())



##user1- 0b8c3f040c0703fea24743824793dacb23f0c496