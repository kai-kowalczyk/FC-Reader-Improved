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
        self.filetype = self.set_filetype()
        self.validated = self.validate_source()

    def validate_source(self):
        if Path(self.path).exists():
            if Path(self.path).is_file():
                if self.filetype not in self.ALLOWED_EXTENSIONS:
                    print('Nieobsługiwany format.')
                    return 'wrong_ext'
                else:
                    return f'valid_{self.filetype}'
            else:
                return 'valid_path'
        else:
            if Path(self.parent_path).is_dir():
                return 'valid_parent_path'
            else:
                return 'invalid_path'

    def validate_destination(self):
        ext = Path(self.destination).suffix[1:]
        dest_parent = Path(self.destination).parent
        if ext not in self.ALLOWED_EXTENSIONS:
            print('Podano złe rozszerzenie pliku wyjściowego. Obsługiwane formaty: .csv, .json, .pickle')
            quit()
        elif not Path(dest_parent).exists():
            print(f'Podana ścieżka pliku wyjściowego {self.destination} nie istnieje.')
            quit()

    def set_filetype(self):
        return Path(self.filename).suffix[1:]

    def show_files_in_dir(self):
        if self.validated == 'wrong_ext':
            print('Podano złe rozszerzenie pliku wejściowego. Dostępne pliki .csv, .json i .pickle w katalogu nadrzędnym to: ')
            print(sorted(Path(self.parent_path).glob('*.csv', '*.json', '*.pickle')))
        elif self.validated == 'valid_path':
            print('Nie podano nazwy pliku wejściowego. Dostępne pliki .csv, .json i .pickle w podanym katalogu to: ')
            print(sorted(Path(self.path).glob('*.csv', '*.json', '*.pickle')))
        elif self.validated == 'valid_parent_path':
            print('Podano złą ścieżkę pliku wejściowego. Dostępne pliki .csv, .json i .pickle w katalogu nadrzędnym to: ')
            print(sorted(Path(self.parent_path).glob('*.csv')))
        else:
            print('Podano złą ścieżkę pliku wejściowego. Dostępne pliki .csv, .json i .pickle w bieżącym katalogu to: ')
            print(sorted(Path(self.cwd).glob('*.csv', '*.json', '*.pickle')))

class CSVReader(Reader):

    def get_csv_data(self):
        with open(self.path, 'r', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            file_data = []
            for row in reader:
                file_data.append(row)
        return file_data

class JSONReader(Reader):
    
    def get_json_data(self):
        pass


class PickleReader(Reader):
    
    def get_pickle_data(self):
        pass
