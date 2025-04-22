import main
import customtkinter as ctk
import user_manager
import os

file_path = os.path.join(os.path.dirname(__file__), "saved", "session.json")

def continue_to_app(content_frame, clear_content):
    main.create_main_window(content_frame, clear_content)

def delete_session(content_frame, clear_content):
    user_manager.delete_session()
    create_login_window(content_frame, clear_content)

def create_confirmation_window(content_frame, clear_content):
    clear_content()
    label = ctk.CTkLabel(content_frame, text=f"Hello, Welcome to S&E Finance! are you \"{user_manager.get_username()}\"?", font=("Arial", 18))
    label.pack(pady=20)
    button1 = ctk.CTkButton(content_frame, text="YES", command=lambda:continue_to_app(content_frame, clear_content))
    button1.pack(pady=10)
    button2 = ctk.CTkButton(content_frame, text="NO", command=lambda:delete_session(content_frame, clear_content))
    button2.pack(pady=10)

def check_for_session(file_path=file_path):
    session = user_manager.load_session()
    if session:
        return True
    else:
        return False

def create_login_window(content_frame, clear_content):
    clear_content()
    label = ctk.CTkLabel(content_frame, text=f"Hello, log-in or register into S&E Finance!", font=("Arial", 18))
    label.pack(pady=20)
    
    ctk.CTkLabel(content_frame, text="Username:").pack(pady=5)
    username_entry = ctk.CTkEntry(content_frame)
    username_entry.pack(pady=5)
    
    ctk.CTkLabel(content_frame, text="Password:").pack(pady=5)
    password_entry = ctk.CTkEntry(content_frame, show="*")
    password_entry.pack(pady=5)
    ctk.CTkButton(content_frame, text="Login", command=lambda: user_manager.authenticate_user(username_entry, password_entry, go_to_main, content_frame, clear_content)).pack(pady=10)
    ctk.CTkButton(content_frame, text="Register", command=lambda: user_manager.register_user(username_entry.get(), password_entry.get())).pack(pady=10)
    

def go_to_main(content_frame,clear_content):
    main.create_main_window(content_frame,clear_content)
