#!/usr/bin python3

import pandas as pd

DATASET_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
DATASET_COLUMN_NAMES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI",
                        "DiabetesPedigreeFunction", "Age", "Outcome"]


class Dataset:
    def __init__(self, name):
        self.name = name
        self.dataset = None

    def load_data(self, data_uri, data_column_names):
        print(f"Loading data from {data_uri}")
        return pd.read_csv(data_uri, names=data_column_names)

    def calculate_average_on_column(self, column_name):
        print(f"The average value of column: {column_name}= {self.dataset[column_name].mean():.3f}")

    def welcome_message(self):
        print("Welcome to Dataset class!")


class DiabetesDataset(Dataset):
    # "Pima Indian::Diabetes Specific Dataset"
    def __init__(self, name):
        super().__init__(name=name)

    def load_data(self, data_uri, data_column_names):
        self.dataset = super().load_data(data_uri, data_column_names)
        print("Now convert label column from numeric to categorical")
        self.dataset["Outcome"] = self._convert_class_label_to_categorical()

    def _convert_class_label_to_categorical(self):
        return self.dataset["Outcome"].apply(lambda numeric_label: "Diabetic" if numeric_label == 1 else "Non-diabetic")

    def calculate_class_percentage(self):
        print("    ===    ")
        print("Calculating percentages per label: ")
        label_counts = self.dataset["Outcome"].value_counts().to_dict()
        total_counts = sum(label_counts.values())
        for label, count in label_counts.items():
            print(f"{label}: {(count / total_counts) * 100.0:.3f}")
        print("    ===    ")

    def welcome_message(self):
        print("Welcome to the diabetes dataset!")


if __name__ == "__main__":
    pima_dataset = DiabetesDataset("Pima Indian Diabetes Dataset")
    pima_dataset.load_data(DATASET_URL, DATASET_COLUMN_NAMES)
    pima_dataset.calculate_class_percentage()
    pima_dataset.calculate_average_on_column("Age")
    pima_dataset.welcome_message()
    print("    ~~~    ")
    general_dataset = Dataset("A General Dataset")
    general_dataset.welcome_message()
