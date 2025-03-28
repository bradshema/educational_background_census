
#!/usr/bin/python3
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='education_statistics'
    )
