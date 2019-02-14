import requests
# USER   # "id": 12,

value='123'
auth_token='2edb54b1e8124ece31e6414e5228ee7ce512a6c2'
hed = {'Authorization': 'Token ' + auth_token,
        'date-from':'2019-02-16T16:46:19Z',
        "date-to": "2019-02-17T17:56:20Z",
        "registration-plate":"use38yy7gr,uzcb2r345"
       }
data={
        "parking": 4,
        "user": 2,
        "number_of_cars":2
}
base="http://127.0.0.1:8000"
end_point='/api/booking/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())



##user1- 0b8c3f040c0703fea24743824793dacb23f0c496