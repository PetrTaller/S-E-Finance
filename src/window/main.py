import customtkinter as ctk 
from segments import create_segment_window
from segments import fetch_segments
from segments import fetch_all_segments_flat
import user_manager
import transaction_manager
import login
#from PIL import Image
from settings import create_settings_window
from transactions import create_transaction_window

import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from io import BytesIO

def create_main_window(content_frame, clear_content):
    clear_content()

    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=3)
    content_frame.grid_columnconfigure(2, weight=1)

    left_sidebar = ctk.CTkFrame(content_frame, corner_radius=5)
    left_sidebar.grid(row=0, column=0, padx=(2.5, 5), pady=5, sticky="nswe")

    profile_image = ctk.CTkLabel(left_sidebar, text="", #image=ctk.CTkImage(light_image=Image.open("assets/images/profile.png"), size=(100, 100))
                                 )
    profile_image.pack(expand=False, fill="both", padx=5, pady=2.5)
    
    profile_name = ctk.CTkLabel(left_sidebar, text=user_manager.get_username())
    profile_name.pack(expand=False, fill="both", padx=5, pady=2.5)
    
    profile_balance = ctk.CTkLabel(left_sidebar, text="Balance: "+str(user_manager.get_balance())+" Kč")
    profile_balance.pack(expand=False, fill="both", padx=5, pady=2.5)
    
    transaction_list = ctk.CTkScrollableFrame(left_sidebar)
    transaction_list.pack(expand=True, fill="both", padx=5, pady=2.5)

    user_transactions = transaction_manager.get_user_transactions()
    if user_transactions:
        for tx in user_transactions:
            # Assuming tx = {"amount": 250, "source": "Groceries", "date": "2025-04-21 10:30:00"}
            tx_frame = ctk.CTkFrame(transaction_list, corner_radius=8)
            tx_frame.pack(fill="x", padx=5, pady=5)

            amount_label = ctk.CTkLabel(tx_frame, text=f"{tx['amount']} Kč", font=ctk.CTkFont(size=16, weight="bold"))
            amount_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))

            source_label = ctk.CTkLabel(tx_frame, text=f"from: {tx['source']}", font=ctk.CTkFont(size=13))
            source_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))

            date_label = ctk.CTkLabel(tx_frame, text=tx['date'], font=ctk.CTkFont(size=10), text_color="gray")
            date_label.grid(row=1, column=1, sticky="e", padx=10, pady=(0, 5))

            # Optional: spacing/column config
            tx_frame.grid_columnconfigure(0, weight=1)
            tx_frame.grid_columnconfigure(1, weight=0)
    else:
        ctk.CTkLabel(transaction_list, text="No transactions yet.", font=ctk.CTkFont(size=13, slant="italic")).pack(pady=10)

    
    transaction_manager_button = ctk.CTkButton(left_sidebar, text="Transactions", command=lambda: transactions_open(content_frame))
    transaction_manager_button.pack(expand=False, fill="both", padx=5, pady=2.5)
    
    button_frame = ctk.CTkFrame(left_sidebar)
    button_frame.pack(side="bottom", expand=False, fill="x", padx=5, pady=2.5)

    settings_button = ctk.CTkButton(button_frame, text="Settings", command=lambda: settings_open(content_frame))
    settings_button.pack(side="left", expand=True, fill="x", padx=0)
    
    logout_button = ctk.CTkButton(button_frame, text="Log-out", corner_radius=5, command=lambda: logout(content_frame, clear_content))
    logout_button.pack(side="right", expand=True, fill="x", padx=0)

    bottom_middle = ctk.CTkFrame(content_frame, corner_radius=5)
    bottom_middle.grid(row=0, column=1, padx=(2.5, 5), pady=5, sticky="nswe")

    right_sidebar = ctk.CTkFrame(content_frame, corner_radius=5)
    right_sidebar.grid(row=0, column=2, padx=(2.5, 5), pady=5, sticky="nswe")

    scrollable_frame = ctk.CTkScrollableFrame(right_sidebar, corner_radius=5)
    scrollable_frame.pack(expand=True, fill="both", padx=5, pady=2.5)
    
    def render_segments(segments, parent_frame, indent=0):
        for segment_id, segment in segments.items():
            # Get the segment's base color (fallback to a default if not provided)
            base_color = segment.get("color", "#888888")

            # Create a container frame which uses a neutral background, but its border reflects the segment color.
            group_frame = ctk.CTkFrame(
                parent_frame,
                fg_color="transparent",         # Neutral background for the frame
                border_color=base_color,     # Border in the segment color
                border_width=2,
                corner_radius=8,
            )
            group_frame.pack(fill="x", padx=indent * 15 + 5, pady=4, ipadx=4, ipady=2)

            # Create the segment button with a neutral color
            segment_button = ctk.CTkButton(
                group_frame,
                text=segment["name"],
                fg_color="transparent",        # Neutral button color
                hover_color="#4d4d4d",       # A slightly darker neutral for hover
                text_color="white",          # Neutral text color; adjust as needed
                anchor="w",
                corner_radius=6,
                height=32,
                command=lambda seg=segment: draw_subsegment_pie(seg)
            )
            segment_button.pack(fill="x", padx=5, pady=2)

            # Render any subsegments recursively, nesting them within the current group frame
            if segment.get("subsegments"):
                child_segments_dict = {s["id"]: s for s in segment["subsegments"]}
                render_segments(child_segments_dict, group_frame, indent=indent + 1)

    # Example usage: fetch_segments() should return a dictionary with the segment structure
    render_segments(fetch_segments(), scrollable_frame)

    add_segment_button = ctk.CTkButton(right_sidebar, text="Configure segments", corner_radius=5, command=lambda: segments_open(content_frame))
    add_segment_button.pack(expand=False, fill="both", padx=5, pady=2.5)
    
    def segments_open(content_frame):
        create_segment_window(content_frame,refresh_main_window=lambda: create_main_window(content_frame, clear_content))

    def settings_open(content_frame):
        create_settings_window(content_frame)
    
    def transactions_open(content_frame):
        create_transaction_window(content_frame,refresh_main_window=lambda: create_main_window(content_frame, clear_content))

    def logout(content_frame, clear_content):
        clear_content()
        login.delete_session(content_frame, clear_content)

    def draw_segment_pie_chart(container, segments):
        # Clear previous widgets in container
        for widget in container.winfo_children():
            widget.destroy()
    
        total_balance = user_manager.get_balance()
    
        labels = [seg["name"] for seg in segments]
        percentages = [float(seg["percentage"]) for seg in segments]
        colors = [seg.get("color", "#888888") for seg in segments]
    
        # Calculate assigned money for each segment
        sizes = [p / 100 * total_balance for p in percentages]
    
        total_assigned_percentage = sum(percentages)
    
        # If segments don't sum to 100%, add "Remaining"
        if total_assigned_percentage < 100:
            remaining_percentage = 100 - total_assigned_percentage
            remaining_money = remaining_percentage / 100 * total_balance
            sizes.append(remaining_money)
            labels.append("Remaining")
            colors.append("#555555")  # neutral color for remaining
    
        # Format labels as actual money
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return f"{val} Kč"
            return my_autopct
    
        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct=make_autopct(sizes),
            textprops=dict(color="white")
        )
        ax.axis('equal')
    
        for autotext in autotexts:
            autotext.set_color("black")
            autotext.set_fontsize(10)
            autotext.set_weight("bold")
    
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        img = Image.open(buf)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 400))
    
        pie_label = ctk.CTkLabel(container, image=ctk_img, text="")
        pie_label.image = ctk_img
        pie_label.pack(pady=10)
    
        plt.close(fig)
    all_segments = list(fetch_segments().values())

    # Show pie in the middle panel
    draw_segment_pie_chart(bottom_middle, all_segments)

    def draw_subsegment_pie(parent_segment):
        subsegments = parent_segment.get("subsegments", [])
        if not subsegments:
            return  # Nothing to draw
    
        total_parent_percentage = float(parent_segment["percentage"])
        total_parent_money = total_parent_percentage / 100 * user_manager.get_balance()
    
        labels = [s["name"] for s in subsegments]
        colors = [s.get("color", "#888888") for s in subsegments]
        percentages = [float(s["percentage"]) for s in subsegments]

        # Calculate actual money for each subsegment
        sizes = [p / 100 * total_parent_money for p in percentages]

        # Add remaining if not 100%
        total_sub_percentage = sum(percentages)
        if total_sub_percentage < 100:
            remaining_percentage = 100 - total_sub_percentage
            remaining_money = remaining_percentage / 100 * total_parent_money
            sizes.append(remaining_money)
            labels.append("Remaining")
            colors.append("#555555")  # dark neutral gray for leftover
    
        for widget in bottom_middle.winfo_children():
            widget.destroy()
    
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return f"{val} Kč"
            return my_autopct
    
        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct=make_autopct(sizes),
            textprops=dict(color="white")
        )
        ax.axis('equal')
    
        for autotext in autotexts:
            autotext.set_color("black")
            autotext.set_fontsize(10)
            autotext.set_weight("bold")
    
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        img = Image.open(buf)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 400))
    
        pie_label = ctk.CTkLabel(bottom_middle, image=ctk_img, text="")
        pie_label.image = ctk_img
        pie_label.pack(pady=(10, 0))
    
        # Add "Back to full pie" button
        back_button = ctk.CTkButton(
            bottom_middle,
            text="⬅ Back to full pie",
            corner_radius=6,
            fg_color="#444",
            hover_color="#333",
            text_color="white",
            command=lambda: draw_segment_pie_chart(bottom_middle, list(fetch_segments().values()))
        )
        back_button.pack(pady=10)
    
        plt.close(fig)