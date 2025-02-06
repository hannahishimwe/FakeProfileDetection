"""
This module represents the Controller component of the M-V-C design pattern.

This module contains the Controller class which acts as an intermediary between the Model and the View.

Responsibilites involve:
-  TODO: Add docstring

"""
from Model import Model

class Controller:
    def __init__(self, model_name: str, tokenizer_name: str):

        """TODO: Add docstring"""

        try:
            self.model = Model(model_name, tokenizer_name)
        except Exception as e:
            print(f"Error initializing model: {e}")
            raise

    def handle_input(self, input_text: str):

        """TODO: Add docstring"""

        try:
            if not isinstance(input_text, str) or not input_text.strip():
                raise ValueError("Input text must be a non-empty string.")

            prediction, probability = self.model.get_classification(input_text)

            return prediction, probability
        
        # Return, instead of a prediction, probability tuple, a default error tuple if an exception occurs
        except ValueError as ve:
            return "Input Error", 0.0
        
        except Exception as e:
            return "Unexpected Error", 0.0  