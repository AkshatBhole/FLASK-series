FlaskMarket
Overview
FlaskMarket is a web-based marketplace application built with Flask, a lightweight Python web framework. It allows users to register, log in, and buy or sell items in a virtual market. Each user has a budget, and they can purchase items if they have sufficient funds. Purchased items are moved to the user's "Owned Items" section, and users can sell them back to the market to regain some of their budget. The application uses SQLite as the database to store user and item data.
This project was developed as a learning exercise to explore Flask, SQLAlchemy for database management, Flask-Login for user authentication, and Bootstrap for front-end styling.
Features

User registration and login/logout functionality.
A market page where users can:
View available items for purchase.
Purchase items if they have sufficient budget.
View their owned items.
Sell items back to the market.

Budget management for users (deducted on purchase, credited on sale).
Flash messages for user feedback (e.g., successful purchase, insufficient funds).
Responsive UI using Bootstrap.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.6 or higher: The project is built using Python.
pip: Python package manager to install dependencies.
Virtualenv (optional but recommended): To create an isolated environment for the project.
A web browser to access the application.

Installation
Follow these steps to set up the project on your local machine:

Clone the Repository:
git clone https://github.com/yourusername/flaskmarket.git
cd flaskmarket

Set Up a Virtual Environment (Optional but recommended):
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

Install Dependencies:The project dependencies are listed in requirements.txt. Install them using:
pip install -r requirements.txt

If you don’t have a requirements.txt, you can install the required packages manually:
pip install flask flask-sqlalchemy flask-bcrypt flask-login wtforms

Initialize the Database:The project uses SQLite as the database, stored in the instance/market.db file. To create and populate the database:
python populate_db.py

This script will create the database and add some initial items and a test user (testuser with password password123).

Run the Application:Start the Flask development server:
python run.py

The application will be accessible at http://127.0.0.1:5000.

Usage

Access the Application:Open your browser and navigate to http://127.0.0.1:5000.

Register or Log In:

Go to /register to create a new account.
Go to /login to log in with an existing account (e.g., username: testuser, password: password123).

Explore the Market:

After logging in, you’ll be redirected to /market.
Available Items: View items available for purchase (items with no owner).
Your Items: View items you own.
Purchase an Item: Click "Purchase Item" next to an available item. If you have enough budget, the item will be added to your "Owned Items," and your budget will be deducted.
Sell an Item: Click "Sell Item" next to an item in your "Owned Items" to sell it back to the market. Your budget will be credited.

Log Out:

Go to /logout to log out of your account.

Project Structure
flaskmarket/
│
├── instance/
│ └── market.db # SQLite database file
├── market/
│ ├── **init**.py # Flask app configuration and initialization
│ ├── models.py # Database models (User, Item)
│ ├── routes.py # Application routes (home, market, register, login, logout)
│ ├── forms.py # WTForms for user input (RegisterForm, LoginForm, etc.)
│ └── templates/
│ ├── home.html # Home page template
│ ├── market.html # Market page template
│ ├── register.html # Registration page template
│ └── login.html # Login page template
├── populate_db.py # Script to initialize and populate the database
├── run.py # Entry point to run the Flask app
└── README.md # Project documentation

Database Schema

User:

id: Primary key
username: Unique username (string)
email_address: Unique email (string)
password_hash: Hashed password (string)
budget: User’s budget (float, default 1000.0)

Item:

id: Primary key
name: Item name (string, unique)
price: Item price (float)
barcode: Item barcode (string, unique)
description: Item description (string, unique)
owner: Foreign key referencing User.id (integer, nullable)

Troubleshooting

Purchased Items Not Showing in "Owned Items":

Ensure your user has sufficient budget to purchase the item.
Check the Flask logs for debug messages (e.g., After purchase commit - Item: Headphones, Owner: 1).
Verify the database (instance/market.db) to confirm the owner field of the item is updated:sqlite3 instance/market.db
SELECT \* FROM item WHERE name = 'Headphones';

Database Issues:

If the database schema is outdated, delete instance/market.db and rerun populate_db.py.
Consider using Flask-Migrate for schema migrations in the future:pip install flask-migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Session Issues:

Ensure SECRET_KEY is set in market/**init**.py to maintain user sessions:app.config['SECRET_KEY'] = 'your_secret_key_here'

Contributing
Contributions are welcome! If you’d like to contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit them (git commit -m "Add your feature").
Push to your branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with Flask, SQLAlchemy, and Bootstrap.
Inspired by Flask tutorials and marketplace application examples.
