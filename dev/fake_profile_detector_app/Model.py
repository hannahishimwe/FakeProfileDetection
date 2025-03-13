"""
This module represents the Model component of the M-V-C design pattern.

This module contains the Model class which is responsible for preparing and processing the business logic of my application.

Responsibilites involve:
- loading the pre-trained model and tokenizer from the model chosen from my experiments;
- responding to the input text data passed in from the user and returning the prediction from the model.

"""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F 
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class Model:

    HUMAN_LABEL = 1
    MODEL_NAME = "dev/roberta_round1"   #CHANGE 
    TOKENIZER_NAME = "roberta-base"     #CHANGE
    
    def __init__(self):
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
            self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME)
            self.tokenizer = AutoTokenizer.from_pretrained(self.TOKENIZER_NAME)
        except Exception as e:
            raise ValueError(f"Error loading model or tokenizer: {e}")

        self.model.eval() 
    
    def evaluate_model(self, df, text_column="text", label_column="is_human"):
        """
        Evaluates the model's performance and counts predicted Human vs Bot.

        params:
        - model (Model): The classification model.
        - df (pd.DataFrame): The dataset containing text samples and true labels.
        - text_column (str): The name of the column containing text data.
        - label_column (str): The name of the column containing the true labels (1 = Human, 0 = Bot).

        returns:
        - dict: A dictionary containing Accuracy, Precision, Recall, F1-score, 
        and the count of predicted Humans and Bots.
        """
        print("starting evaluations...")
        predictions = []

        for text in df[text_column]:
            pred_label = self.get_classification(text)  # Model's classification
            predictions.append(1 if pred_label == "Human" else 0)  # Convert to binary

        # Convert to Pandas Series for easy aggregation
        y_pred = pd.Series(predictions)
        y_true = df[label_column]

        # Compute evaluation metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        # Count predicted classes
        num_humans = (y_pred == 1).sum()
        num_bots = (y_pred == 0).sum()
        total_predictions = num_humans + num_bots

        return {
            "Predicted Humans": f"{(num_humans / total_predictions) * 100:.0f}%",
            "Predicted Bots": f"{(num_bots / total_predictions) * 100:.0f}%",
            "Accuracy": round(accuracy, 4),
            "Precision": round(precision, 4),
            "Recall": round(recall, 4),
            "F1-score": round(f1, 4)
        }

    def get_classification(self, input_text: str) -> tuple[str, float]:
        """

        Processes input and uses helper function to return the classification and probability of the prediction
        This will be passed on to the View component.

        params:

        - self: the Model object
        - input_text (str): the text data to be processed and predicted by the model

        returns:

        - tuple:
            - prediction (str): the classification of the prediction
        
        """

        self.inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

        with torch.no_grad(): 
            self.outputs = self.model(**self.inputs)
        
        prediction = "Human" if torch.argmax(self.outputs.logits, dim=-1).item() == self.HUMAN_LABEL else "Bot"
        
        return prediction
    
