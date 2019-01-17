import os

import manage

print(os.popen("http http://127.0.0.1:8000/api/booking/ \"Authorization: Token 0b8c3f040c0703fea24743824793dacb23f0c496\" ").read())
