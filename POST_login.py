import os

import manage

print(os.popen("http POST  http://127.0.0.1:8000/api/rest-auth/login/ username=user12@mail.com  email=user12@mail.com password=matp17954").read())


# http POST  http://127.0.0.1:8000/api/rest-auth/login/ username=user3@mail.com  email="user3@mail.com" password="matp17954"

