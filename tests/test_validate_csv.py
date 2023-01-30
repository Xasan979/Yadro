import pytest
import os
import allure
from csvreader_config import csv_dir
from logging import getLogger
from csvreader import CSVReader
from tests.csvreader_error import *

logger = getLogger()

csv_files_invalid = [
    pytest.param(os.path.join(csv_dir, "test_broken.csv")),
    pytest.param(os.path.join(csv_dir, "test_broken_headers.csv")),
    pytest.param(os.path.join(csv_dir, "test_invalid_character.csv"))]

csv_files_valid = [
    pytest.param(os.path.join(csv_dir, "test_nested.csv")),
    pytest.param(os.path.join(csv_dir, "file.csv"))]

csv_files_division_zero = [pytest.param(os.path.join(csv_dir, "test_zero.csv"))]

csv_files_empty = [pytest.param(os.path.join(csv_dir, "test_empty.csv"))]


@allure.epic("TestCSV")
class TestCSV:


    @staticmethod
    @allure.description("Checking csv_files_invalid")
    @allure.story('A correct error was received with invalid values in csv')
    @pytest.mark.parametrize("path_invalid", csv_files_invalid)
    def test_validate_csv(path_invalid):
        reader = CSVReader(path_invalid)
        with pytest.raises(InvalidValueError):
            reader.read_csv()
        logger.info('Got correct error with invalid csv')


    @staticmethod
    @allure.description("Checking csv_files_valid")
    @allure.story('The results of valid files are obtained')
    @pytest.mark.parametrize("path_valid", csv_files_valid)
    def test_calculate_csv(path_valid):
        reader = CSVReader(path_valid)
        reader.read_csv()
        assert reader
        logger.info('Valid file')


    @staticmethod
    @allure.description("Checking csv_files_division_zero")
    @allure.story('A correct error was received with division by zero')
    @pytest.mark.parametrize("path_division_zero", csv_files_division_zero)
    def test_calculate(path_division_zero):
        reader = CSVReader(path_division_zero)
        with pytest.raises(ZeroDivisionError):
            reader.read_csv()
        logger.info('Division by zero is prohibited')


    @staticmethod
    @allure.description("Checking csv_files_empty")
    @allure.story('A correct error was received with an empty csv')
    @pytest.mark.parametrize("path_empty", csv_files_empty)
    def test_read_csv(path_empty):
        reader = CSVReader(path_empty)
        with pytest.raises(EmptyCSVError):
            reader.read_csv()
        logger.info('Csv file is empty')
