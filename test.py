import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import scrolledtext, ttk, simpledialog
import pyperclip
import keyboard  # For adding keyboard shortcuts

# Clipboard slots dictionary to store the copied content
clipboard_slots = {}

# Clipboard history list to store multiple clipboard entries
clipboard_history = []

# Maximum number of history entries
MAX_HISTORY_SIZE = 10

def on_icon_click(event):
    """Callback function when the floating icon is clicked."""
    root.withdraw()  # Hide the icon window
    open_main_window()

def open_main_window():
    """Function to open the clipboard manager window."""
    main_window = tk.Toplevel(root)
    main_window.title("Clipboard Manager")
    main_window.geometry("500x500")  # Adjust size to accommodate future features
    main_window.attributes("-topmost", True)  # Keep the window on top

    # Frame for the copied slots
    frame = ttk.Frame(main_window, padding="10")
    frame.pack(expand=True, fill='both', side='top', padx=10, pady=10)

    # Frame for logging actions
    log_frame = tk.Frame(main_window)
    log_frame.pack(padx=10, pady=10)

    log_text = scrolledtext.ScrolledText(log_frame, state='disabled', height=10, wrap='word')
    log_text.pack(fill='both', expand=True)

    # Dropdown to select clipboard slots
    dropdown_var = tk.StringVar()
    dropdown = ttk.Combobox(frame, textvariable=dropdown_var, state="readonly")
    dropdown.pack(fill='x', pady=5)

    def update_dropdown():
        """Update dropdown with the available clipboard slots."""
        filtered_slots = [slot for slot, content in clipboard_slots.items() if content] 
        dropdown['values'] = filtered_slots  # Update dropdown values
        dropdown.set('')

    def log_action(message):
        """Log actions in the log area."""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        log_text.config(state='normal')
        log_text.insert(tk.END, f"[{current_time}] {message}\n")
        log_text.config(state='disabled')
        log_text.yview(tk.END)

    def handle_copy(slot):
        """Handle copy action for a specific slot."""
        content = pyperclip.paste()
        clipboard_slots[slot] = content
        log_action(f"Copied to slot '{slot}': {content}")
        add_to_history(content)  # Add to clipboard history
        update_dropdown()  # Update the dropdown values
        display_slots()  # Refresh slot display
        display_history()  # Refresh history display

    def handle_paste():
        """Handle paste action from the selected dropdown slot."""
        slot = dropdown.get()
        if slot and clipboard_slots.get(slot):
            pyperclip.copy(clipboard_slots[slot])
            log_action(f"Pasted from slot '{slot}': {clipboard_slots[slot]}")
        else:
            log_action(f"No content to paste from slot '{slot}'")

    def handle_cut(slot):
        """Handle cut action for a specific slot."""
        content = pyperclip.paste()
        clipboard_slots[slot] = content
        log_action(f"Cut to slot '{slot}': {content}")
        pyperclip.copy('')  # Clear the clipboard
        update_dropdown()
        add_to_history(content)  # Add to clipboard history
        display_slots()  # Refresh slot display
        display_history()  # Refresh history display

    def update_shortcut():
        """Prompt to update a shortcut (copy, paste, or cut)."""
        slot = simpledialog.askstring("Input", "Enter the identifier for the new slot:")
        if slot in clipboard_slots:
            messagebox.showerror("Invalid Slot", "This slot identifier already exists.")
            return

        shortcut_type = simpledialog.askstring("Input", f"Enter new shortcut for slot {slot} (copy/paste/cut):")
        if shortcut_type:
            log_action(f"Updated shortcut for slot {slot}: {shortcut_type}")
            update_dropdown()

    def setup_shortcuts():
        """Setup keyboard shortcuts for copying, cutting, and pasting slots."""
        # Add hotkeys for copy, cut, and paste for each slot number (1-9)
        for slot_num in range(1, 10):
            slot_key = f"slot{slot_num}"
            # Copy to a specific slot: Ctrl+Shift+C+SlotNumber
            keyboard.add_hotkey(f'ctrl+shift+c+{slot_num}', lambda s=slot_key: handle_copy(s))
            # Cut to a specific slot: Ctrl+Shift+X+SlotNumber
            keyboard.add_hotkey(f'ctrl+shift+x+{slot_num}', lambda s=slot_key: handle_cut(s))
            # Paste from a specific slot: Ctrl+Shift+V+SlotNumber
            keyboard.add_hotkey(f'ctrl+shift+v+{slot_num}', lambda: handle_paste())

    # History Functions
    def add_to_history(content):
        """Add clipboard content to the history and maintain size."""
        if len(clipboard_history) >= MAX_HISTORY_SIZE:
            clipboard_history.pop(0)  # Remove the oldest entry
        clipboard_history.append(content)
        log_action(f"Added to history: {content}")

    def display_history():
        """Display clipboard history."""
        history_frame = tk.Frame(main_window)
        history_frame.pack(pady=5)
        for idx, entry in enumerate(clipboard_history):
            entry_label = tk.Label(history_frame, text=f"{idx + 1}: {entry[:30]}{'...' if len(entry) > 30 else ''}")
            entry_label.pack(anchor='w', padx=5, pady=2)

    def display_slots():
        """Display clipboard slots with edit and delete options."""
        for widget in frame.winfo_children():
            widget.destroy()  # Clear the frame to refresh content

        for slot, content in clipboard_slots.items():
            if content:
                # Display partial content (first 30 characters)
                partial_content = content[:30] + '...' if len(content) > 30 else content
                slot_label = tk.Label(frame, text=f"{slot}: {partial_content}")
                slot_label.pack(anchor='w', padx=5, pady=2)

                # Edit button
                edit_button = tk.Button(frame, text="Edit", command=lambda s=slot: edit_slot(s))
                edit_button.pack(anchor='w', padx=5, pady=2)

                # Delete button
                delete_button = tk.Button(frame, text="Delete", command=lambda s=slot: delete_slot(s))
                delete_button.pack(anchor='w', padx=5, pady=2)

    def edit_slot(slot):
        """Allow user to edit the content of a slot."""
        new_content = simpledialog.askstring("Edit Slot", f"Edit content for slot '{slot}':", initialvalue=clipboard_slots[slot])
        if new_content is not None:
            clipboard_slots[slot] = new_content
            log_action(f"Slot '{slot}' edited.")
            display_slots()  # Refresh the display after edit

    def delete_slot(slot):
        """Delete the content of a specific slot."""
        if messagebox.askyesno("Delete Slot", f"Are you sure you want to delete slot '{slot}'?"):
            clipboard_slots.pop(slot, None)
            log_action(f"Slot '{slot}' deleted.")
            update_dropdown()
            display_slots()  # Refresh the display after deletion

    # Log some actions for now
    log_action("Clipboard Manager Opened")

    # Display buttons for copy, cut, paste, and slot management
    ttk.Button(frame, text="Copy to Slot 1", command=lambda: handle_copy("slot1")).pack(pady=5)
    ttk.Button(frame, text="Cut to Slot 2", command=lambda: handle_cut("slot2")).pack(pady=5)
    ttk.Button(frame, text="Paste from Selected Slot", command=handle_paste).pack(pady=5)
    ttk.Button(frame, text="Update Shortcut", command=update_shortcut).pack(pady=5)

    # Button to close the clipboard manager and return to the floating icon
    close_button = tk.Button(main_window, text="Close", command=lambda: close_main_window(main_window))
    close_button.pack(pady=10)

    main_window.protocol("WM_DELETE_WINDOW", lambda: close_main_window(main_window))

    update_dropdown()  # Initialize the dropdown values
    setup_shortcuts()  # Setup keyboard shortcuts for clipboard operations
    display_slots()  # Display the clipboard slots
    display_history()  # Display the clipboard history

