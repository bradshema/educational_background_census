# INFO: Project Setup Guide

This guide will help you set up the project, access the MySQL database, and run the application locally.

# 1. Clone the GitHub Repository

Start by cloning the project repository to your local machine:

    "git clone https://github.com/bradshema/educational_background_census.git"


2. Set Up MySQL Locally

Make sure you have MySQL installed. If you don't have it, download and install it from the MySQL website.


3. Create a Database
Once MySQL is installed, you'll need to create a new database to import the data into.

Log into MySQL:

    "mysql -u root -p"

Create a new database (replace your_database_name with a name of your choice):

    "CREATE DATABASE your_database_name;"

Exit MySQL:

    "Exit"


4. Import the Database

Next, import the database from the exported_database.sql file into the database you just created.

Navigate to the folder where exported_database.sql is located.

Run the following command (replace your_database_name with the name you created):

    "mysql -u root -p your_database_name < exported_database.sql"

# This will import the database structure and data into your local MySQL server.


5. Configure the Project
You'll need to update the project’s configuration files to connect to your local MySQL database.

    Look for a configuration file like .env or something similar in the project.

    Update the database connection details:

        DB_HOST: localhost (usually the default)

        DB_USERNAME: root (or your MySQL username)

        DB_PASSWORD: Your MySQL password

        DB_NAME: The name of the database you created (your_database_name)

Example .env file:
    DB_HOST=localhost
    DB_USERNAME=root
    DB_PASSWORD=your_password
    DB_NAME=your_database_name


6. Run the Project
Now that the database is set up and the configuration is updated, you're ready to run the project!

    Follow the instructions in the project to start it locally (e.g., npm start for Node.js or python app.py for Python projects).


Troubleshooting!!!

    Can't connect to MySQL? Make sure MySQL is running and your credentials are correct.

    Database import fails? Double-check that you're importing the .sql file into the correct database.

    Code not working? Ensure all dependencies are installed and the configuration is set up correctly.

    If you run into issues, don't hesitate to reach out!


