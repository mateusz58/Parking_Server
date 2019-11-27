import os

base="http://127.0.0.1:8000/"

end_point='api-token-auth/'
url = base+end_point

TOKEN="ac0d1629c8e02089b303e1e2d87c9215cea35f74"

print(os.popen("http POST "+url+" username=user2@mail.com  password=matp17954").read())
