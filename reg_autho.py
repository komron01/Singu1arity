# database.py

import psycopg2
import settings

def db_register(username, password, f_name, s_name, email, dob, phone):
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = conn.cursor()

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()


        if existing_user:
            # Username already exists, return False (registration failed)
            return False

        # Insert the new user
        cursor.execute(
            "INSERT INTO users (username, password, f_name, s_name, email, dob, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (username, password, f_name, s_name, email, dob, phone)
        )

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return True to indicate successful registration
        return True

    except Exception as e:
        print('Error occurred:', e)
        return False  # Registration failed


def db_login(username, password):
    try:
        conn = psycopg2.connect(**settings.DATABASE_CONFIG)
        cursor = conn.cursor()

        # Example: Check if the provided username and password match a user in the database
        cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (username, password))
        user_id = cursor.fetchone()

        # Disconnect
        cursor.close()
        conn.close()

        return user_id  # Return the user_id if login is successful, None otherwise
    except Exception as e:
        print('Error occurred:', e)
        return None  # Login failed