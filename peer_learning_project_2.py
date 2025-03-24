#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error

class User:
    def __init__(self, name, age, gender, province, education_level, employment_status):
        self.name = name
        self.age = age
        self.gender = gender
        self.province = province
        self.education_level = education_level
        self.employment_status = employment_status

class DatabaseManager:
    def __init__(self, db_name='jason'):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Butterknife69",
                database=db_name
            )
            self.cursor = self.connection.cursor()
            self.create_table()
            print("Database connected successfully!")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
    def create_table(self):
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                gender VARCHAR(20),
                province VARCHAR(225),
                education_level VARCHAR(225),
                employment_status VARCHAR(255)
            )
            ''')
            self.connection.commit()
        except Error as e:
            print(f"Error creating table: {e}")
            
    def add_user(self, user):
        try:
            query = "INSERT INTO users (name, age, gender, province, education_level, employment_status) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (user.name, user.age, user.gender, user.province, user.education_level, user.employment_status))
            self.connection.commit()
            print(f"User {user.name} added successfully!")
        except Error as e:
            print(f"Error adding user: {e}")

    def view_by_province(self, province):
        query = "SELECT * FROM users WHERE province = %s"
        self.cursor.execute(query, (province,))
        return self.cursor.fetchall()
    
    def get_stats(self):
        query = "SELECT province, COUNT(*) FROM users GROUP BY province"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_education_stats(self):
        query = "SELECT education_level, COUNT(*) FROM users GROUP BY education_level"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_no_education_level_count(self, education_level):
        query = "SELECT COUNT(*) FROM users WHERE LOWER(education_level) != LOWER(%s)"
        self.cursor.execute(query, (education_level,))
        return self.cursor.fetchone()[0]

    def get_employment_stats_by_age(self, age_limit, employment_status):
        query = "SELECT COUNT(*) FROM users WHERE age > %s AND employment_status = %s"
        self.cursor.execute(query, (age_limit, employment_status))
        return self.cursor.fetchone()[0]

    def get_bachelors_and_unemployed_count(self):
        query = "SELECT COUNT(*) FROM users WHERE LOWER(education_level) = 'bachelors' AND LOWER(employment_status) = 'unemployed'"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def get_total_users(self):
        query = "SELECT COUNT(*) FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def close_connection(self):
        try:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("Database connection closed.")
        except Error as e:
            print(f"Error closing connection: {e}")

class App:
    def __init__(self):
        self.db = DatabaseManager()

    def show_menu(self):
        print("\n--- Education Data App ---")
        print("1. Enter User Data")
        print("2. View Data By Province")
        print("3. Show Statistics & Reports")
        print("4. Show Custom Education Statistics")
        print("5. Show Employment Statistics")
        print("6. Exit Application")

    def handle_input(self):
        while True:
            self.show_menu()
            choice = input("Choose an option:\n")
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.view_data()
            elif choice == '3':
                self.show_statistics()
            elif choice == '4':
                self.show_custom_education_statistics()
            elif choice == '5':
                self.show_employment_statistics()
            elif choice == '6':
                self.db.close_connection()
                print("Exiting...")
                exit()
            else:
                print("Invalid Input! Please try again.\n")

    def add_user(self):
        name = input("Enter name:\n")

        while True:
            try:
                age = int(input("Enter age:\n"))
                if age <= 0:
                    print("Age must be a positive integer. Try again.")
                else:
                    break
            except ValueError:
                print("Invalid Input. Please enter a number for age.")

        gender = input("Enter your gender (Male/Female/Other):\n").strip().lower()
        while gender not in ["male", "female", "other"]:
            gender = input("Invalid input. Choose Male, Female, or Other:\n").strip().lower()

        province = input("Enter Province of residence:\n").strip()

        education_level = input("Enter highest level of education (Primary, Highschool, Bachelors, Masters, PhD):\n").strip().lower()
        while education_level not in ["primary", "highschool", "bachelors", "masters", "phd"]:
            education_level = input("Invalid choice. Choose from Primary, Highschool, Bachelors, Masters, PhD:\n").strip().lower()

        employment_status = input("Enter employment status (Unemployed, Employed, Self-Employed):\n").strip().lower()
        while employment_status not in ["unemployed", "employed", "self-employed"]:
            employment_status = input("Invalid choice. Choose Unemployed, Employed, or Self-Employed:\n").strip().lower()

        new_user = User(name, age, gender, province, education_level, employment_status)
        self.db.add_user(new_user)
        print(f"Added {new_user.name} to the database.")

    def view_data(self):
        province = input("Enter the province you want to view:\n").strip()
        users = self.db.view_by_province(province)
        if users:
            for user in users:
                print(user)
        else:
            print("No data found for that province.")

    def show_statistics(self):
        stats = self.db.get_stats()
        for stat in stats:
            print(f"{stat[0]}: {stat[1]} users")

    def show_custom_education_statistics(self):
        education_level = input("Enter the education level to filter (e.g., Bachelors):\n").strip().lower()
        total_users = self.db.get_total_users()
        no_education_level_count = self.db.get_no_education_level_count(education_level)

        if total_users > 0:
            percentage_no_education_level = (no_education_level_count / total_users) * 100
            print(f"{no_education_level_count} people do not have {education_level}, which is {percentage_no_education_level:.2f}% of total users.")
        else:
            print("No users found in the database.")

    def show_employment_statistics(self):
        print("1. Show percentage of people above 30 who are employed.")
        print("2. Show percentage of people with a Bachelor's degree who are unemployed.")
        choice = input("Choose an option:\n")
        
        total_users = self.db.get_total_users()
        
        if choice == '2':
            count = self.db.get_bachelors_and_unemployed_count()
            percentage = (count / total_users) * 100 if total_users > 0 else 0
            print(f"{count} people with a Bachelor's degree are unemployed, which is {percentage:.2f}% of total users.")

if __name__ == "__main__":
    app = App()
    app.handle_input()
