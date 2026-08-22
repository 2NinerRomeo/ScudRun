import os
from typing import List, Dict, Any

from parse_card_statement import parse_statement_info


def sanitize_root_dir(root_dir: str) -> str:
    """Normalize a directory path and reject the common trailing-slash escape case."""
    if not root_dir:
        raise ValueError("A directory path is required")

    cleaned = root_dir.strip().rstrip("\\/")

    if cleaned.endswith('"') or cleaned.endswith("'"):
        raise ValueError(
            f"Invalid path: '{root_dir}'. Remove the trailing backslash or quote escape and try again."
        )

    return cleaned


def find_statement_pdfs(root_dir: str) -> List[str]:
    """Recursively find .pdf files under the given directory."""
    sanitized_root = sanitize_root_dir(root_dir)

    pdf_files = []
    for current_root, _, files in os.walk(sanitized_root):
        for filename in files:
            #print(f"Checking file: {os.path.join(current_root, filename)}")
            if filename.lower().endswith(".pdf"):
                #print(f"Found PDF file: {os.path.join(current_root, filename)}")
                pdf_files.append(os.path.join(current_root, filename))

    if not pdf_files:
        print(f"No PDF statement files were found under: {sanitized_root}")

    print(f"Found {len(pdf_files)} PDF files under {sanitized_root}")
    return sorted(pdf_files)


def parse_statement_files(root_dir: str) -> List[Dict[str, Any]]:
    """Parse all statement PDFs under the directory and return the dictionaries sorted by Closing Date."""
    statements = []
    for pdf_path in find_statement_pdfs(root_dir):
        print(f"Parsing statement PDF: {pdf_path}")
        parsed = parse_statement_info(pdf_path)
        statements.append(parsed)

    # Sort by closing date in SQL format so the statements are in chronological order.
    return sorted(statements, key=lambda item: item.get("Closing Date", "0000-00-00"))


def preview_statements(root_dir: str) -> List[Dict[str, str]]:
    """Return a compact list of account numbers and closing dates for the parsed statements."""
    preview = []
    for statement in parse_statement_files(root_dir):
        preview.append({
            "Account Number": statement.get("Account Number", ""),
            "Closing Date": statement.get("Closing Date", "")
        })
    return preview


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find statement PDFs recursively and parse them.")
    parser.add_argument("root_dir", help="Root directory to search for PDF statements")
    parser.add_argument("--preview", action="store_true", help="Display account numbers and closing dates only")
    args = parser.parse_args()

    if args.preview:
        for statement in preview_statements(args.root_dir):
            print(f"{statement['Account Number']} | {statement['Closing Date']}")
    else:
        for statement in parse_statement_files(args.root_dir):
            print(statement)
