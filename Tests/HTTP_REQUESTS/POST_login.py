import os

base="http://192.168.8.106:8000/"
end_point1='api/rest-auth/'
end_point2='api-token-auth/'
url = base+end_point2

print(os.popen("http POST "+url+" username=user2@mail1.com  password=matp17954").read())


# http POST  http://127.0.0.1:8000/api/rest-auth/login/ username=user3@mail.com  email="user3@mail.com" password="matp17954"