def close_main_window(main_window):
    """Close the main window and return to the floating icon."""
    main_window.destroy()  # Close the clipboard window
    root.deiconify()  # Show the floating icon again

def on_drag_start(event):
    """Capture the initial position when dragging starts."""
    event.widget._drag_data = {"x": event.x, "y": event.y}

def on_drag_motion(event):
    """Handle the movement while dragging."""
    x = root.winfo_x() + event.x - event.widget._drag_data["x"]
    y = root.winfo_y() + event.y - event.widget._drag_data["y"]
    root.geometry(f"+{x}+{y}")

def on_hover(event):
    """Show the close/open buttons when hovered."""
    close_button.place(relx=0.7, rely=0.0)  # Position top-right of the icon

def on_leave(event):
    """Hide the close/open buttons when the mouse leaves."""
    close_button.place_forget()  # Hide the button

def close_icon():
    """Function to close the floating icon."""
    root.quit()

def setup_floating_icon():
    global root, close_button
    root = tk.Tk()
    root.title("Floating Icon")
    root.overrideredirect(True)  # Remove window decorations
    root.attributes("-topmost", True)  # Keep it on top of other windows

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Default position: bottom-right corner, below the close button
    window_width = 50
    window_height = 50
    x_offset = screen_width - window_width - 20  # Adjust to place it on the right
    y_offset = screen_height - window_height - 80  # Adjust to place it below the close button

    # Set the position of the window
    root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

    # Load the icon image
    icon_image = Image.open("cert.jpeg")  # Replace with your image path
    icon_image = icon_image.resize((50, 50), Image.Resampling.LANCZOS)  # Resize image to fit window
    icon_photo = ImageTk.PhotoImage(icon_image)

    # Create a label to display the icon
    icon_label = tk.Label(root, image=icon_photo, bg="white")
    icon_label.pack()

    # Bind the click event to the label (triggered when mouse is released)
    icon_label.bind("<ButtonRelease-1>", on_icon_click)

    # Bind dragging events to make the icon movable
    icon_label.bind("<Button-1>", on_drag_start)  # Start dragging on left-click
    icon_label.bind("<B1-Motion>", on_drag_motion)  # Perform drag motion

    # Bind hover events to show/hide the close button
    icon_label.bind("<Enter>", on_hover)  # When mouse enters the icon
    icon_label.bind("<Leave>", on_leave)  # When mouse leaves the icon

    # Create a close button for the hover effect
    close_button = tk.Button(root, text="X", command=close_icon, bg="red", fg="white", bd=0, padx=5, pady=2)
    close_button.place_forget()  # Initially hide the button

    root.mainloop()

if __name__ == "__main__":
    setup_floating_icon()
