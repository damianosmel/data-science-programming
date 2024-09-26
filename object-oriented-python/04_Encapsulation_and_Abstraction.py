#!/usr/bin python3

from abc import ABC, abstractmethod
import pandas as pd
from sklearn.model_selection import train_test_split

DATASET_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
DATASET_COLUMN_NAMES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI",
                        "DiabetesPedigreeFunction", "Age", "Outcome"]


class DataAnalysis(ABC):
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


class DiabetesDataAnalysis(DataAnalysis):
    def __init__(self, name):
        self._name = name
        self._dataset = None
        self._data, self._target = None, None
        self.__spliting_seed = 25031821

    def load_data(self, data_uri, data_column_names, target_variable_name):
        print(f"Loading data from {data_uri}")
        self._dataset = pd.read_csv(data_uri, names=data_column_names)
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


if __name__ == "__main__":
    pima_data_analysis = DiabetesDataAnalysis("Pima Indian Diabetes Dataset")
    pima_data_analysis.load_data(DATASET_URL, DATASET_COLUMN_NAMES, "Outcome")
    pima_data_analysis.calculate_stats_per_feature()
    pima_data_analysis.split_dataset(test_ratio=1 / 3)
    pima_data_analysis.calculate_target_variable_distribution()
