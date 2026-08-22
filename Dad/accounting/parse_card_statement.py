import argparse
import os
import re
from datetime import datetime
from decimal import Decimal
import pdb

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - fallback if pypdf is unavailable
    PdfReader = None


def format_sql_date(date_str):
    """Convert a US-formatted date string to YYYY-MM-DD for SQL."""
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Could not parse date: {date_str}")

def parse_chase_statement(normalized_text):
    """Extract statement details from a Chase PDF statement.

    Returns a dictionary with:
    - Previous Balance
    - Current Balance
    - Opening Date
    - Closing Date
    - Account Number
    """
    previous_balance_match = re.search(r"Previous Balance\s*(?P<sign>[-])?\$(?P<amount>[0-9,]+\.\d{2})", normalized_text)
    current_balance_match = re.search(r"(?:New Balance|Current Balance)\s*(?P<sign>[-])?\$(?P<amount>[0-9,]+\.\d{2})", normalized_text)
    date_range_match = re.search(r"Opening/Closing Date\s*([0-9]{2}/[0-9]{2}/[0-9]{2})\s*-\s*([0-9]{2}/[0-9]{2}/[0-9]{2})", normalized_text)
    account_number_match = re.search(r"Account number:\s*([0-9|X]{4})\s*([0-9|X]{4})\s*([0-9|X]{4})\s*([0-9]{4})", normalized_text)

    if not previous_balance_match:
        raise ValueError("Could not find Previous Balance in the PDF text")
    if not current_balance_match:
        raise ValueError("Could not find Current Balance in the PDF text")
    if not date_range_match:
        raise ValueError("Could not find Opening/Closing Date in the PDF text")
    if not account_number_match:
        raise ValueError("Could not find Account Number in the PDF text")

    previous_balance = previous_balance_match.group("amount").replace(",", "")
    current_balance = current_balance_match.group("amount").replace(",", "")
    if previous_balance_match.group("sign") == "-":
        previous_balance = f"-{previous_balance}"
    if current_balance_match.group("sign") == "-":
        current_balance = f"-{current_balance}"

    return {
        "Previous Balance": previous_balance,
        "Current Balance": current_balance,
        "Opening Date": format_sql_date(date_range_match.group(1)),
        "Closing Date": format_sql_date(date_range_match.group(2)),
        "Account Number": account_number_match.group(4) #+ account_number_match.group(2) #+ account_number_match.group(3) + account_number_match.group(4)
    }

def parse_amex_statement(normalized_text):
    """Extract statement details from an American Express PDF statement.

    Returns a dictionary with:
    - Previous Balance
    - Current Balance
    - Closing Date
    - Account Number
    """
    closing_date_match = re.search(r"Closing Date\s*([0-9]{2}/[0-9]{2}/[0-9]{2})", normalized_text)
    account_number_match = re.search(r"Account Ending\s*([0-9]{1}-[0-9]{5})", normalized_text)

    if not closing_date_match:
        raise ValueError("Could not find Closing Date in the PDF text")
    if not account_number_match:
        raise ValueError("Could not find Account Number in the PDF text")

    legacy_summary_match = re.search(
        r"Previous Balance\s+Payments/Credits\s+New Charges\s+Fees\s+Interest Charged\s+(?P<summary>.*?)(?:Closing Date:|Account Ending:|$)",
        normalized_text
    )
    new_summary_match = re.search(
        r"Account Summary\s+Previous Balance\s+Payments/Credits\s+New Charges\s+Fees\s+Interest Charged\s*(?P<summary>.*?)(?:Credit Limit|Cash Advance Limit|$)",
        normalized_text
    )

    if legacy_summary_match:
        summary_text = legacy_summary_match.group("summary")
        amount_matches = re.findall(r"([+-]?)\s*\$?([0-9,]+\.\d{2})", summary_text)
    elif new_summary_match:
        summary_text = new_summary_match.group("summary")
        amount_matches = re.findall(r"([+-]?)\s*\$?([0-9,]+\.\d{2})", summary_text)
    else:
        raise ValueError("Could not find an AMEX summary block in the PDF text")

    if len(amount_matches) < 5:
        raise ValueError("Could not parse the expected five AMEX summary amounts")

    signed_amounts = []
    current_balance = Decimal("0")
    for sign, amount_text in amount_matches[:5]:
        normalized_sign = "-" if sign == "-" else ""
        amount_value = Decimal(amount_text.replace(",", ""))
        if normalized_sign:
            amount_value = -amount_value
        signed_amounts.append(f"{normalized_sign}{amount_value}")
        current_balance += amount_value

    return {
        "Previous Balance": signed_amounts[0],
        "Current Balance": str(current_balance),
        "Closing Date": format_sql_date(closing_date_match.group(1)),
        "Account Number": account_number_match.group(1)
    }


def parse_statement_info(file_name):
    """Extract statement details from a Chase or AMEX PDF statement.

    Returns a dictionary with:
    - Previous Balance
    - Current Balance
    - Opening Date
    - Closing Date
    - Account Number
    """
    if not file_name:
        raise ValueError("A PDF file name or path is required")

    path = file_name
    if not os.path.exists(path):
        local_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(local_path):
            path = local_path
        else:
            raise FileNotFoundError(f"Could not find PDF file: {file_name}")

    if PdfReader is None:
        raise ImportError("pypdf is required to read PDF files")

    reader = PdfReader(path)
    if len(reader.pages) == 0:
        raise ValueError(f"PDF has no pages: {path}")

    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    normalized = re.sub(r"\s+", " ", text)

    chase_match = re.search(r"Chase", normalized)
    amex_match = re.search(r"American Express", normalized)

    if chase_match and amex_match:
        raise ValueError("PDF contains both Chase and American Express text; cannot determine statement type")
    if not chase_match and not amex_match:
        pdb.set_trace()  # Debugging breakpoint
        raise ValueError("PDF does not contain Chase or American Express text; cannot determine statement type")
    
    if chase_match:
        return parse_chase_statement(normalized)
    
    elif amex_match:
        return parse_amex_statement(normalized)


def main():
    parser = argparse.ArgumentParser(description="Parse Chase statement PDF values")
    parser.add_argument("file_name", nargs="?", default="charges_toProcess/chase_20240808.pdf", help="Path to the Chase PDF file")
    args = parser.parse_args()

    info = parse_statement_info(args.file_name)
    print(info)


if __name__ == "__main__":
    main()
