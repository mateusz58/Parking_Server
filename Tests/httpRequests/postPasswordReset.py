

import requests

data={
    "email": "matp321@mail.com",
}
base="http://192.168.8.106:8000"
end_point='/api/rest-auth/password/reset/'
url = base+end_point
response = requests.post(url, json=data, headers=None)
print(response)
print(response.json())



