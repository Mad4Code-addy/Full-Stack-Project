# Flask Contact Form with Admin Panel

A Python Flask web application featuring:
- Public contact form with submissions stored in SQLite
- Admin authentication system
- Admin management interface
- Responsive design with Bootstrap-like styling

## Features

- User-facing contact form (name, email, message)
- Admin login/logout functionality
- Admin dashboard to view submissions
- Admin management (add/remove admin users)
- SQLite database storage
- Environment variable configuration
- CSRF protection
- Password hashing

## Prerequisites

- Python 3.8+
- pip package manager

## Installation

1. **Clone the repository**:
   
       git clone https://github.com/gspagare/Full-Stack-Project.git
       cd Full-Stack-Project

2. **Create and activate virtual environment**:

       python -m venv venv
    ### On Windows:
       venv\Scripts\activate
    ### On macOS/Linux:
       source venv/bin/activate

3. **Install dependencies**:

       pip install -r requirements.txt

## Configuration

1. **Create environment files**:

    Create .env file:

        SECRET_KEY=your-secret-key-here
        DATABASE_URL=sqlite:///instance/site.db
        ADMIN_USERNAME=admin
        ADMIN_PASSWORD=securepassword123

    Create .flaskenv file:

        FLASK_APP=app.py
        FLASK_ENV=development

2. **Database Setup**:

    The SQLite database will be automatically created in the instance folder when you first run the application.

## Running the Application

    python app.py

   The application will be available at http://localhost:5000

## First-Time Setup

1. Access the admin panel at http://localhost:5000/login

2. Log in using the credentials from your .env file

3. Immediately:
   Add a new admin account with secure credentials
   Log out and log in with the new admin account
   Delete the default admin account (recommended)
