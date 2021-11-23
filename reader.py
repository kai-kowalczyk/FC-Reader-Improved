import sys
from lib import Reader

try:
    source = sys.argv[1]
    destination = sys.argv[2]
    changes = sys.argv[3:]
    reader = Reader(source, destination, changes)
except IndexError:
    print('Uruchom program wpisując "python3 reader.py [source] [destination][nr rzędu,nr kolumny,zmiana do wprowadzenia]". Zmian możesz wprowadzić więcej niż jedną. Numery rzędów i kolumn policz zaczynając od 0.')




