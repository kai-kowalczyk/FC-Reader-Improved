import sys
from pathlib import Path
from lib import Reader

source = sys.argv[1]
destination = sys.argv[2]
changes = sys.argv[3:]

'''changes "Y,X,wartosc" Y - wiersz(od 0), X - kolumna (od 0), wartosc - modyfikacja do wpisania w komórkę'''


reader = Reader(source, destination, changes)

if reader.validated == 'valid_csv':
    pass

elif reader.validated == 'valid_json':
    pass

elif reader.validated == 'valid_pickle':
    pass

else:
    reader.show_files_in_dir()
