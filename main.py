# main.py
# app.py
import psycopg2
from flask import *
import settings
import reg_autho
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'singularity'  # Replace with a unique and secret key
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Add more if needed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_picture(file, user_id):
    if file and allowed_file(file.filename):
        filename = f"user_{user_id}_profile_picture.jpg"  # You can modify the filename as needed
        print(filename, app.config['UPLOAD_FOLDER'], file, flush=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    else:
        return None
# global session_user_id
@app.route('/')
def index():
    
    return render_template('index.html')
@app.route('/feed')
def feed():
    
    return render_template('feed.html')

@app.route('/dialogue')
def dialogue():
    
    return render_template('dialogue.html')

@app.route('/update_profile',  methods=['GET'])
def update_profile():
    session_user_id = session.get('user_id')
    
    # # Retrieve user ID from the URL parameters
    # url_user_id = request.args.get('user_id')
    # url_user_id = int(url_user_id) if url_user_id is not None else None

    # if session_user_id is None or session_user_id != url_user_id:
    #     # Unauthorized access, redirect to login
    #     return redirect('/login')

    # Retrieve additional user data from the database based on user ID
    user_data = get_user_data(session_user_id)
    # print(user_data, flush=True)
    if user_data:
        
        # Render the dashboard template with the retrieved user data
        return render_template('profile_update.html', user=user_data)
    else:
        return redirect('/login')
    # return render_template('profile_update.html')
def update_user_data(user_id, new_username, new_email, new_phone, new_pic):
    
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = conn.cursor()

        # Construct the SQL query to update user data
        update_query = """
            UPDATE public.users
            SET username = %s, email = %s, phone = %s, picture = %s
            WHERE user_id = %s
        """

        # Execute the query with the new data
        cursor.execute(update_query, (new_username, new_email, new_phone, new_pic, user_id))

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()


        return True  # Update successful
    except Exception as e:
        print("Error updating user data:", e)
        return False  # Update failed

@app.route('/update_profile_post', methods=['POST'])
def update_profile_post():
    try:
        session_user_id = session.get('user_id')

        if not session_user_id:
            # Unauthorized access, redirect to login
            return redirect('/login')

        # Retrieve user data from the database based on the session user ID
        user_data = get_user_data(session_user_id)

        if not user_data:
            return redirect('/login')

        # Retrieve form data
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        new_phone = request.form.get('phone')
        print(request.files,flush=True)

        # Handle profile picture upload
        
        if 'new_profile_picture' in request.files:
            
            new_profile_picture = request.files['new_profile_picture']
            
            # Save the new profile picture and get the filename
            profile_picture_filename = save_profile_picture(new_profile_picture, session_user_id)
            
            # Update user data in the database
            update_user_data(session_user_id, new_username, new_email, new_phone, profile_picture_filename)

        # Redirect to the updated profile page
        return redirect(url_for('profile'))
    except Exception as e:
        print("Error updating profile:", e, flush=True)
        abort(500)  # Raise a 500 error and display the error message
@app.route('/wall')
def wall():
    
    return render_template('wall.html')

@app.route('/profile')
def profile():
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
        return render_template('profile.html', user=user_data)
    else:
        return redirect('/login')
    # return render_template('profile.html')

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
            return redirect(url_for('profile', user_id=user_id))
        else:   
            return 'Something went wrong'


    # Render the login page for GET requests or failed login
    return render_template('login.html')
@app.route('/check-username', methods=['POST'])
def check_username():
    # Get the username from the AJAX request
    username = request.form.get('username')
    # print(username, flush=True)
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
        # print(user_data, flush=True)
        # Disconnect
        cursor.close()
        conn.close()

        return user_data

    except Exception as e:
        print('Error occurred:', e)
        return None  # Return None if an error occurs
    
@app.route('/get_friends/<int:user_id>', methods=['GET'])
def get_user_friends(user_id):
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = conn.cursor()

        # Example query to retrieve friends of the given user
        cursor.execute("""
            SELECT u.username, u.picture
            FROM friends f
            JOIN users u ON (f.user_id2 = u.user_id)
            WHERE f.user_id1 = %s AND f.status = 'pending'
        """, (user_id,))

        friends = cursor.fetchall()

        # Disconnect
        cursor.close()
        conn.close()

        return jsonify(friends)

    except Exception as e:
        print('Error occurred:', e)
        return jsonify([])  # Return an empty list if an error occurs    
    
@app.route('/get_friends/<int:user_id>')
def get_friends(user_id):
    # Assuming you have a function to fetch friends from the database
    friends = get_user_friends(user_id)

    # Convert the friends data to a format suitable for JSON response
    friends_data = [{'id': friend[0], 'username': friend[1]} for friend in friends]

    return jsonify(friends_data)
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

@app.route('/search')
def search():
    return render_template('search.html')

# New route for handling user search
@app.route('/search_user', methods=['GET'])
def search_users():
    search_letter = request.args.get('letter')

    # Perform a database query to retrieve users starting with the given letter
    users = get_users_by_letter(search_letter)

    # Return the results as JSON
    return jsonify(users)

def get_users_by_letter(search_letter):
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)  # Ensure you have the correct database configuration
        cursor = conn.cursor()

        # Example query to retrieve users starting with the given letter
        cursor.execute("SELECT username, picture FROM users WHERE username ILIKE %s", (search_letter + '%',))
        users = cursor.fetchall()
        # print(users, flush=True)
        # Disconnect
        cursor.close()
        conn.close()

        return users

    except Exception as e:
        print('Error occurred:', e)
        return []  # Return an empty list if an error occurs

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message='Page not found'), 404

# Custom error handler for other errors
@app.errorhandler(Exception)
def handle_error(error):
    return render_template('error.html', error_code=500, error_message='Internal Server Error'), 500


if __name__ == '__main__':
    app.run(debug=True)
