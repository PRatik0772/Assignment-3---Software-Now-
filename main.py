from gui import ImageApp  # Import ImageApp class from gui.py
import tkinter as tk  # Import tkinter here since it is used in main.py

if __name__ == "__main__":
    root = tk.Tk()  # Create the Tkinter root window
    app = ImageApp(root)  # Pass the root window to the ImageApp class
    root.mainloop()  # Start the Tkinter main loop
