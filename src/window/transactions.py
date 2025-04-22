import customtkinter as ctk
from datetime import datetime
import mysql.connector
import user_manager
from transaction_manager import add_transaction
import os

transaction_manager = None

def close_transaction_window(window):
    window.withdraw()

def create_transaction_window(parent, refresh_main_window=None):
    global transaction_manager
    if transaction_manager and transaction_manager.winfo_exists():
        transaction_manager.deiconify()
        return

    transaction_manager = ctk.CTkToplevel(parent)
    transaction_manager.title("Add Transaction")
    transaction_manager.geometry("400x500")
    transaction_manager.minsize(300, 200)
    transaction_manager.resizable(False, False)
    icon_path = os.path.join(os.path.dirname(__file__), '..', "assets", "icons", "main.ico")
    transaction_manager.iconbitmap(icon_path)

    transaction_manager.grid_rowconfigure(0, weight=1)
    transaction_manager.grid_columnconfigure(0, weight=1)

    main_frame = ctk.CTkFrame(transaction_manager, corner_radius=5)
    main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

    amount_label = ctk.CTkLabel(main_frame, text="Amount:")
    amount_label.pack(anchor="w", pady=(5, 0))
    amount_entry = ctk.CTkEntry(main_frame)
    amount_entry.pack(fill="x", padx=5, pady=5)

    source_label = ctk.CTkLabel(main_frame, text="Source:")
    source_label.pack(anchor="w", pady=(5, 0))
    source_entry = ctk.CTkEntry(main_frame)
    source_entry.pack(fill="x", padx=5, pady=5)

    date_label = ctk.CTkLabel(main_frame, text="Date (YYYY-MM-DD HH:MM:SS):")
    date_label.pack(anchor="w", pady=(5, 0))
    date_entry = ctk.CTkEntry(main_frame)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    date_entry.pack(fill="x", padx=5, pady=5)

    def on_add():
        success = add_transaction(
            user_id=user_manager.get_user_id(),
            amount=amount_entry.get(),
            source=source_entry.get(),
            date=date_entry.get()
        )
        if success:
            close_transaction_window(transaction_manager)
            if refresh_main_window:
                refresh_main_window()

    add_button = ctk.CTkButton(main_frame, text="Add Transaction", command=on_add)
    add_button.pack(pady=10)

    close_button = ctk.CTkButton(main_frame, text="Close", command=lambda: close_transaction_window(transaction_manager))
    close_button.pack(pady=5)

    transaction_manager.protocol("WM_DELETE_WINDOW", lambda: close_transaction_window(transaction_manager))
    transaction_manager.lift()
    return transaction_manager

