"""
This module represents the Model component of the M-V-C design pattern.

This module contains the Model class which is responsible for preparing and processing the business logic of my application.

Responsibilites involve:
- loading the pre-trained model and tokenizer from the model chosen from my experiments;
- responding to the input text data passed in from the user and returning the prediction from the model.

NOTE: uses single responsibility principle in functions

"""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F 
import shap
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

class Model:

    HUMAN_LABEL = 1
    
    def __init__(self, model_name, tokenizer_name):
        """

        Initializes the Model object with the pre-trained model and tokenizer.

        params:

        - self: the Model object
        - model_name (str): the name of the pre-trained model to be loaded
        - tokenizer_name(str): the name of the pre-trained tokenizer to be loaded

        """
        self.outputs = None
        self.inputs = None
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            print(self.model)
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        except Exception as e:
            raise ValueError(f"Error loading model or tokenizer: {e}")

        self.model.eval() 

    def get_classification(self, input_text: str) -> tuple[str, float]:
        """

        Processes input and uses helper functio to return the classification and probability of the prediction
        This will be passed on to the View component.

        params:

        - self: the Model object
        - input_text (str): the text data to be processed and predicted by the model

        returns:

        - tuple:
            - prediction (str): the classification of the prediction
            - probability (float): the probability of the prediction
        
        """

        self.inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

        with torch.no_grad(): 
            self.outputs = self.model(**self.inputs)
        
        prediction = self.get_prediction(self.outputs)
        print(prediction)
        probability = self.get_probability(self.outputs)
        try:
            print(probability)
        except:
            print("error")

        return prediction, probability


    def get_prediction(self, outputs):
        """

        Handles logic to predict the class of the input text data.

        params:

        - self: the Model object
        - outputs (object): the output of the model after processing the input text data

        returns:

        - prediction (str): the most likely classification according to the model (whether it was written by a human or bot)
        
        """
        prediction = "Human" if torch.argmax(outputs.logits, dim=-1).item() == self.HUMAN_LABEL else "Bot"
        
        return prediction
    
    def get_probability(self, outputs): 

        """

        Handles logic to return the probability of the prediction.

        params:

        - self: the Model object
        - outputs (object): the output of the model after processing the input text data

        returns:

        - probability (float): the probability of the prediction, rounded to 2 decimal places
        
        """

        logits = outputs.logits
        probability = F.softmax(logits, dim=-1).max().item()

        # Convert to percentage and round to 2 decimals
        probability = round(probability * 100, 2)

        return probability


    def get_summary_plot(self, input_text: str):
        try:
            print("in get_summary_plot")
            print(self.outputs)
            explainer = shap.Explainer(self.outputs.logits, self.inputs['input_ids'])
            shap_values = explainer(self.inputs['input_ids'])

            # Create the summary plot (do not show it yet)
            plt.figure(figsize=(10, 5))
            shap.summary_plot(shap_values, self.inputs['input_ids'], show=False, plot_type='bar')

            # Save the plot to a BytesIO object
            buf = BytesIO()
            plt.savefig(buf, format='PNG')
            buf.seek(0)
            image = Image.open(buf)
            return image  # Return the image object (not the plot)
        except Exception as e:
            print(f"Error generating SHAP summary plot: {e}")
            return None