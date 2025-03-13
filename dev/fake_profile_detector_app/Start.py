import tkinter as tk
from tkinter import ttk
from View import View  
from Model import Model
from Controller import Controller

class MainApp:

    def __init__(self):
        """Initialize and run the Tkinter app."""
        self.root = tk.Tk()
        self.root.tk.call("source", "dev/fake_profile_detector_app/themes/forest-dark.tcl")  
        ttk.Style().theme_use("forest-dark")  
        self.root.geometry("700x350")

        # Dictionary of dataset names & file paths
        self.dataset_options = {
            "Twitter Dataset": "dev/fake_profile_detector_app/production_csv/validation_sample.csv",
        }

        # Initialize Model
        self.model = Model()

        # Initialize Controller and View
        self.controller = Controller(self.model, None, self.dataset_options)
        self.view = View(self.root, self.controller, self.dataset_options)
        self.controller.view = self.view  # Assign view to controller after creation

        self.root.mainloop()

# This will only run when the file is executed directly
if __name__ == "__main__":
    app = MainApp()  # Instantiate the MainApp class to start the GUI



"""
Landing Page with explanation of the app
Button that sends through extra visualisation of the data
"""