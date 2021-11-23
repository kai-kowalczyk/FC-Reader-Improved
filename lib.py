from pathlib import Path
import csv
import json
import pickle

class Reader:

    ALLOWED_EXTENSIONS = ('csv', 'json', 'pickle')

    def __init__(self, path, destination, changes):
        self.filename = Path(path).name
        self.path = path
        self.parent_path = Path(self.path).parent  
        self.destination = destination
        self.changes = changes
        self.cwd = Path.cwd()
        self.src_filetype = self.set_filetype(self.filename)
        self.dest_filetype = self.set_filetype(Path(self.destination).name)
        self.src_validated = self.validate_source()
        self.dest_validated = self.validate_destination()
        self.file_data = self.read_data()
        self.mod_file()
        self.create_output()

    def validate_source(self):
        if Path(self.path).exists():
            if Path(self.path).is_file():
                if self.src_filetype not in self.ALLOWED_EXTENSIONS:
                    print('Nieobsługiwany format.')
                    error = 'wrong_ext'
                    self.show_files_in_dir(error)
                else:
                    return f'valid_{self.src_filetype}'
            else:
                error = 'valid_path'
                self.show_files_in_dir(error)
        else:
            if Path(self.parent_path).is_dir():
                error = 'valid_parent_path'
                self.show_files_in_dir(error)
            else:
                error = 'invalid_path'
                self.show_files_in_dir(error)

    def validate_destination(self):
        dest_parent = Path(self.destination).parent
        if self.dest_filetype not in self.ALLOWED_EXTENSIONS:
            print('Podano złe rozszerzenie pliku wyjściowego. Obsługiwane formaty: .csv, .json, .pickle')
            quit()
        elif not Path(dest_parent).exists():
            print(f'Podana ścieżka pliku wyjściowego {self.destination} nie istnieje.')
            quit()
        else:
            return True

    def set_filetype(self, file):
        return Path(file).suffix[1:]

    def validate_change(self, element):
        splitted_element = element.split(',')
        row_index = int(splitted_element[0])
        column_index = int(splitted_element[1])
        change_value = splitted_element[2]
        return row_index, column_index, change_value

    def mod_file(self):
        try:
            for element in self.changes:
                row_index, column_index, change_value = self.validate_change(element)
                self.file_data[row_index][column_index] = str(change_value)
        except IndexError:
            print('Wprowadzono nr rzędu/nr kolumny, które nie istnieją w pliku źródłowym. Wprowadź poprawne dane.')
            quit()

    def read_data(self):
        if self.src_filetype == 'csv':
            csv_src = CSVReader()
            return csv_src.get_csv_data(self.path)
        elif self.src_filetype == 'json':
            json_src = JSONReader()
            return json_src.get_json_data(self.path)
        elif self.src_filetype == 'pickle':
            pickle_src = PickleReader()
            return pickle_src.get_pickle_data(self.path) 

    def create_output(self):
        if self.dest_filetype == 'csv':
            csv_dest = CSVReader()
            csv_dest.csv_output(self.file_data, self.destination)
        elif self.dest_filetype == 'json':
            json_dest = JSONReader()
            json_dest.json_output(self.file_data, self.destination)
        elif self.dest_filetype == 'pickle':
            pickle_dest = PickleReader()
            pickle_dest.pickle_output(self.file_data, self.destination)

    def show_files_in_dir(self, error):
        if error == 'wrong_ext':
            print('Podano złe rozszerzenie pliku wejściowego. Dostępne pliki .csv, .json i .pickle w katalogu nadrzędnym to: ')
            print(sorted(Path(self.parent_path).glob('*.csv', '*.json', '*.pickle')))
        elif error == 'valid_path':
            print('Nie podano nazwy pliku wejściowego. Dostępne pliki .csv, .json i .pickle w podanym katalogu to: ')
            print(sorted(Path(self.path).glob('*.csv', '*.json', '*.pickle')))
        elif error == 'valid_parent_path':
            print('Podano złą ścieżkę pliku wejściowego. Dostępne pliki .csv, .json i .pickle w katalogu nadrzędnym to: ')
            print(sorted(Path(self.parent_path).glob('*.csv')))
        else:
            print('Podano złą ścieżkę pliku wejściowego. Dostępne pliki .csv, .json i .pickle w bieżącym katalogu to: ')
            print(sorted(Path(self.cwd).glob('*.csv', '*.json', '*.pickle')))


class CSVReader(Reader):

    def __init__(self):
        pass

    def get_csv_data(self, src_file):
        print('get csv data')
        with open(src_file, 'r', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            file_data = []
            for row in reader:
                file_data.append(row)
        return file_data

    def csv_output(self, data, dest_file):
        with open(dest_file, 'w') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(data)

class JSONReader(Reader):

    def __init__(self):
        pass
    
    def get_json_data(self, src_file):
        with open(src_file, 'r', newline='') as file:
            file_data = json.load(file)
        return file_data

    def json_output(self, data, dest_file):
        with open (dest_file, 'w') as file:
            json.dump(data, file)

class PickleReader(Reader):

    def __init__(self):
        pass
    
    def get_pickle_data(self, src_file):
        with open(src_file, 'rb') as file:
            file_data = pickle.load(file)
        return file_data

    def pickle_output(self, data, dest_file):
        with open(dest_file, 'wb') as file:
            pickle.dump(data, file)
