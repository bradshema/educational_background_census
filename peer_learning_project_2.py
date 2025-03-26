#!/usr/bin/python3

# NOTE: This is to import the database.
import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

# INFO: Creating user class and attributes.  
class User:
    def __init__(self, name, age, gender, province, educational_level):
        self.name = name
        self.age = age
        self.gender = gender
        self.province = province
        self.educational_level = educational_level

# INFO: Creating a data management class.
class DatabaseManager:
    def __init__(self, db_name='jason'):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
<<<<<<< HEAD
                user='root',  
                password='Butterknife69',  
                database=db_name 
=======
                user='root',
                password='',
                database=db_name
>>>>>>> 32873cd0f04d53e6dfc569c4d1dd14df20a8764b
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                self.create_table()
                print('Database connected successfully!')
            else:
                print('Failed to connect to the database.')
        except Error as e:
            print(f'Error connecting to MySQL: {e}')

    def create_table(self): # NOTE: This will create a database if it isn't created.
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    age INT,
                    gender VARCHAR(20),
                    province VARCHAR(255),
                    educational_level VARCHAR(255)
                )
            ''')
            self.connection.commit()
        except Error as e:
            print(f'Error creating table: {e}')

    def add_user(self, user): # INFO: This function is for user creation.
        try:
            query = '''
                INSERT INTO users (name, age, gender, province, educational_level) 
                VALUES (%s, %s, %s, %s, %s)
            '''
            self.cursor.execute(query, (user.name, user.age, user.gender, user.province, user.educational_level))
            self.connection.commit()
            print(f'User {user.name} added successfully!')
        except Error as e:
            print(f'Error adding user: {e}')

    def get_stats(self): # NOTE: GETTING STATS.
        try:
            query = 'SELECT province, COUNT(*) FROM users GROUP BY province'
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f'Error retrieving statistics: {e}')
            return []

    def view_by_province(self, province): #  INFO: This will allow the user to view stats by province.
        try:
            query = 'SELECT * FROM users WHERE province = %s'
            self.cursor.execute(query, (province,))
            return self.cursor.fetchall()
        except Error as e:
            print(f'Error retrieving data: {e}')
            return []

    def get_education_stats(self, province):
        try:
            query = '''
                SELECT 
                    SUM(CASE WHEN educational_level IN ('bachelors', 'masters', 'phd') THEN 1 ELSE 0 END) AS educated,
                    SUM(CASE WHEN educational_level IN ('primary', 'highschool') THEN 1 ELSE 0 END) AS uneducated
                FROM users WHERE province = %s
            '''
            self.cursor.execute(query, (province,))
            return self.cursor.fetchone()
        except Error as e:
            print(f'Error retrieving custom statistics: {e}')
            return (0, 0)

    def close_connection(self): # INFO: Will end the connection to the database.
        try:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print('Database connection closed.')
        except Error as e:
            print(f'Error closing connection: {e}')

class App: # INFO: New class to manage the user experience.
    def __init__(self):
        self.db = DatabaseManager()

    def show_menu(self): # INFO: Displays menu in a neat format.
        menu = [
            ['Option', 'Description'],
            ['1', 'Enter User Data'],
            ['2', 'View Data By Province'],
            ['3', 'Show Statistics & Reports'],
            ['4', 'Show Custom Statistics'],
            ['5', 'Exit Application']
        ]
        print(tabulate(menu, headers="firstrow", tablefmt="grid"))

    def handle_input(self): # INFO: Handle input is self explanatory.
        while True:
            self.show_menu()
            choice = input('Choose an option: ')
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.view_data()
            elif choice == '3':
                self.show_statistics()
            elif choice == '4':
                self.show_custom_statistics()
            elif choice == '5':
                self.db.close_connection()
                print('Exiting...')
                break
            else:
                print('Invalid input! Please try again.')

    def add_user(self): # INFO: Allow new user creation.
        name = input('Enter name: ').strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        age = int(input('Enter age: '))
        if not age:
            raise ValueError("Age cannot be empty.")
        gender = input('Enter gender (Male/Female/Other): ').strip().lower()
        if not gender:
            raise ValueError("Gender cannot be empty.")
        province = input('Enter province: ').strip()
        if not province:
            raise ValueError("Province cannot be empty.")
        educational_level = input('Enter highest level of education (Primary, Highschool, Bachelors, Masters, PhD): ').strip().lower()
        if not educational_level:
            raise ValueError("Education level cannot be empty.")
        new_user = User(name, age, gender, province, educational_level)
        self.db.add_user(new_user)

    def view_data(self): # INFO: Displays user data.
        province = input('Enter the province to view: ').strip()
        users = self.db.view_by_province(province)
        if users:
            print(tabulate(users, headers=["ID", "Name", "Age", "Gender", "Province", "Education"], tablefmt="grid"))
        else:
            print('No data found for that province.')

    def show_statistics(self): # INFO: Provides stats.
        stats = self.db.get_stats()
        if stats:
            print(tabulate(stats, headers=["Province", "User Count"], tablefmt="grid"))
        else:
            print('No data available.')

    def show_custom_statistics(self): # INFO: Shows custom stats.
        province = input('Enter the province for custom statistics: ').strip()
        educated, uneducated = self.db.get_education_stats(province)
        total = educated + uneducated
        if total > 0:
            print(f"In {province}, {educated} people are educated ({(educated / total) * 100:.2f}%) and {uneducated} are uneducated ({(uneducated / total) * 100:.2f}%).")
        else:
            print(f'No data available for {province}.')

if __name__ == '__main__':
    app = App()
    app.handle_input()
