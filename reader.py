import sys
from pathlib import Path
from lib import Reader, CSVReader, JSONReader, PickleReader

source = sys.argv[1]
destination = sys.argv[2]
changes = sys.argv[3:]

'''changes "Y,X,wartosc" Y - wiersz(od 0), X - kolumna (od 0), wartosc - modyfikacja do wpisania w komórkę'''

#reader = Reader(source, destination, changes)

def set_filetype():
    return Path(source).suffix[1:]

if set_filetype() == 'csv':
    reader = CSVReader(source, destination, changes, 'csv')
    if reader.validated == 'valid_csv':
        file_data = reader.get_csv_data()
        for element in reader.changes:
            row_index, column_index, change_value = reader.validate_change(element)
            reader.mod_file(file_data, row_index, column_index, change_value)
        reader.create_output(file_data)
    else:
        reader.show_files_in_dir()

elif set_filetype() == 'json':
    reader = JSONReader(source, destination, changes, 'json')
    if reader.validated == 'valid_json':
        file_data = reader.get_json_data()
        for element in reader.changes:
            row_index, column_index, change_value = reader.validate_change(element)
            reader.mod_file(file_data, row_index, column_index, change_value)
        reader.create_output(file_data)
        print(file_data)

elif set_filetype() == 'pickle':
    pass

else:
    reader = Reader(source, destination, changes)
    reader.show_files_in_dir()
