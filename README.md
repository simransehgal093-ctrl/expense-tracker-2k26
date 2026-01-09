# Expense Tracker 2k26

A simple and secure Expense Tracker web application built using **Flask** and **MySQL**.

## Features
- User Registration with password hashing
- User Login & Logout
- Session-based authentication
- Add, view, and delete expenses
- Each user sees only their own data
- Clean and responsive UI using Bootstrap

## Tech Stack
- Backend: Python (Flask)
- Database: MySQL
- Frontend: HTML, Bootstrap
- Authentication: Werkzeug password hashing

```## Project Structure 
expense-tracker-2k26/
├── app.py
├── requirements.txt
├── templates/
│ ├── base.html
│ ├── register.html
│ ├── login.html
│ ├── dashboard.html
│ └── edit_expense.html
└── venv/
```

```## Setup Instructions

1. Clone the repository
git clone <repository-url>
cd expense-tracker-2k26
Create and activate virtual environment

2.
python -m venv venv
venv\Scripts\activate
Install dependencies

3.
pip install -r requirements.txt
Create MySQL database

4 in sql,
CREATE DATABASE expense_tracker_2k26;
Run the application

5.
python app.py
Open browser


http://127.0.0.1:5000```



**Test Cases**

User can register with valid username, email, and password

Passwords are stored in hashed format

User can login with correct credentials

Invalid login shows error message

Unauthenticated user cannot access dashboard

Logged-in user can add an expense

Logged-in user can edit an expense

Logged-in user can delete an expense

User can logout successfully
