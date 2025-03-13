"""
This module represents the Controller component of the M-V-C design pattern.

This module contains the Controller class which acts as an intermediary between the Model and the View.

Responsibilites involve:
-  TODO: Add docstring

"""
from Model import Model  # Ensure the filename is lowercase
from View import View
import pandas as pd

class Controller:
    def __init__(self, model, view, dataset_options):
        self.model = model
        self.view = view
        self.dataset_options = dataset_options  
        self.dataset = pd.read_csv("dev/fake_profile_detector_app/production_csv/validation_sample.csv")

    def load_selected_dataset(self, dataset_name):
        """Loads dataset based on user selection from ComboBox."""
        file_path = self.dataset_options.get(dataset_name)  
        
        if not file_path:
            self.view.display_error("Invalid dataset selection.")
            return
        
        try:
            self.dataset = pd.read_csv(file_path)
            self.view.display_message(f"Dataset '{file_path}' loaded successfully.")
        except Exception as e:
            self.view.display_error(f"Error loading dataset: {e}")
        
    
    def handle_classification(self):
            """Classifies the dataset and displays results in the View."""

            if self.dataset is None:
                self.view.display_error("No dataset loaded. Please load a dataset first.")
                return

            results = self.model.evaluate_model(self.dataset)
            self.view.display_results(results)