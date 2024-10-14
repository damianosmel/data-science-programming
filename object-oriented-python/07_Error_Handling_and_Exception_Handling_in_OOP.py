#!/usr/bin python3
from urllib.error import URLError

import pandas as pd
import urllib.request

DATASET_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
DATASET_COLUMN_NAMES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI",
                        "DiabetesPedigreeFunction", "Age", "Outcome"]


class NotExpectedColumnNamesError(Exception):
    def __init__(self, expected_column_number, actual_column_number):
        self._expected_column_number = expected_column_number
        self._actual_column_number = actual_column_number
        self.reason = f"Number of columns of loaded dataframe is not equal to the expected one.\nActual:{self._actual_column_number}\nExpected:{self._expected_column_number}"


class PimaDataset:
    _dataset = None
    _dataset_file = "pima_dataset.csv"
    _dataset_column_names = None

    def __init__(self, data_url, column_names):
        try:
            urllib.request.urlretrieve(data_url, self._dataset_file)
            self._load_dataset(column_names)

        except urllib.error.URLError as url_error:
            print(f"URL error on GET request, reason: {url_error.reason}.")
        except urllib.error.HTTPError as http_error:
            print(f"HTTP error on GET request, reason: {http_error.reason}.")
        except NotExpectedColumnNamesError as columns_number_error:
            print(f"Parsing error on reading dataframe from file, reason: {columns_number_error.reason}.")

    def _load_dataset(self, column_names):
        print(self._dataset_file)
        self._dataset = pd.read_csv(self._dataset_file)
        self._dataset_column_names = column_names
        columns_number_expected = len(self._dataset_column_names)
        _, columns_number_actual = self._dataset.shape
        if columns_number_expected != columns_number_actual:
            self._dataset = None
            raise NotExpectedColumnNamesError(columns_number_expected, columns_number_actual)

    def get_basic_stats_per_feature(self):
        print("    ~~~    ")
        print("Stats per feature: ")
        print(f"{self._dataset.describe().loc[['mean', 'std']]}")


if __name__ == "__main__":
    ###     ###     ###
    # raise URL ERROR
    ###     ###     ###
    # dataset_url_incorrect = DATASET_URL + "_something_faulty"
    # assert PimaDataset(dataset_url_incorrect,DATASET_COLUMN_NAMES), "URL error on GET request, reason: Not Found."

    ###     ###     ###
    # raise custom parsing error: "not expected number of columns"
    ###     ###     ###
    dataset_columns_incomplete = DATASET_COLUMN_NAMES[0:3]
    assert PimaDataset(DATASET_URL,
                       dataset_columns_incomplete), f"Parsing error on reading dataframe from file, reason: Number of columns of loaded dataframe is not equal to the expected one.\nActual:{dataset_columns_incomplete}\nExpected:{DATASET_COLUMN_NAMES}."
