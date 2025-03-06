import tkinter as tk
from View import View  # Import TkinterApp class

class MainApp:

    def __init__(self):
        """Initialize and run the Tkinter app."""
        self.root = tk.Tk()  # Create the root Tkinter window
        self.root.geometry("700x350")
        self.app = View(self.root)  # Initialize the TkinterApp with root window
        self.root.mainloop()  # Run the Tkinter main loop

# This will only run when the file is executed directly
if __name__ == "__main__":
    app = MainApp()  # Instantiate the MainApp class to start the GUI



"""
Landing Page with explanation of the app
Button that sends through extra visualisation of the data
"""