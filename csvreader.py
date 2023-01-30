import argparse
import copy
import re
from pprint import pprint
from tests.csvreader_error import InvalidValueError, EmptyCSVError


class CSVReader:

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.raw_csv = None
        self.calculated_csv = None
        self.values = None
        self.axes = None

    def _validate_csv(self):
        """
        Проверить что ось x буквы, а у - целые числа
        """
        for key, value in self.axes.items():
            validate_header = lambda header: header.isalpha() if key == 'x' else header.isdigit()
            for val in value:
                try:
                    assert validate_header(val)
                except AssertionError:
                    raise InvalidValueError(
                        f"В названии {'столбца' if key == 'x' else 'строки'} присутствует {val} вместо "
                        f"{'буквы' if key == 'x' else 'целого, положительного числа'}. {value} ")

        # '''Проверка на допустимые символы :  +, -, *, / '''
        expressions = [cell for value_1 in self.values for cell in value_1 if "=" in cell]
        for desired_value in expressions:
            for y_index, row in enumerate(self.values):
                for x_index, cell_value in enumerate(row):
                    if cell_value == desired_value:
                        x_value = self.axes['x'][x_index]
                        y_value = self.axes['y'][y_index]
                        operators = ['+', '-', '*', '/']
                        try:
                            assert any(c in operators for c in cell_value)
                        except AssertionError:
                            raise InvalidValueError(
                                f"В ячейке {x_value}{y_value} обнаружены недопустимые символы"
                                f" {cell_value}, к допустимым относятся {operators} ")

        # """Проверку что в ячейках целые а не дробные числа или отрицательные числа"""
        for y_index, row in enumerate(self.values):
            for x_index, element in enumerate(row):
                if element.replace(".", "").replace("-", "").isnumeric():
                    x_value = self.axes['x'][x_index]
                    y_value = self.axes['y'][y_index]
                    element = int(element)
                    try:
                        assert element >= 0
                    except (ValueError, AssertionError):
                        raise InvalidValueError(
                            f"{element} значение является float в ячейке {x_value}{y_value} ")
                    except AssertionError:
                        raise InvalidValueError(
                            f"{element} значение является отрицательным числом в ячейке {x_value}{y_value} ")

    def _calculate_cell(self, expression):

        cell_names = re.findall(r'(?P<x>[a-zA-Z]+)(?P<y>\d*)', string=expression)
        cell_value_map = {}
        for name in cell_names:
            # Отлавливать ошибку с несуществующей ячейкой
            value_position = {"x": self.axes['x'].index(name[0]),
                              "y": self.axes['y'].index(name[1])
                              }
            key = f"{name[0]}{name[1]}"
            value = self.values[value_position['y']][value_position['x']]
            value = '0' if value == "" else value
            if "=" in value:
                nested_expression = copy.deepcopy(value)
                nested_values_map = self._calculate_cell(nested_expression)
                for k, v in nested_values_map.items():
                    nested_expression = nested_expression.replace(k, v)
                value = str(eval(nested_expression.replace('=', '')))
            cell_value_map[key] = value
        return cell_value_map

    def _calculate(self, expression):
        """
        Вычислить все совпадающие выражения в csv
        """
        calculated_cells = self._calculate_cell(expression)
        for key, value in calculated_cells.items():
            expression = expression.replace(key, value)
        try:
            assert '/' not in expression or not re.search(r'(?<!\d)0(?!\d)', expression)
            return eval(expression.replace('=', ''))
        except AssertionError:
            raise ZeroDivisionError(f"В выражении {expression} , деление на ноль запрещено")
        except TypeError:
            raise BaseException

    def _calculate_csv(self):
        """
        Рассчитать и распечатать csv
        """

        self.calculated_csv = [self.raw_csv[0]]
        for row_idx, row in enumerate(self.raw_csv[1:]):
            row_idx += 1
            self.calculated_csv.insert(row_idx, "")
            splitted_raw = row.split(',')
            for cell_idx, cell in enumerate(splitted_raw):
                separator = "" if cell_idx + 1 == len(splitted_raw) else ","
                self.calculated_csv[row_idx] += f'{self._calculate(cell)}{separator}' if '=' in cell \
                    else f"{cell}{separator}"
        pprint(self.calculated_csv, width=1)

    def read_csv(self):
        """
        Прочитайте и проанализируйте необработанный csv-файл для дальнейшего использования
        """
        with open(file=self.csv_path, encoding='utf-8', mode='r') as file:
            self.raw_csv = file.read().splitlines()
            self.values = [row.replace('\n', '').split(',')[1:] for row in self.raw_csv[1:]]
            if len(self.raw_csv) == 0:
                raise EmptyCSVError('Csv фаил пустой')
            self.axes = {'x': self.raw_csv[0][1:].split(','),
                         'y': [row.split(',')[0] for row in self.raw_csv[1:]]}
            self._validate_csv()
            self._calculate_csv()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse csv file to table')
    parser.add_argument('--path', type=str, required=True, help='Path to csv file')

    args = parser.parse_args()
    if args.path:
        CSVReader(args.path).read_csv()
