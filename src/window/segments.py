import re
import customtkinter as ctk
from tkinter import colorchooser
from tkinter import messagebox
from segment_manager import fetch_segments
from segment_manager import update_segment
from segment_manager import fetch_all_segments_flat
from segment_manager import add_segment
from segment_manager import delete_segment
import os

segments_manager = None
segments_data = {}
selected_button = None  # Track the last selected button

def close(window):
    global selected_button
    if selected_button:
        selected_button.configure(fg_color="transparent")  # Deselect the current button
    selected_button = None  # Reset the selected button
    window.withdraw()  # Hide the window instead of destroying it

def create_segment_window(content_frame, refresh_main_window=None):
    global segments_manager

    if segments_manager is not None and segments_manager.winfo_exists():
        segments_manager.lift()  # Bring the window to the front if it's already open
        segments_manager.deiconify()  # Unhide the window if it's hidden
        return

    # Create a new window if it doesn't exist
    segments_manager = ctk.CTkToplevel(content_frame)
    segments_manager.title("Segment Manager")
    segments_manager.geometry("1000x500")
    icon_path = os.path.join(os.path.dirname(__file__),"..", "assets", "icons", "main.ico")
    segments_manager.iconbitmap(icon_path)
    segments_manager.minsize(500, 250)
    segments_manager.resizable(True, True)
    segments_manager.lift()

    segments_manager.grid_rowconfigure(0, weight=1)
    segments_manager.grid_rowconfigure(1, weight=0)
    segments_manager.grid_columnconfigure(0, weight=1)
    segments_manager.grid_columnconfigure(1, weight=5)

    scrollable_frame = ctk.CTkScrollableFrame(segments_manager, corner_radius=5)
    scrollable_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

    right_frame = ctk.CTkFrame(segments_manager, corner_radius=5)
    right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nswe")

    bottom_section = ctk.CTkFrame(segments_manager, corner_radius=5)
    bottom_section.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    close_button = ctk.CTkButton(bottom_section, text="Close", corner_radius=5, command=lambda: close(segments_manager))
    close_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    add_segment_button = ctk.CTkButton(bottom_section, text="Add Segment", corner_radius=5, command=lambda: add_new_segment(scrollable_frame, right_frame))
    add_segment_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")
    
    def close(window):
        global selected_button
        if selected_button:
            selected_button.configure(fg_color="transparent")  # Deselect the current button
        selected_button = None  # Reset the selected button
        window.withdraw()  # Hide the window instead of destroying it
        if refresh_main_window:
            refresh_main_window()  # 🔁 Refresh main window when this closes

    segments_manager.protocol("WM_DELETE_WINDOW", lambda: close(segments_manager))  # Handle the window close event
    load_segments(scrollable_frame, right_frame)
    segments_manager.lift()
def add_new_segment(scrollable_frame, right_frame):
    def submit_new_segment():
        # Retrieve user inputs
        name = segment_name_entry.get()
        color = segment_color_entry.get()
        percentage = percentage_entry.get()
        parent_id = parent_segment_var.get()  # Get the selected parent ID from the dropdown
        if parent_id != "None" :
            parent_id = parent_id[0]
        # Validate inputs
        if not name:
            messagebox.showerror("Input Error", "Name cannot be empty.")
            return
        if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
            messagebox.showerror("Input Error", "Color must be a valid hex code (e.g., #FFFFFF).")
            return
        if not percentage.isdigit() or not 0 <= int(percentage) <= 100:
            messagebox.showerror("Input Error", "Percentage must be a number between 0 and 100.")
            return

        # Add the segment or subsegment to the database
        add_segment(name, color, int(percentage), parent_id if parent_id != "None" else None)

        # Close the modal and reload the segments
        modal.destroy()
        load_segments(scrollable_frame, right_frame)

    # Create a modal window for input
    modal = ctk.CTkToplevel()
    modal.title("Add New Segment")
    modal.geometry("400x500")
    modal.grab_set()  # Make the modal window modal

    # Name Input
    name_label = ctk.CTkLabel(modal, text="Name:")
    name_label.pack(padx=10, pady=5, anchor="w")
    segment_name_entry = ctk.CTkEntry(modal)
    segment_name_entry.pack(padx=10, pady=5, fill="x")

    # Color Input
    color_label = ctk.CTkLabel(modal, text="Color (Hex):")
    color_label.pack(padx=10, pady=5, anchor="w")
    segment_color_entry = ctk.CTkEntry(modal)
    segment_color_entry.insert(0, "#FFFFFF")  # Default color
    segment_color_entry.pack(padx=10, pady=5, fill="x")

    # Percentage Input
    percentage_label = ctk.CTkLabel(modal, text="Percentage:")
    percentage_label.pack(padx=10, pady=5, anchor="w")
    percentage_entry = ctk.CTkEntry(modal)
    percentage_entry.pack(padx=10, pady=5, fill="x")

    # Parent Segment Dropdown
    parent_label = ctk.CTkLabel(modal, text="Parent Segment:")
    parent_label.pack(padx=10, pady=5, anchor="w")

    # Fetch all segments for the dropdown
    segments_flat_list = fetch_all_segments_flat()
    parent_segment_var = ctk.StringVar(value="None")
    parent_dropdown = ctk.CTkComboBox(
        modal,
        values=["None"] + [f"{segment['id']}: {segment['name']}" for segment in segments_flat_list],
        variable=parent_segment_var
    )
    parent_dropdown.pack(padx=10, pady=5, fill="x")

    # Submit Button
    submit_button = ctk.CTkButton(modal, text="Add Segment", command=submit_new_segment)
    submit_button.pack(pady=20)

    # Cancel Button
    cancel_button = ctk.CTkButton(modal, text="Cancel", command=modal.destroy)
    cancel_button.pack(pady=10)


