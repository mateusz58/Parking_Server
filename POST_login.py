import os

import manage

print(os.popen("http POST  http://127.0.0.1:8000/api-token-auth/ username=matp321@gmail.com  email=matp321@gmail.com password=matp17954").read())


# http POST  http://127.0.0.1:8000/api/rest-auth/login/ username=user3@mail.com  email="user3@mail.com" password="matp17954"

