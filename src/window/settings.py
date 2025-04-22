import customtkinter as ctk
import os

settings_manager = None

def close_settings(window):
    window.withdraw()

def create_settings_window(parent):
    global settings_manager
    if settings_manager and settings_manager.winfo_exists():
        settings_manager.deiconify()
        return

    settings_manager = ctk.CTkToplevel(parent)
    settings_manager.title("Settings")
    settings_manager.geometry("600x500")
    settings_manager.minsize(400, 400)
    settings_manager.resizable(True, True)
    icon_path = os.path.join(os.path.dirname(__file__), "..","assets", "icons", "main.ico")
    settings_manager.iconbitmap(icon_path)

    settings_manager.grid_rowconfigure(0, weight=1)
    settings_manager.grid_columnconfigure(0, weight=1)

    main_frame = ctk.CTkFrame(settings_manager, corner_radius=5)
    main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

    # General settings section
    general_label = ctk.CTkLabel(main_frame, text="General Settings", font=("Arial", 16, "bold"))
    general_label.pack(pady=10, anchor="w")

    theme_label = ctk.CTkLabel(main_frame, text="Theme:")
    theme_label.pack(anchor="w")
    theme_option = ctk.CTkComboBox(main_frame, values=["Light", "Dark", "System"])
    theme_option.pack(fill="x", padx=5, pady=5)

    currency_label = ctk.CTkLabel(main_frame, text="Currency:")
    currency_label.pack(anchor="w")
    currency_option = ctk.CTkComboBox(main_frame, values=["Czech Crown", "Euro", "British Pound","Japanese Yen"])
    currency_option.pack(fill="x", padx=5, pady=5)

    # Change password section
    password_label = ctk.CTkLabel(main_frame, text="Change Password", font=("Arial", 16, "bold"))
    password_label.pack(pady=10, anchor="w")

    current_password_label = ctk.CTkLabel(main_frame, text="Current Password:")
    current_password_label.pack(anchor="w")
    current_password_entry = ctk.CTkEntry(main_frame, show="*")
    current_password_entry.pack(fill="x", padx=5, pady=5)

    new_password_label = ctk.CTkLabel(main_frame, text="New Password:")
    new_password_label.pack(anchor="w")
    new_password_entry = ctk.CTkEntry(main_frame, show="*")
    new_password_entry.pack(fill="x", padx=5, pady=5)

    confirm_password_label = ctk.CTkLabel(main_frame, text="Confirm New Password:")
    confirm_password_label.pack(anchor="w")
    confirm_password_entry = ctk.CTkEntry(main_frame, show="*")
    confirm_password_entry.pack(fill="x", padx=5, pady=5)

    # Buttons section
    button_frame = ctk.CTkFrame(settings_manager, corner_radius=5)
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    save_button = ctk.CTkButton(button_frame, text="Save", command=lambda: print("Settings saved"))
    save_button.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    close_button = ctk.CTkButton(button_frame, text="Close", command=lambda: close_settings(settings_manager))
    close_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    settings_manager.protocol("WM_DELETE_WINDOW", lambda: close_settings(settings_manager))
    settings_manager.lift()
    return settings_manager
