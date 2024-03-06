# main.py
# app.py
import psycopg2
from flask import *
import settings
from flask_session import Session
import reg_autho
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'singularity'  # Replace with a unique and secret key
# Configure the Flask app to use the 'filesystem' session type
app.config['SESSION_TYPE'] = 'filesystem'
# Set the session timeout (in seconds), for example, 600 seconds (10 minutes)
app.config['PERMANENT_SESSION_LIFETIME'] = 600
Session(app)



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Add more if needed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_picture(file, user_id):
    if file and allowed_file(file.filename):
        filename = f"user_{user_id}_profile_picture.jpg"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Return the file path, not base64 encoding
        return file_path
    else:
        return None
# global session_user_id
@app.route('/')
def index():
    
    return render_template('login.html')

@app.route('/feed', methods=['GET'])
def feed():
    user_id = session.get('user_id')

    if user_id is not None:
        user_data = get_user_data(user_id)
        user_pic = user_data[8]
        if user_pic == None:
            user_pic = 'uploads/default.png'
    
        return render_template('feed.html', user=user_id, user_pic=user_pic)
    else:
        # Handle case where user is not authenticated
        return redirect(url_for('login'))

@app.route('/get_posts_wall', methods=['GET'])
def get_posts_wall():
    user_id = session.get('user_id')
    feed_posts = '1'  # Initialize to None in case there's an exception

    if user_id is not None:
        
        try:
            conn = psycopg2.connect(**settings.DATABASE_CONFIG)
            cursor = conn.cursor()
            
            # Fetch posts from friends with JOIN and ORDER BY timestamp
            cursor.execute("""
                SELECT distinct(p.post_id), p.user_id, p.content, p.timestamp, u.username, u.f_name, u.s_name
                FROM friends f
                JOIN posts p ON (f.user_id1 = p.user_id OR f.user_id2 = p.user_id)
                JOIN users u ON p.user_id = u.user_id
                WHERE f.user_id1 = %s OR f.user_id2 = %s
                ORDER BY p.timestamp DESC;

            """, (user_id,user_id))
            
                        
            feed_posts = cursor.fetchall()
            print(feed_posts, user_id, flush=True)
            cursor.close()
            conn.close()
        except Exception as e:
            print(e, flush=True)

        
    return  feed_posts


