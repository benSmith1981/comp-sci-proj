# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import MySQLdb.cursors, re, hashlib

# app = Flask(__name__)
# app.secret_key = 'catgamer'

# # Intialize MySQL
# mysql = MySQL(app)

# @app.route('/pythonlogin/', methods=['GET', 'POST'])
# def login():
#     # Output a message if something goes wrong
#     msg = 'Something went wrong'
#     # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         password = request.form['password']
#         # Retrieve the hashed password
#         hash = password + app.secret_key
#         hash = hashlib.sha1(hash.encode())
#         password = hash.hexdigest()
#          # Check if account exists using MySQL
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
#         # Fetch one record and return the result
#         account = cursor.fetchone()
#         # If account exists in accounts table in out database
#         if account:
#             # Create session data, we can access this data in other routes
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['username'] = account['username']
#             # Redirect to home page
#             return redirect(url_for('home'))
#         else:
#             # Account doesnt exist or username/password incorrect
#             msg = 'Incorrect username/password!'

# # http://localhost:5000/python/logout - this will be the logout page
# @app.route('/pythonlogin/logout')
# def logout():
#     # Remove session data, this will log the user out
#    session.pop('loggedin', None)
#    session.pop('id', None)
#    session.pop('username', None)
#    # Redirect to login page
#    return redirect(url_for('login'))

# # http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
# @app.route('/pythonlogin/register', methods=['GET', 'POST'])
# def register():
#     # Output message if something goes wrong...
#     msg = ''
#     # Check if "username", "password" and "email" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#     elif request.method == 'POST':
#         # Form is empty... (no POST data)
#         msg = 'Please fill out the form!'
#     # Show registration form with message (if any)
#     return render_template('register.html', msg=msg)


# # Check if account exists using MySQL
# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
# account = cursor.fetchone()
# # If account exists show error and validation checks
# if account:
#     msg = 'Account already exists!'
# elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#     msg = 'Invalid email address!'
# elif not re.match(r'[A-Za-z0-9]+', username):
#     msg = 'Username must contain only characters and numbers!'
# elif not username or not password or not email:
#     msg = 'Please fill out the form!'
# else:
#     # Hash the password
#     hash = password + app.secret_key
#     hash = hashlib.sha1(hash.encode())
#     password = hash.hexdigest()
#     # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
#     cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
#     mysql.connection.commit()
#     msg = 'You have successfully registered!'

# # http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for logged in users
# @app.route('/pythonlogin/home')
# def home():
#     # Check if the user is logged in
#     if 'loggedin' in session:
#         # User is loggedin show them the home page
#         return render_template('home.html', username=session['username'])
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

# # http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
# @app.route('/pythonlogin/profile')
# def profile():
#     # Check if the user is logged in
#     if 'loggedin' in session:
#         # We need all the account info for the user so we can display it on the profile page
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
#         account = cursor.fetchone()
#         # Show the profile page with account info
#         return render_template('profile.html', account=account)
#     # User is not logged in redirect to login page
#     return redirect(url_for('login'))

# if __name__ == '__main__':        
#     with app.app_context():
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
#         account = cursor.fetchone()
#         # your script or initialization code here
#         app.run()


from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re, hashlib

app = Flask(__name__)
app.secret_key = 'catgamer'

# Initialize MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_user'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_db'
mysql = MySQL(app)

@app.route('/pythonlogin', methods=['GET', 'POST'])
def login():
    msg = 'Something went wrong'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Hash the password
        hash = hashlib.sha1((password + app.secret_key).encode()).hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, hash))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Hash the password
            hash = hashlib.sha1((password + app.secret_key).encode()).hexdigest()
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, hash, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    return render_template('register.html', msg=msg)

@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
