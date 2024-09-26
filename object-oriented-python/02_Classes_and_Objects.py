#!/usr/bin/env python3

import pandas as pd

DATASET_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
DATASET_COLUMN_NAMES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI",
                        "DiabetesPedigreeFunction", "Age", "Outcome"]


class Person:
    def __init__(self, attributes):
        print(f"Initializing Person instance...")
        self.attributes = attributes
        self.attributes["Outcome"] = "Diabetic" if self.attributes["Outcome"] == 1 else "Non-diabetic"

    @classmethod
    def arrange_values_to_names(cls, names, values):
        return dict(zip(names, values))

    def print_info(self):
        print(f"Printing patient info:")
        for name, value in self.attributes.items():
            print(f"{name}: {value}")

    def is_diabetic(self):
        return True if self.attributes["Outcome"] == "Diabetic" else False


pima_dataset = pd.read_csv(DATASET_URL, names=DATASET_COLUMN_NAMES)
patient_22_row = pima_dataset.iloc[21]
patient_22 = Person(Person.arrange_values_to_names(pima_dataset.columns.values, list(patient_22_row)))
patient_22.print_info()
print(f"this patient is diabetic: {patient_22.is_diabetic()}")
