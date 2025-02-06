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
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
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

        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

        with torch.no_grad(): 
            outputs = self.model(**inputs)
        
        prediction = self.get_prediction(outputs)
        probability = self.get_probability(outputs)

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

        probability = F.softmax(outputs, dim=-1).max().item()
        probability = round(probability * 100, 2)

        return probability


        