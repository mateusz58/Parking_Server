import requests
# USER   # "id": 12,

value='123'
auth_token='ac0d1629c8e02089b303e1e2d87c9215cea35f74'
hed = {'Authorization': 'Token ' + auth_token,
        'date-from':'2019-02-16T16:46:19Z',
        "date-to": "2019-02-17T17:56:20Z",
        "registration-plate":"use38yy7gr,uzcb2r345"
       }
data={
        "parking": 2,
        "user": 3,
        "number_of_cars":2
}
base="http://127.0.0.1:8000"
end_point='/api/booking/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())



##user1- 0b8c3f040c0703fea24743824793dacb23f0c496