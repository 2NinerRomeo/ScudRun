import argparse
import datetime
from pathlib import Path

import dbConnect as db
from cardCsvLoader import CREDFILENAME, loadTransactions


def filename_date(path):
    """Return the date encoded in a supported card CSV filename."""
    name = path.name
    for date_format, date_length in (('%Y%m%d', 8), ('%Y-%m-%d', 10)):
        for start in range(len(name) - date_length + 1):
            candidate = name[start:start + date_length]
            try:
                return datetime.datetime.strptime(candidate, date_format).date()
            except ValueError:
                continue
    raise ValueError(f"No date found in CSV filename: {name}")


def find_card_csv_files(folder):
    """Find and chronologically sort CSV files directly in a folder."""
    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise ValueError(f"Not a directory: {folder}")

    csv_files = list(folder_path.glob('*.csv'))
    invalid_files = [path for path in csv_files if _has_no_filename_date(path)]
    if invalid_files:
        names = ', '.join(path.name for path in invalid_files)
        raise ValueError(f"No date found in CSV filename(s): {names}")

    return sorted(csv_files, key=lambda path: (filename_date(path), path.name))


def _has_no_filename_date(path):
    try:
        filename_date(path)
    except ValueError:
        return True
    return False


def load_card_csv_folder(folder, input_fn=input):
    """Load every dated CSV in chronological filename order."""
    csv_files = find_card_csv_files(folder)
    if not csv_files:
        print(f"No CSV files found in {Path(folder)}")
        return

    database = db.Dbase(CREDFILENAME)
    database.connect()
    for csv_file in csv_files:
        print(f"Loading {csv_file}")
        loadTransactions(database, str(csv_file), input_fn=input_fn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Load dated card transaction CSV files in chronological order.')
    parser.add_argument('folder', help='Folder containing card CSV files')
    args = parser.parse_args()
    load_card_csv_folder(args.folder)
