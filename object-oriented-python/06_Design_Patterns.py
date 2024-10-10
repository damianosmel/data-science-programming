#!/usr/bin python3

import pandas as pd

DATASET_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
DATASET_COLUMN_NAMES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI",
                        "DiabetesPedigreeFunction", "Age", "Outcome"]


# Implements Singleton pattern to declare an instance only once and load a dataset only once
class PimaDatasetLoader:
    __instance = None
    _dataset = None

    def __new__(cls):
        if cls.__instance is None:
            print(f"Creating instance for first and last time")
            cls.__instance = super(PimaDatasetLoader, cls).__new__(cls)
        return cls.__instance

    def load_dataset(self):
        if self._dataset is None:
            print(f"Loading data set for first and last time")
            self._dataset = pd.read_csv(DATASET_URL, names=DATASET_COLUMN_NAMES)
        return self._dataset


if __name__ == "__main__":
    dataset_loader_first = PimaDatasetLoader()
    dataset_loader_second = PimaDatasetLoader()

    # check if loaders are the same
    print(f"Are the two loaders the same object: {dataset_loader_first is dataset_loader_second}")

    dataset_first = dataset_loader_first.load_dataset()
    dataset_second = dataset_loader_second.load_dataset()

    # check if loaded datasets are the same
    print(f"Are the two datasets the same object: {dataset_first is dataset_second}")
