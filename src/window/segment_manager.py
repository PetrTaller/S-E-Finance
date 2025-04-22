import mysql.connector
from tkinter import messagebox
from user_manager import load_session, find_user_by_username

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

def fetch_segments():
    """Fetch all segments from the database and organize them by parent_id."""
    conn = get_db_connection()
    if conn is None:
        return {}

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM segment ORDER BY parent_id, id")
    segments = cursor.fetchall()
    cursor.close()
    conn.close()

    segments_dict = {}

    # Create a dictionary of segments keyed by their ID
    for segment in segments:
        segments_dict[segment["id"]] = {**segment, "subsegments": []}

    # Now link subsegments to their respective parents
    for segment in segments:
        parent_id = segment["parent_id"]
        if parent_id is not None:
            segments_dict[parent_id]["subsegments"].append(segments_dict[segment["id"]])

    # Return only top-level segments (parent_id is None)
    top_level_segments = {k: v for k, v in segments_dict.items() if v["parent_id"] is None}

    return top_level_segments

def update_segment(segment_id, name, color, percentage):
    """Update a segment in the database."""
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    query = """
        UPDATE segment
        SET name = %s, color = %s, percentage = %s
        WHERE id = %s
    """
    cursor.execute(query, (name, color, percentage, segment_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_segment_color(segment_id):
    """Retrieve the color of a specific segment by its ID."""
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        query = "SELECT color FROM segment WHERE id = %s"
        cursor.execute(query, (segment_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            messagebox.showerror("Not Found", f"No segment found with ID {segment_id}")
            return None

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not fetch segment color: {err}")
        return None

    finally:
        conn.close()

def add_segment(name, color, percentage, parent_id=None):
    """Add a new segment to the database, associated with the current user."""
    session = load_session()
    if not session or "username" not in session:
        messagebox.showerror("Session Error", "No user is logged in.")
        return

    username = session.get("username")
    user = find_user_by_username(username)
    if not user:
        messagebox.showerror("User Error", "Could not find user in the database.")
        return

    user_id = user.get("id")
    if not user_id:
        messagebox.showerror("User Error", "User ID is not available.")
        return

    conn = get_db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO segment (name, color, percentage, parent_id, user_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, color, percentage, parent_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Segment added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not add segment: {err}")
        if conn:
            conn.close()

def fetch_all_segments_flat():
    """Fetch all segments from the database in a flat list."""
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM segment")
    segments = cursor.fetchall()
    cursor.close()
    conn.close()

    return segments

def delete_segment(segment_id):
    """Delete a segment from the database, associated with the current user."""
    session = load_session()
    if not session or "username" not in session:
        messagebox.showerror("Session Error", "No user is logged in.")
        return

    username = session.get("username")
    user = find_user_by_username(username)
    if not user:
        messagebox.showerror("User Error", "Could not find user in the database.")
        return

    user_id = user.get("id")
    if not user_id:
        messagebox.showerror("User Error", "User ID is not available.")
        return

    conn = get_db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        
        # Check if the segment belongs to the current user
        cursor.execute("SELECT user_id FROM segment WHERE id = %s", (segment_id,))
        segment = cursor.fetchone()
        
        if not segment:
            messagebox.showerror("Not Found", f"No segment found with ID {segment_id}.")
            return

        #if segment[1] != user_id:
        #    messagebox.showerror("Permission Denied", "You are not authorized to delete this segment.")
        #    return

        # Delete the segment
        cursor.execute("DELETE FROM segment WHERE id = %s", (segment_id,))
        conn.commit()

        messagebox.showinfo("Success", "Segment deleted successfully!")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not delete segment: {err}")
    finally:
        cursor.close()
        conn.close()

