
import requests

auth_token='6b7b8af0af5bbd3b0a59dd106faffccf2ad9f50d'
hed = {'Authorization': 'Token ' + auth_token}
user="matp321@mail.com"
Parking="Parking1"
data={
    "Date_From": "2019-01-13T16:46:19Z",
    "Date_To": "2019-01-13T16:46:20Z",
    "parking": "Parking1",
    "registration_plate": "plate1234",
    "user":"matp321@mail.com"
}
base="http://192.168.8.106:8000"
end_point='/api/booking/'
url = base+end_point
response = requests.post(url, json=data, headers=hed)
print(response)
print(response.json())

