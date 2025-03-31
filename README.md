# Educational Statistics Project: Project Setup Guide

This guide will help you set up the project, access the MySQL database, and run the application locally.

## 1. Clone the GitHub Repository

Start by cloning the project repository to your local machine:

    git clone https://github.com/bradshema/educational_background_census.git


## 2. Navigate to Project Directory

    cd educational_background_census

## 3. Install Dependencies

    pip install -r requirements.txt

## 4. Database Setup
Run the setup script which will configure your MySQL database:
    ./setup.py

The script will prompt you for:
- MySQL username (default: root)
- MySQL password (default: empty)

This will automatically set up the database for you.


## 5. Run the Application
    python3 peer_learning_project_2.py

Follow the menu instructions displayed in the terminal.
Troubleshooting!!!


## Troubleshooting

- **Database Connection Issues**: Verify your MySQL credentials are correct
- **Missing Dependencies**: Make sure all requirements were installed successfully
- **Permission Issues**: Ensure you have appropriate permissions to create and modify databases