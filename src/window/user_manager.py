import json
from tkinter import messagebox
import bcrypt
import mysql.connector
import os

def get_db_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='Projekt'
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Error", "Could not connect to the database.")
        return None
    
SESSION_FILE = os.path.join(os.path.dirname(__file__), '..', 'saved', 'session.json')

def load_session():
    """Loads session data from session.json."""
    try:
        with open(SESSION_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {SESSION_FILE} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON in {SESSION_FILE}.")
        return None
    
def delete_session():
    """Deletes the current session by removing session.json."""
    try:
        with open(SESSION_FILE, 'w') as file:
            file.write("{}")  # Clears the session file
        print("Session deleted successfully.")
    except Exception as e:
        print(f"Error: Could not delete session: {e}")

def save_session(session_data):
    """Saves session data to session.json."""
    try:
        with open(SESSION_FILE, 'w') as file:
            json.dump(session_data, file, indent=4)
    except Exception as e:
        print(f"Error: Could not save to {SESSION_FILE}: {e}")

def create_session(username, password):
    """Creates a new session with the provided username and hashed password."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    session_data = {
        "username": username,
        "password": hashed_password
    }
    save_session(session_data)
    print("Session created successfully.")

def load_users():
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        return users
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Error", "Could not retrieve users.")
        return []
    finally:
        if connection:
            connection.close()

def save_user(user_id, username, password, balance):
    """Saves or updates a user in the database."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE user
        SET username = %s, password = %s, balance = %s
        WHERE id = %s
    """, (username, password, balance, user_id))
    connection.commit()
    cursor.close()
    connection.close()

def find_user_by_username(username):
    """Finds a user by username in the database."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

def get_username():
    """Returns the username from the current session."""
    session = load_session()
    return session.get('username') if session else None

def get_balance():
    """Returns the balance of the current user."""
    username = get_username()
    if username:
        user = find_user_by_username(username)
        return user.get('balance') if user else None
    return None

def set_username(new_username):
    username = get_username()
    if username:
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("UPDATE user SET username = %s WHERE username = %s", (new_username, username))
                connection.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            finally:
                connection.close()
    return False

def set_balance(new_balance):
    username = get_username()
    if username:
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("UPDATE user SET balance = %s WHERE username = %s", (new_balance, username))
                connection.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            finally:
                connection.close()
    return False

def set_password(new_password):
    username = get_username()
    if username:
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("UPDATE user SET password = %s WHERE username = %s", (hashed_password, username))
                connection.commit()
                return True
            except mysql.connector.Error as err:
                print(f"Error: {err}")
            finally:
                connection.close()
    return False

def register_user(username, password):
    """Registers a new user in the database."""
    users = load_users()
    if any(user['username'] == username for user in users):
        messagebox.showerror("Registration Error", "Username already exists.")
        return
    elif username == "":
        messagebox.showerror("Registration Error", "Username cannot be blank.")
        return
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO user (username, password, balance)
        VALUES (%s, %s, %s)
    """, (username, hashed_password, 0))
    connection.commit()
    cursor.close()
    connection.close()
    messagebox.showinfo("Registration Successful", "You can now log in.")

def authenticate_user(username_entry, password_entry, method, content_frame, clear_content):
    """Authenticates user based on username and password."""
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Input Error", "Username and password cannot be empty.")
        return
    user = find_user_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        create_session(username, password)
        method(content_frame, clear_content)
        print(f"User {username} authenticated successfully.")
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")


        