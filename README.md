# Combating Fraudulent Social Media Accounts using Natural Language Processing - FakeProfileDetection Repository

## Overview
This repository contains tools and models for detecting fake profiles, specifically focusing on the identification of fraudulent user profiles in datasets. The project includes various notebooks for training, model optimization, and evaluation, as well as a GUI app to demonstrate the results of the optimised model in action. This was developed for my King's College London Undergraduate Computer Science Individual Project, supervised by Maher Salem.

## Directory Structure

- **dev**: Contains the main development files for the project.
    - **csv**: Contains CSV files.
    - **fake_profile_detector_app**: The folder containing a GUI application for demonstrating the optimised model.
    - **notebooks**: The directory containing Jupyter notebooks related to model training, optimisation, and evaluation.

## Dependencies for the app

To install all the required dependencies, you can use the following:

```bash
pip install -r requirements.txt
```
## Running the App

To run the Fake Profile Identification App, **ensure you are located in the repository folder** and then follow this step:

### On the Terminal run the application through Start.py:

```bash
python3 dev/fake_profile_detector_app/Start.py
```

### Notebooks Directory
The **notebooks** directory contains the Jupyter notebook that focus on building, training, and evaluating transformer-based models for text classification. Below is a description of the key notebook file:

#### **build_model.ipynb**
This notebook focuses on building and evaluating transformer-based models for text classification. It includes:
- **Data preprocessing**: Prepares the dataset for model training.
- **Tokenisation**: Converts text data into tokenised form for feeding into transformer models.
- **Model training**: Trains the model using the preprocessed and tokenised data.
- **Evaluation**: Evaluates the model using various performance metrics, including accuracy, precision, recall, and F1-score.
- **Hyperparameter tuning**: Uses **Optuna** for optimizing hyperparameters such as learning rate, batch size, and number of epochs to achieve the best results.

### Clean Datasets
- **Clean Datasets.py**: This Python script contains the `CleanDatasets` class, which is responsible for cleaning and preprocessing the datasets. This class is utilized within the notebooks for data preprocessing tasks.

### Fake Profile Detector App
- **GUI Application**: This is a simple Tkinter-based app developed to demonstrate the optimized model in action. It leverages my model which I uploaded to **Hugging Face's cloud** for seamless inference. The app allows users to upload a CSV dataset and click "Classify Dataset" to receive the classification results and evaluation metrics.
- **Note**: The application is single-threaded, meaning it can become slow or unresponsive when handling large datasets or heavy computation. Users are advised to be patient, as this application is primarily for research demonstration purposes.

## Running the Notebooks in Google Colab

As explained in more detail in the file, this is the necessary step: 

### Clone the Repository to Google Drive
On first-time access, uncomment the following lines in the notebook to clone the repository into your Google Drive:

```python
%cd /content/drive/MyDrive/
!git clone https://github.com/hannahishimwe/FakeProfileDetection.git
```

Then you will be able to run the rest of the cells

## Academic Note:

This application is for research purposes, and the performance limitations (due to Tkinter's single-threaded nature) are acknowledged. Optimizing the UI for better performance under heavy computation was outside the scope of the project, as this was not part of the academic requirements.

#### Feel free to clone the repository, experiment with the models, and explore the results! If you have any issues or suggestions, please feel free to raise an issue or create a pull request.
