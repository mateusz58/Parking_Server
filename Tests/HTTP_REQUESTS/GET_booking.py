import os



import os



base="http://192.168.8.106:8000"
Token="14c8cbc0438111d2d7297260c46ef359dee7ee68"
endpoint="/api/booking/"

print(os.popen("http "+base+endpoint+" \"Authorization: Token "+Token+"\" ").read())
