import tkinter as tk
from PIL import Image, ImageTk

def on_icon_click(event):
    """Callback function when the floating icon is clicked."""
    root.withdraw()  # Hide the icon window
    open_new_window()

def open_new_window():
    """Function to open a small window after the icon is clicked."""
    new_window = tk.Toplevel(root)
    new_window.title("Small Window")
    new_window.geometry("200x150")  # Set the size of the new window
    new_window.attributes("-topmost", True)  # Keep the new window on top

    # Add content to the new window
    label = tk.Label(new_window, text="This is a small window!")
    label.pack(pady=20)

    # Button to close the small window and show the icon again
    close_button = tk.Button(new_window, text="Close", command=lambda: close_new_window(new_window))
    close_button.pack(pady=10)

    # Handle window close using window controls
    new_window.protocol("WM_DELETE_WINDOW", lambda: close_new_window(new_window))

def close_new_window(new_window):
    """Function to close the small window and show the icon again."""
    new_window.destroy()  # Close the small window
    root.deiconify()  # Show the floating icon again

def on_drag_start(event):
    """Capture the initial position when the drag starts."""
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
