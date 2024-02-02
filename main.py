# app.py
import psycopg2
from flask import *
import settings
import reg_autho
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        f_name = request.form['firstName']
        s_name = request.form['lastName']
        email = request.form['email']
        dob = request.form['dob']
        phone = request.form['phone']

        # Perform registration in the database
        if reg_autho.db_register(username, password, f_name, s_name, email, dob, phone):
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
        if reg_autho.db_login(username, password):
            # Redirect to a dashboard or home page on successful login
            return redirect(url_for('dashboard'))
        else:
            return 'Something went wrong'

    # Render the login page for GET requests or failed login
    return render_template('login.html')
@app.route('/check-username', methods=['POST'])
def check_username():
    # Get the username from the AJAX request
    username = request.form.get('username')
    print(username, flush=True)
    # Perform the check (replace this with your actual logic)
    is_username_available = not username_exists_in_database(username)

    # Return the result as JSON
    return jsonify({'available': is_username_available})

def username_exists_in_database(username):
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = conn.cursor()

        # Example query to check if the username exists in the "users" table
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        # Disconnect
        cursor.close()
        conn.close()

        return result is not None  # Return True if the username exists, False otherwise
    except Exception as e:
        print('Error occurred:', e)
        return False  # Assume username exists in case of an error

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

@app.route('/success')
def success():
    return "Registration successful!"

if __name__ == '__main__':
    app.run(debug=True)
