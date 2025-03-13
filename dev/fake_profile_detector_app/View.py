"""
This module represents the View component of the M-V-C design pattern.

This module contains the View class which displays the data from the Model to the user and sends user inputs to the Controller. 

Responsibilites involve:
- TODO: Add docstring
- TODO: cite tkinter geeks for geeks 
- TODO: visualise attnetion scores: If the model misclassifies something, we can debug by checking which words it focused on.



"""

import tkinter as tk
from tkinter import messagebox
from Controller import Controller
import shap
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io

class View:

    def __init__(self, root):
        self.root = root
        self.root.title("Human Or Bot Profile Detector")

        # Initialize the Controller with the model and tokenizer names
        model_path = "dev/roberta_round1"
        self.controller = Controller(model_path, "roberta-base")

        self.classification_pg_frame = tk.Frame(self.root)
        self.additional_info_pg_frame = tk.Frame(self.root)

        self.create_classification_page()
        self.create_additional_info_page()

        self.show_frame(self.classification_pg_frame)
    
    def show_frame(self, frame):
        for f in (self.classification_pg_frame, self.additional_info_pg_frame):
            f.pack_forget()  
        frame.pack(fill="both", expand=True) 

    def create_classification_page(self):
        # Input label
        label = tk.Label(self.classification_pg_frame, text="Enter Text To Receive Classification:")
        label.pack(pady=5)

        # Text entry box for user input
        self.text_entry = tk.Entry(self.classification_pg_frame, width=40)
        self.text_entry.pack(pady=5)

        # Label to display the result
        self.result_label = tk.Label(self.classification_pg_frame, text="Prediction: ", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.probability_label = tk.Label(self.classification_pg_frame, text="Probability: ", font=("Helvetica", 12))
        self.probability_label.pack(pady=5)

        # Button to trigger classification
        self.classify_button = tk.Button(self.classification_pg_frame, text="Classify", command=self.handle_classification)
        self.classify_button.pack(pady=10)

        self.additional_info_button = tk.Button(
            self.classification_pg_frame, text="Additional Information",
            command=lambda: self.show_frame(self.additional_info_pg_frame)
        )
        self.additional_info_button.pack(pady=10)
        self.additional_info_button.pack_forget()  # Hide initially

    
    def create_additional_info_page(self):
        label = tk.Label(self.additional_info_pg_frame, text="Additional Information Page")
        label.pack(pady=10)

        shap_image = self.handle_shap()
        if shap_image is not None:
                # Convert the PIL image to a Tkinter-compatible image
                tk_image = ImageTk.PhotoImage(shap_image)
                
                # Create a label to display the image
                img_label = tk.Label(self.additional_info_pg_frame, image=tk_image)
                img_label.image = tk_image  # Keep a reference to avoid garbage collection
                img_label.pack(pady=10)

        back_button = tk.Button(self.additional_info_pg_frame, text="Back to Classification",
                                command=lambda: self.show_frame(self.classification_pg_frame))
        back_button.pack(pady=10)
        self.show_frame(self.additional_info_pg_frame)

    def handle_classification(self):
        # Get the input text from the entry box
        input_text = self.text_entry.get()

        try:
            # Get the prediction and probability from the controller
            prediction, probability = self.controller.handle_classification(input_text)

            # Update the result labels
            self.result_label.config(text=f"Prediction: {prediction}")
            self.probability_label.config(text=f"Probability: {probability}%")

            self.classify_button.pack_forget()
            self.additional_info_button.pack()
            self.new_classification_button = tk.Button(self.classification_pg_frame, text="New Classification",
                                                       command=lambda: self.reset_classification_page())
            self.new_classification_button.pack(pady=10)

        except Exception as e:
            # If any error occurs, show a message box with the error
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def reset_classification_page(self):

        self.text_entry.delete(0, tk.END)
        self.result_label.config(text="Prediction: ")
        self.probability_label.config(text="Probability: ")
        self.classify_button.pack(pady=10)
        self.additional_info_button.pack_forget()
        self.new_classification_button.pack_forget()
        self.show_frame(self.classification_pg_frame)


    def handle_shap(self):
        input_text = self.text_entry.get()

        return self.controller.handle_shap(input_text)


