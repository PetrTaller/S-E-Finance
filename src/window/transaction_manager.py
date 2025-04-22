import mysql.connector
from tkinter import messagebox
from user_manager import get_db_connection
from user_manager import get_username

def get_user_transactions():
    """Retrieves all transactions of the currently logged-in user."""
    username = get_username()
    if username:
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT t.id, t.amount, t.source, t.date
                    FROM transaction t
                    JOIN user u ON t.user_id = u.id
                    WHERE u.username = %s
                    ORDER BY t.date DESC
                """, (username,))
                transactions = cursor.fetchall()
                return transactions
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                messagebox.showerror("Database Error", "Could not retrieve transactions.")
                return []
            finally:
                connection.close()
    return []
import mysql.connector
from tkinter import messagebox
from datetime import datetime

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

def add_transaction(user_id, amount, source, date=None):
    """Adds a new transaction to the database and updates the user's balance."""
    if not date:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Ensure amount is a valid integer (or float if you support decimals)
        amount = int(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return False

    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        # Insert the transaction
        cursor.execute("""
            INSERT INTO transaction (user_id, amount, source, date)
            VALUES (%s, %s, %s, %s)
        """, (user_id, amount, source, date))

        # Update the user's balance
        cursor.execute("""
            UPDATE user
            SET balance = balance + %s
            WHERE id = %s
        """, (amount, user_id))

        connection.commit()
        messagebox.showinfo("Success", "Transaction added and balance updated successfully.")
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Error", "Failed to add transaction.")
        return False
    finally:
        cursor.close()
        connection.close()

