"""
This module represents the View component of the M-V-C design pattern.

This module contains the View class which displays the data from the Model to the user and sends user inputs to the Controller. 

Responsibilites involve:
- TODO: Add docstring
- TODO: cite tkinter geeks for geeks 
- TODO: visualise attnetion scores: If the model misclassifies something, we can debug by checking which words it focused on.



"""
import tkinter as tk
from tkinter import ttk

class View:
    def __init__(self, root, controller, dataset_options):

        # Initialising root and controller objects

        self.controller = controller
        self.root = root

        self.root.geometry("600x400")
        self.root.configure(padx=20, pady=20)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # CREATE MAIN FRAME

        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True)


        self.label = ttk.Label(main_frame, text="Select Dataset:", font=("Arial", 14))
        self.label.pack(pady=5)


        self.dataset_combobox = ttk.Combobox(main_frame, values=list(dataset_options.keys()), state="readonly")
        self.dataset_combobox.pack(pady=5)
        self.root.update_idletasks()
        # self.dataset_combobox.bind("<<ComboboxSelected>>", self.on_dataset_selected) -- commented for efficiency, uncomment if using multiple datasets


        self.classify_button = ttk.Button(main_frame, text="Classify Dataset", command=self.start_classification)
        self.classify_button.pack(pady=10)


        self.new_classification_button = ttk.Button(root, text="New Classification", command=self.reset_ui)
        self.new_classification_button.pack_forget()


        self.status_label = ttk.Label(main_frame, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)


        self.results_frame = ttk.Frame(main_frame, padding=10, style="Results.TFrame")
        self.results_frame.pack(pady=5, fill="x")
        self.results_frame.pack_forget() 

        # Display classification results
        metrics = ["Predicted Humans:", "Predicted Bots:", "Actual Humans:", "Actual Bots:", "Accuracy:", "Precision:", "Recall:", "F1-score:"]
        self.metric_labels = []
        self.value_labels = []

        for i, metric in enumerate(metrics):
            label = ttk.Label(self.results_frame, text=metric, font=("Arial", 12), anchor="w", foreground="white")
            label.grid(row=i, column=0, sticky="w", padx=(10, 5))  # Left-aligned
            self.metric_labels.append(label)

            value_label = ttk.Label(self.results_frame, text="--", font=("Arial", 12), anchor="e", foreground="white")
            value_label.grid(row=i, column=1, sticky="e", padx=(5, 10))  # Right-aligned
            self.value_labels.append(value_label)

        # Apply custom styling
        self.style = ttk.Style()
        self.style.configure("Results.TFrame", background="grey20")
        self.root.update_idletasks()

    def start_classification(self):
        """Updates UI while classification is running."""
        self.status_label.config(text="Classifying In Progress...", foreground="orange")
        self.root.update_idletasks() 
        self.controller.handle_classification()
        self.status_label.pack_forget()
        self.classify_button.pack_forget()
        self.new_classification_button.pack(pady=5)  
        self.root.update_idletasks()

    def on_dataset_selected(self, event):
        """Handles dataset selection from ComboBox."""
        selected_dataset = self.dataset_combobox.get()
        self.controller.load_selected_dataset(selected_dataset)
        self.dataset_combobox.update_idletasks()

    def display_message(self, message):
        """Displays a success message."""
        self.status_label.config(text=message, foreground="green")

    def display_error(self, error_message):
        """Displays an error message."""
        self.status_label.config(text=error_message, foreground="red")
    
    def reset_ui(self):
        """Resets the UI to its initial state."""
        self.results_frame.pack_forget()  
        self.new_classification_button.pack_forget()  
        self.classify_button.pack(pady=10)
        self.status_label.config(text="")
        self.status_label.pack(pady=5)
        self.root.update_idletasks()

    def display_results(self, results):
        """Formats and displays the classification results in a grey box with aligned text."""
        values = [
        results["Predicted Humans"],
        results["Predicted Bots"],
        results["Actual Humans"],
        results["Actual Bots"],
        f"{results['Accuracy']:.4f}",
        f"{results['Precision']:.4f}",
        f"{results['Recall']:.4f}",
        f"{results['F1-score']:.4f}"
        ]
    
        for label, value in zip(self.value_labels, values):
            label.config(text=value)

        self.results_frame.pack(pady=10, fill="x")