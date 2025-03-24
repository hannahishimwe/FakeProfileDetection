"""
This module represents the Controller component of the M-V-C design pattern.

This module contains the Controller class which acts as an intermediary between the Model and the View.

Responsibilites involve:

- loading the dataset based on user selection;
- handling the classification of the dataset and displaying the results in the View.

"""
import pandas as pd
import os

class Controller:
    def __init__(self, model, view, dataset_options):
        self.model = model
        self.view = view
        self.dataset_options = dataset_options  
        #Pre load for efficiency for the demonstration
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        CSV_PATH = os.path.join(BASE_DIR, "production_csv", "validation_sample.csv") 
        self.dataset = pd.read_csv(CSV_PATH)

    # To be used if other datasets are to be loaded
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