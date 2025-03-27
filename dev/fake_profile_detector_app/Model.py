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
    MODEL_NAME = "hannahishimwe/fakeprofiledetection_roberta"
    TOKENIZER_NAME = "roberta-base" 
    
    
    def __init__(self):
        """

        Initializes the Model object with the pre-trained model and tokenizer.

        params:

        - self: the Model object
        - model_name (str): the name of the pre-trained model to be loaded
        - tokenizer_name(str): the name of the pre-trained tokenizer to be loaded

        """
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME, from_tf=False)
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
        y_pred = df[text_column].apply(self.get_classification).map({"Human": 1, "Bot": 0})
        y_true = df[label_column]

        metrics = {
            "Accuracy": round(accuracy_score(y_true, y_pred), 4),
            "Precision": round(precision_score(y_true, y_pred), 4),
            "Recall": round(recall_score(y_true, y_pred), 4),
            "F1-score": round(f1_score(y_true, y_pred), 4),
            "Predicted Humans": (y_pred == 1).sum(),
            "Predicted Bots": (y_pred == 0).sum(),
            "Actual Humans": (y_true == 1).sum(),
            "Actual Bots": (y_true == 0).sum(),
        }

        return metrics

    def get_classification(self, input_text: str):
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

        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

        with torch.no_grad():
            logits = self.model(**inputs).logits

        return "Human" if torch.argmax(logits).item() == self.HUMAN_LABEL else "Bot"


