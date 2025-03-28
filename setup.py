#!/usr/bin/python3

import os

def get_mysql_credentials():
    username = input("Enter MySQL username (default: root): ") or "root"
    password = input("Enter MySQL password (default: empty): ") or ""
    return username, password

def save_credentials(username, password):
    with open("db_connection.py", "w") as f:
        f.write(f"""
#!/usr/bin/python3
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='{username}',
        password='{password}',
        database='education_statistics'
    )
""")
    print("[✔] Database connection function saved in db_connection.py")

def create_database(username, password):
    print("[+] Creating database: education_statistics...")
    os.system(f"mysql -u{username} -p'{password}' -e 'CREATE DATABASE IF NOT EXISTS education_statistics;'")
    print("[✔] Database created successfully.")

def create_users_table(username, password):
    print("[+] Creating users table...")
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT NOT NULL,
        gender VARCHAR(10),
        province VARCHAR(100),
        educational_level VARCHAR(50),
        employment_status VARCHAR(50)
    );
    """
    os.system(f"mysql -u{username} -p'{password}' -D education_statistics -e \"{create_table_sql}\"")
    print("[✔] Users table created successfully.")

def insert_user_data(username, password):
    print("[+] Inserting user data from ./databases/data.sql...")
    os.system(f"mysql -u{username} -p'{password}' education_statistics < ./databases/data.sql")
    print("[✔] User data inserted successfully.")

def main():
    username, password = get_mysql_credentials()
    save_credentials(username, password)
    create_database(username, password)
    create_users_table(username, password)
    insert_user_data(username, password)
    print("[✔] All steps completed. You can now run your application.")
    print("[!] To continue, run: python your_next_script.py")

if __name__ == "__main__":
    main()
