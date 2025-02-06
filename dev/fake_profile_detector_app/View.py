"""
This module represents the View component of the M-V-C design pattern.

This module contains the View class which displays the data from the Model to the user and sends user inputs to the Controller. 

Responsibilites involve:
- TODO: Add docstring


"""

import tkinter as tk
from tkinter import messagebox
from Controller import Controller

class View:

    def __init__(self, root):
        self.root = root
        self.root.title("Human Or Bot Profile Detector")

        # Initialize the Controller with the model and tokenizer names
        self.controller = Controller("distilbert-base-uncased", "distilbert-base-uncased")

        # Create the UI elements
        self.create_widgets()

    def create_widgets(self):
        # Input label
        self.input_label = tk.Label(self.root, text="Enter Text To Receive Classification:")
        self.input_label.pack(pady=5)

        # Text entry box for user input
        self.text_entry = tk.Entry(self.root, width=40)
        self.text_entry.pack(pady=5)

        # Button to trigger classification
        self.classify_button = tk.Button(self.root, text="Classify", command=self.handle_classification)
        self.classify_button.pack(pady=10)

        # Label to display the result
        self.result_label = tk.Label(self.root, text="Prediction: ", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.probability_label = tk.Label(self.root, text="Probability: ", font=("Helvetica", 12))
        self.probability_label.pack(pady=5)

    def handle_classification(self):
        # Get the input text from the entry box
        input_text = self.text_entry.get()

        try:
            # Get the prediction and probability from the controller
            prediction, probability = self.controller.handle_input(input_text)

            # Update the result labels
            self.result_label.config(text=f"Prediction: {prediction}")
            self.probability_label.config(text=f"Probability: {probability}%")

        except Exception as e:
            # If any error occurs, show a message box with the error
            messagebox.showerror("Error", f"An error occurred: {e}")



