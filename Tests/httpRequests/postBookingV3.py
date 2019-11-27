import requests


value='123'
auth_token='e2dcc0104592247e950fc7c072bc60303cef4acc'
hed = {'Authorization': 'Token ' + auth_token,
        'date-from':'2019-02-18T16:46:19Z',
        "date-to": "2019-02-22T17:56:20Z",
        "registration-plate":"use68yy7gr,uzca2r345"
       }
data={
        "parking": 2,
        "user": 3,
        "number_of_cars":2
}
base="http://192.168.8.106:8000"
end_point='/api/booking/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())



