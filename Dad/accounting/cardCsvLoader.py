import csv
import sys
import dbConnect as db
import csvParser as csv
from enum import Enum
import datetime
from collections import Counter
from decimal import Decimal

CREDFILENAME = 'creds.json'


class CardType(Enum):
    CHASE = 1
    AMEX = 2


def _date_value(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    return value


def _amount_value(value):
    return Decimal(str(value)).normalize()


def _transaction_values(trans, card, account_suffix=None):
    if card == CardType.CHASE:
        return {
            'transDate': datetime.datetime.strptime(
                trans['Transaction Date'], '%m/%d/%Y').strftime('%Y-%m-%d'),
            'postDate': datetime.datetime.strptime(
                trans['Post Date'], '%m/%d/%Y').strftime('%Y-%m-%d'),
            'description': trans['Description'],
            'autoCat': trans['Category'],
            'autoType': trans['Type'],
            'amount': trans['Amount'],
            'memo': trans['Memo'],
            'account': account_suffix,
        }
    if card == CardType.AMEX:
        return {
            'transDate': None,
            'postDate': datetime.datetime.strptime(
                trans['Date'], '%m/%d/%Y').strftime('%Y-%m-%d'),
            'description': trans['Description'],
            'amount': str(float(trans['Amount']) * -1),
            'memo': trans['Card Member'],
            'account': trans['Account #'],
        }
    raise ValueError('Unknown statement type')


def _signature(values):
    return (
        _date_value(values['transDate']),
        _date_value(values['postDate']),
        values['description'],
        _amount_value(values['amount']),
        values['memo'],
        values['account'],
        values['acct_id'],
    )


def _bank_card_ids(cursor):
    cursor.execute("SELECT account_id, suffix FROM bankCards")
    return {suffix: card_id for card_id, suffix in cursor.fetchall()}


def _resolve_account_ids(values_list, bank_card_ids):
    for values in values_list:
        account_suffix = values['account']
        if account_suffix not in bank_card_ids:
            print("Unable to find bankCards suffix for transaction:", values)
            raise ValueError(
                f"No bankCards entry found for account suffix {account_suffix!r}")
        values['acct_id'] = bank_card_ids[account_suffix]


def _database_signatures(cursor, account_ids):
    fields = ('transDate', 'postDate', 'description', 'amount', 'memo', 'account', 'acct_id')
    placeholders = ', '.join(['%s'] * len(account_ids))
    cursor.execute(
        "SELECT transDate, postDate, description, amount, memo, account, acct_id "
        f"FROM cardTransactions WHERE acct_id IN ({placeholders})",
        tuple(account_ids))
    #print(f"Placeholders: {placeholders}")
    #print(f"Database query returned {cursor.rowcount} rows for account IDs: {account_ids}")
    return Counter(_signature(dict(zip(fields, row))) for row in cursor.fetchall())


def _confirm_gap(first_gap, transaction_count, input_fn):
    answer = input_fn(
        f"Existing transactions reappear after CSV row {first_gap + 1} "
        f"of {transaction_count}. Load through this gap? [y/N] ")
    return answer.strip().lower() in ('y', 'yes')


def _insert_transactions(database, cardDictLst, card, file_path, account_suffix=None, input_fn=input):
    cursor = database.db.cursor()
    #Card transactions are stored in reverse order, so we need to reverse the 
    # list to get the correct order for insertion.
    values_list = [_transaction_values(trans, card, account_suffix)
                   for trans in reversed(cardDictLst)]
    bank_card_ids = _bank_card_ids(cursor)
    _resolve_account_ids(values_list, bank_card_ids)
    existing = _database_signatures(cursor, sorted({values['acct_id'] for values in values_list}))
    matched = []

    if card == CardType.CHASE:
        print("Looks Like a Chase Statement")
        insert_query = ("INSERT INTO cardTransactions (transDate, postDate, "
                        "description, autoCat, autoType, amount, memo, account,"
                        " acct_id) VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s)")
        fields = ('transDate', 'postDate', 'description', 'autoCat', 'autoType',
                  'amount', 'memo', 'account', 'acct_id')
    elif card == CardType.AMEX:
        print("Looks Like an Amex Statement")
        insert_query = ("INSERT into cardTransactions (postDate, description, "
                        "amount, memo, account, acct_id) VALUES (%s, %s, %s, %s, %s, %s)")
        fields = ('postDate', 'description', 'amount', 'memo', 'account', 'acct_id')
    else:
        raise ValueError("Unknown statement type")

    for values in values_list:
        signature = _signature(values)
        matched.append(bool(existing[signature]))
        if existing[signature]:
            existing[signature] -= 1

    #look for gaps in the matched list. If there is a gap, confirm with the user before proceeding.
    first_unmatched = next((index for index, is_match in enumerate(matched) if not is_match), None)
    gap_found = first_unmatched is not None and any(matched[first_unmatched + 1:])
    if gap_found:
        if not _confirm_gap(first_unmatched, len(values_list), input_fn):
            values_list = values_list[:first_unmatched]

    inserted = 0
    duplicates_skipped = 0
    for index, values in enumerate(values_list):
        if matched[index]:
            duplicates_skipped += 1
            continue
        vals = tuple(values[field] for field in fields)
        #print("Post Date: " + values['postDate'] + " Description: "
        #      + values['description'] + " amount: " + str(values['amount']))
        cursor.execute(insert_query, vals)
        inserted += 1

    database.db.commit()
    print("File loaded:", file_path)
    print("   ", inserted, "record(s) inserted.")
    print("   ", duplicates_skipped, "duplicate record(s) skipped.")
    if not gap_found:
        print("    No gaps found.")


def _chase_account_suffix(file_path):
    filename = file_path.rsplit('\\', 1)[-1].rsplit('/', 1)[-1]
    return '-' + filename[5:9]


def loadTransactions(database, file_path, input_fn=input):
    cardCsv = csv.CSVParser(file_path)
    cardCsv.read_csv()
    cardDictList = cardCsv.to_dict_list()

    chaseList = ['Transaction Date', 'Post Date', 'Description', 'Category', 'Type', 'Amount', 'Memo']
    amexList = ['Date', 'Description', 'Card Member', 'Account #', 'Amount']

    #print(cardCsv.headers)
    if cardCsv.headers == chaseList:
        return _insert_transactions(
            database, cardDictList, CardType.CHASE,
            file_path, _chase_account_suffix(file_path), input_fn)
    if cardCsv.headers == amexList:
        return _insert_transactions(
            database, cardDictList, CardType.AMEX, file_path, input_fn=input_fn)
    raise ValueError("Unknown statement")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the path to the CSV file as an argument.")
        sys.exit(1)

    finDb = db.Dbase(CREDFILENAME)
    finDb.connect()
    loadTransactions(finDb, sys.argv[1])