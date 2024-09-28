#!/usr/bin python3

import pandas as pd
from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split

DATASET_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
DATASET_COLUMN_NAMES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI",
                        "DiabetesPedigreeFunction", "Age", "Outcome"]


class DatasetProcessing(ABC):
    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def calculate_stats_per_feature(self):
        pass

    @abstractmethod
    def split_dataset(self):
        pass

    @abstractmethod
    def calculate_target_variable_distribution(self):
        pass


class StandardDatasetProcessor(DatasetProcessing):
    def __init__(self, name):
        self._name = name
        self._dataset = None
        self._data, self._target = None, None
        self.__spliting_seed = 25031821

    def load_data(self, dataset, target_variable_name):
        print(f"Loading data from Dataframe")
        self._dataset = dataset
        self._data = self._dataset.loc[:, self._dataset.columns != target_variable_name]
        self._target = self._dataset[target_variable_name]

    def calculate_stats_per_feature(self):
        print("    ~~~    ")
        print("Stats for each feature")
        print(f"{self._data.describe().loc[['mean', 'std']]}")

    def split_dataset(self, test_ratio):
        print("    ~~~    ")
        print(f"Splitting into training & testing, with test ratio={test_ratio:.3f}")
        if test_ratio > 0.0 and test_ratio <= 1.0:
            self._data_train, self._data_test, self._target_train, self._target_test = train_test_split(self._data,
                                                                                                        self._target,
                                                                                                        test_size=test_ratio,
                                                                                                        random_state=self.__spliting_seed)

            self._data_test = self._dataset.drop(self._data_train.index)
            print(f"Training instances: {self._data_train.head()}")
            print(f"Testing instances: {self._data_test.head()}")

    def calculate_target_variable_distribution(self):
        print("    ~~~    ")
        print("Stats for target variable")
        print(f"{self._target.value_counts()}")


class Patient:
    def __init__(self, attributes):
        self.attributes = attributes
        self.attributes["Outcome"] = "Diabetic" if self.attributes["Outcome"] == 1 else "Non-diabetic"

    @classmethod
    def arrange_values_to_names(cls, names, values):
        return dict(zip(names, values))

    def get_attributes(self):
        return self.attributes

class PatientDataSet:
    def __init__(self, patients):
        self._patients = [patient.get_attributes() for patient in patients]

    def to_dataframe(self):
        return pd.DataFrame(self._patients)

if __name__ == "__main__":
    # create 100 patients instances and use to create a new dataset (subset of initial one)
    pima_dataset = pd.read_csv(DATASET_URL, names=DATASET_COLUMN_NAMES)
    patient_13_row = pima_dataset.iloc[12]
    patient_13 = Patient(Patient.arrange_values_to_names(pima_dataset.columns.values, list(patient_13_row)))
    patients_100 = [
        Patient(Patient.arrange_values_to_names(pima_dataset.columns.values, list(pima_dataset.iloc[row_count]))) for
        row_count in range(1, 100)]
    patients_100_dataset = PatientDataSet(patients_100)

    # process the created dataset
    patients_data_processor = StandardDatasetProcessor("Pima Indian Diabetes Dataset - First 100 patients")
    data = patients_100_dataset.to_dataframe()
    patients_data_processor.load_data(patients_100_dataset.to_dataframe(), "Outcome")
    patients_data_processor.calculate_stats_per_feature()
    patients_data_processor.split_dataset(test_ratio=1 / 3)
    patients_data_processor.calculate_target_variable_distribution()
