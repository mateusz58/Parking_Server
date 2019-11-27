import sqlite3
from django.db import connection


import os.path

BASE_DIR="F:/Google drive/Projects_programming/Python/django_projects/djangox/"
db_path = os.path.join(BASE_DIR, "db.sqlite3")
with sqlite3.connect(db_path) as db:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pages_booking")
    result = cursor.fetchall()
    for p in result:
        print(p)