@app.route('/dialogue')
def dialogue():
    
    return render_template('dialogue.html')
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/update_profile',  methods=['GET'])
def update_profile():
    session_user_id = session.get('user_id')

    user_data = get_user_data(session_user_id)
   
    if user_data:
        return render_template('profile_update.html', user=user_data)
    else:
        return redirect('/login')

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
        print(new_pic, flush=True)
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

    # Retrieve the user ID from the URL parameters
    url_user_id = request.args.get('user_id')

    # Check if the viewer is the owner of the profile
    is_owner = False

    if url_user_id is not None:
        # If url_user_id is present in the URL, use it
        url_user_id = int(url_user_id)
        is_owner = session_user_id == url_user_id
    else:
        # If url_user_id is not present, use session_user_id
        url_user_id = session_user_id
        is_owner = True  # Assume the viewer is the owner if no specific user_id is provided in the URL

    # Retrieve additional user data from the database based on user ID
    user_data = get_user_data(url_user_id)
    user_pic = user_data[8]
    if user_pic == None:
        user_pic = 'uploads/default.png'

    if user_data:
        print(user_data, flush=True)
        # Render the dashboard template with the retrieved user data and ownership status
        return render_template('profile.html', user=user_data, user_pic=user_pic, is_owner=is_owner)
    else:
        return redirect('/login')




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
        else:
            return render_template('registration.html', error='We have someone already with that username or email')

    # Render the registration page for GET requests or failed registration
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if the user is already logged in
    if 'user_id' in session:
        # User is already logged in, redirect to the dashboard or profile
        return redirect(url_for('profile'))  # or 'profile'

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
            # Pass an error message to the login page
            return render_template('login.html', error_message='Incorrect username or password')

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
            SELECT CONCAT(u1.f_name, ' ', u1.s_name) AS friend_name, u1.picture AS friend_picture, u1.user_id AS friend_id
            FROM friends f
            JOIN users u1 ON (f.user_id2 = u1.user_id)
            WHERE f.user_id1 = %s AND f.status = 'accepted'
            
            UNION
            
            SELECT CONCAT(u2.f_name, ' ', u2.s_name) AS friend_name, u2.picture AS friend_picture, u2.user_id AS friend_id
            FROM friends f
            JOIN users u2 ON (f.user_id1 = u2.user_id)
            WHERE f.user_id2 = %s AND f.status = 'accepted'
        """, (user_id, user_id))


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
    friends_data = [{'id': friend[0], 'username': friend[1], 'picture': friend[2] or 'uploads/default.png'} for friend in friends]

    return jsonify(friends_data)

@app.route('/add_friend/<int:friend_id>', methods=['POST'])
def add_friend(friend_id):
    try:
        session_user_id = session.get('user_id')

        if not session_user_id:
            # Unauthorized access, redirect to login or handle as needed
            return redirect('/login')

        # Check if the friend_id is valid and not the same as the user's ID
        if friend_id == session_user_id:
            # Invalid friend_id, handle as needed (e.g., show an error message)
            return jsonify({'error': 'Invalid friend_id'})

        # Check if the friendship already exists
        if not friendship_exists(session_user_id, friend_id):
            # Insert the friendship with 'accepted' status
            insert_friendship(session_user_id, friend_id, 'accepted')

            # Return a success response (you can customize this as needed)
            return jsonify({'success': 'Friend request sent successfully'})
        else:
            # Friendship already exists, handle as needed (e.g., show a message)
            return jsonify({'info': 'Friendship already exists'})

    except Exception as e:
        print("Error adding friend:", e)
        return jsonify({'error': 'An error occurred while adding a friend'})

def friendship_exists(user_id1, user_id2):
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = conn.cursor()

        # Check if the friendship already exists with 'accepted' status
        cursor.execute("""
            SELECT id FROM friends
            WHERE (user_id1 = %s AND user_id2 = %s AND status = 'accepted')
               OR (user_id1 = %s AND user_id2 = %s AND status = 'accepted')
        """, (user_id1, user_id2, user_id2, user_id1))

        result = cursor.fetchone()

        # Disconnect
        cursor.close()
        conn.close()

        return result is not None  # Return True if friendship exists, False otherwise

    except Exception as e:
        print('Error checking friendship:', e)
        return False  # Assume friendship exists in case of an error

def insert_friendship(user_id1, user_id2, status):
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = conn.cursor()

        # Insert the friendship with 'accepted' status
        cursor.execute("""
            INSERT INTO public.friends (user_id1, user_id2, status, created_at)
            VALUES (%s, %s, %s, NOW())
        """, (user_id1, user_id2, status))

        # Commit the changes
        conn.commit()

        # Disconnect
        cursor.close()
        conn.close()

    except Exception as e:
        print('Error inserting friendship:', e)

    
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/success')
def success():
    return redirect('/login')

@app.route('/search')
def search():
    user_id = session.get('user_id')

    if user_id is not None:
        user_data = get_user_data(user_id)
        user_pic = user_data[8]
        if user_pic == None:
            user_pic = 'uploads/default.png'
    return render_template('search.html', user=user_data, user_pic=user_pic)

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
        cursor.execute("SELECT CONCAT(f_name, ' ', s_name), picture, user_id FROM users WHERE username ILIKE %s", (search_letter + '%',))
        users = cursor.fetchall()
        # print(users, flush=True)
        # Disconnect
        cursor.close()
        conn.close()

        return users

    except Exception as e:
        print('Error occurred:', e)
        return []  # Return an empty list if an error occurs

# Route to get posts for a specific user
@app.route('/get_posts/<int:user_id>', methods=['GET'])
def get_posts(user_id):
    try:
        # Connect to the database
        connection = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = connection.cursor()

        # Fetch posts for the specified user from the database
        cursor.execute("""
            SELECT post_id, user_id, content, timestamp
            FROM posts
            WHERE user_id = %s
        """, (user_id,))

        posts = cursor.fetchall()

        # Convert posts to a list of dictionaries
        posts_list = [
            {'post_id': post[0], 'user_id': post[1], 'content': post[2], 'timestamp': post[3]}
            for post in posts
        ]

        # Close the database connection
        connection.close()

        return jsonify(posts_list)
    except Exception as e:
        return str(e)

# Route to add a new post for a specific user
@app.route('/add_post/<int:user_id>', methods=['POST'])
def add_post(user_id):
    try:
        # Connect to the database
        connection = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = connection.cursor()

        # Get the content from the request
        content = request.form.get('content')

        # Insert a new post into the database
        cursor.execute("""
            INSERT INTO posts (user_id, content, timestamp)
            VALUES (%s, %s, %s)
        """, (user_id, content, datetime.utcnow()))

        # Commit the transaction and close the database connection
        connection.commit()
        connection.close()

        return 'Post added successfully!'
    except Exception as e:
        return str(e)


# Route to handle post deletion
@app.route('/delete_post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        # Connect to the database
        connection = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = connection.cursor()

        # Delete the post with the given post_id
        cursor.execute("DELETE FROM posts WHERE post_id = %s", (post_id,))
        
        # Commit the changes to the database
        connection.commit()

        # Close the database connection
        cursor.close()
        connection.close()

        return jsonify({'message': 'Post deleted successfully'}), 200

    except Exception as e:
        # Handle any errors that may occur during the process
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message='Page not found'), 404

# Custom error handler for other errors
@app.errorhandler(Exception)
def handle_error(error):
    return render_template('error.html', error_code=500, error_message='Internal Server Error'), 500


if __name__ == '__main__':
    app.run(debug=True)
