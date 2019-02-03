

import os



base="http://192.168.8.106:8000"
Token="14c8cbc0438111d2d7297260c46ef359dee7ee68"

print(os.popen("http "+base+"/api/parking/ \"Authorization: Token "+Token+"\" ").read())