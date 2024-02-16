# app.py
import psycopg2
from flask import *
import settings
import reg_autho
app = Flask(__name__)
app.secret_key = 'singularity'  # Replace with a unique and secret key
#eto dobavil mirlan

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
        user_id = reg_autho.db_login(username, password)
        if user_id:            
            session['user_id'] = user_id[0]

            # Redirect to a dashboard or home page on successful login with user details
            return redirect(url_for('dashboard', user_id=user_id))
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
# Assume you have functions to retrieve user data from the database based on user_id
def get_user_data(user_id):
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = conn.cursor()

        # Replace this query with the appropriate query to get user data based on user_id
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()

        # Disconnect
        cursor.close()
        conn.close()

        return user_data

    except Exception as e:
        print('Error occurred:', e)
        return None  # Return None if an error occurs

# Dashboard route
@app.route('/dashboard')
def dashboard():
    # Retrieve user ID from the session
    session_user_id = session.get('user_id')
    
    # Retrieve user ID from the URL parameters
    url_user_id = request.args.get('user_id')
    url_user_id = int(url_user_id) if url_user_id is not None else None

    if session_user_id is None or session_user_id != url_user_id:
        # Unauthorized access, redirect to login
        return redirect('/login')

    # Retrieve additional user data from the database based on user ID
    user_data = get_user_data(session_user_id)
    if user_data:
        # Render the dashboard template with the retrieved user data
        return render_template('dashboard.html', user=user_data)
    else:
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/success')
def success():
    return "Registration successful!"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message='Page not found'), 404

# Custom error handler for other errors
@app.errorhandler(Exception)
def handle_error(error):
    return render_template('error.html', error_code=500, error_message='Internal Server Error'), 500


if __name__ == '__main__':
    app.run(debug=True)
