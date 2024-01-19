# app.py

from flask import *

app = Flask(__name__)

# Assuming you have a user table in your database
# Modify the database connection function to include login
def db_login(username, password):
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = conn.cursor()

        # Example: Check if the provided username and password match a user in the database
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        # Disconnect
        cursor.close()
        conn.close()

        return user is not None  # Return True if login is successful
    except Exception as e:
        print('Error occurred:', e)
        return False  # Login failed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform registration in the database
        if db_register(username, password):
            # Redirect to the success page on successful registration
            return redirect(url_for('success'))

    # Render the registration page for GET requests or failed registration
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform login validation in the database
        if db_login(username, password):
            # Redirect to a dashboard or home page on successful login
            return redirect(url_for('dashboard'))

    # Render the login page for GET requests or failed login
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

@app.route('/success')
def success():
    return "Registration successful!"

if __name__ == '__main__':
    app.run(debug=True)