def load_segments(scrollable_frame, right_frame):
    global segments_data

    segments_data = fetch_segments()
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    def create_buttons_for_segment(segment, indent=0):
        # Create button for the segment with proper indentation on the left
        segment_button = ctk.CTkButton(
            scrollable_frame,
            text=segment["name"],
            fg_color="transparent",
            border_width=0.1,
            hover_color="#424242",
            corner_radius=0,
            anchor="w"
        )

        # Apply indentation only on the left side while button fills remaining width
        segment_button.pack(padx=(indent * 15, 5), pady=5, fill="x")
        # Rebind the click event to the new button
        segment_button.configure(command=lambda s=segment, b=segment_button: on_segment_click(s, right_frame, b))

        # If the segment has subsegments, recursively create buttons for them
        if "subsegments" in segment: 
            for subsegment in segment["subsegments"]:
                create_buttons_for_segment(subsegment, indent=indent + 1)

    # Create buttons for the top-level segments
    for segment_id, segment in segments_data.items():
        create_buttons_for_segment(segment)

    # Reset any selection (deselect all buttons)
    global selected_button
    selected_button = None

def on_segment_click(segment, right_frame, button):
    global selected_button

    # If there's a previously selected button, reset it
    if selected_button and selected_button != button:
        selected_button.configure(fg_color="transparent")  # Deselect the previous button

    # Update the selected button's color
    if button.winfo_exists():  # Check if the button exists before modifying it
        button.configure(fg_color="#545454")  # Select the new button
        selected_button = button  # Update the selected_button reference

    # Clear right frame and load segment details
    for widget in right_frame.winfo_children():
        widget.destroy()

    segment_name_label = ctk.CTkLabel(right_frame, text="Name:")
    segment_name_label.pack(padx=5, pady=5, anchor="w")
    
    segment_name_entry = ctk.CTkEntry(right_frame)
    segment_name_entry.insert(0, segment["name"])
    segment_name_entry.pack(padx=5, pady=5, anchor="w")

    color_label = ctk.CTkLabel(right_frame, text="Color:")
    color_label.pack(padx=5, pady=5, anchor="w")

    # Create a button to open the color picker
    def open_color_picker():
        color_code = colorchooser.askcolor(initialcolor=segment["color"])[1]  # returns (rgb, hex)
        if color_code:  # If a color was chosen
            color_entry.delete(0, "end")
            color_entry.insert(0, color_code)
            color_display.configure(bg=color_code)  # Update color display box

    color_picker_button = ctk.CTkButton(right_frame, text="Choose Color", command=open_color_picker)
    color_picker_button.pack(padx=5, pady=5, anchor="w")

    color_entry = ctk.CTkEntry(right_frame)
    color_entry.insert(0, segment["color"])
    color_entry.pack(padx=5, pady=5, anchor="w")

    # Create a label to show the selected color visually
    color_display = ctk.CTkLabel(right_frame, text=" ", width=20, height=20, corner_radius=5, bg_color=segment["color"])
    color_display.pack(padx=5, pady=5, anchor="w")

    percentage_label = ctk.CTkLabel(right_frame, text="Percentage:")
    percentage_label.pack(padx=5, pady=5, anchor="w")

    percentage_entry = ctk.CTkEntry(right_frame)
    # Ensure that the percentage is displayed as a whole number
    percentage_entry.insert(0, str(int(segment["percentage"])))  # Cast to int to ensure it's a whole number
    percentage_entry.pack(padx=5, pady=5, anchor="w")

    update_button = ctk.CTkButton(right_frame, text="Update Segment", command=lambda: update_segments(segment, segment_name_entry.get(), color_entry.get(), percentage_entry.get()))
    update_button.pack(padx=5, pady=5)

    delete_button = ctk.CTkButton(right_frame, text="Delete Segment", command=lambda: delete_segment(segment["id"]))
    delete_button.pack(padx=5, pady=5)

    def update_segments(segment, name, color, percentage):
        # Validate that the percentage is a valid number and is a whole number
        if not percentage.isdigit():  # Check if the percentage is a valid integer
            print("Invalid input: Percentage must be a whole number.")
            return  # Don't proceed if the percentage is not a valid number

        # Validate the color input to be a valid hex code (e.g., #FFFFFF)
        if not re.match(r'^#[0-9A-Fa-f]{6}$', color):  # Check if the color is a valid hex code
            print("Invalid color: Please enter a valid hex color code (e.g., #FFFFFF).")
            return  # Don't proceed if the color is not a valid hex code

        # Convert percentage to an integer
        percentage = int(percentage)

        # Call the update_segment function with validated input
        update_segment(segment["id"], name, color, percentage)

        # Re-load the segments after updating
        scrollable_frame = ctk.CTkScrollableFrame(segments_manager, corner_radius=5)
        scrollable_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")
        load_segments(scrollable_frame, right_frame)

            