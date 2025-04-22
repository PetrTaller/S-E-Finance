import sys
import os
import customtkinter as ctk
sys.path.append(os.path.join(os.path.dirname(__file__), 'window'))
import login

app = ctk.CTk()
app.title("")
app.geometry("1300x500")
app.minsize(1000, 500)
app.resizable(True, True)
icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "main.ico")
app.iconbitmap(icon_path)

content_frame = ctk.CTkFrame(app)
content_frame.pack(fill="both", expand=True, padx=0, pady=0)

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

if __name__ == "__main__":
    if login.check_for_session():
        login.create_confirmation_window(content_frame, clear_content)
    else:
        login.create_login_window(content_frame, clear_content)

app.mainloop()
