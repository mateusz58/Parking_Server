import os



print(os.popen("http http://127.0.0.1:8000/api/booking/ \"Authorization: Token 14c8cbc0438111d2d7297260c46ef359dee7ee68\" ").read())
