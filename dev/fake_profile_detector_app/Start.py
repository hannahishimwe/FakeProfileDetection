"""
This is the main entry for the Fake Profile Detector application.

This initialises and runs the Tkinter app

"""

import tkinter as tk
from tkinter import ttk
from View import View  
from Model import Model
from Controller import Controller
import os


class MainApp:

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

    theme_path = os.path.join(BASE_DIR, "themes", "forest-dark.tcl")
    csv_path = os.path.join(BASE_DIR, "production_csv", "validation_sample.csv")

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Experimenting the Suitability of Pre-trained Transformers for Fake Profile Detection")
        self.root.tk.call("source", self.theme_path) 
        ttk.Style().theme_use("forest-dark")  
        self.root.geometry("1000x350")


        self.dataset_options = {
            "Twitter Dataset": self.csv_path,
        }

        self.model = Model()
        self.controller = Controller(self.model, None, self.dataset_options)
        self.view = View(self.root, self.controller, self.dataset_options)
        self.controller.view = self.view  

        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()  

