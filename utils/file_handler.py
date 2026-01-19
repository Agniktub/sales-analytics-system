# utils/file_handler.py

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()

            # Skip header and remove empty lines
            raw_lines = []
            for line in lines[1:]:
                line = line.strip()
                if line:
                    raw_lines.append(line)

            return raw_lines

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    Returns: list of dictionaries with keys:
    ['TransactionID','Date','ProductID','ProductName',
     'Quantity','UnitPrice','CustomerID','Region']
    """
    transactions = []
    expected_fields = 8

    for line in raw_lines:
        parts = line.split("|")

        if len(parts) != expected_fields:
            continue

        transaction_id, date, product_id, product_name, qty, price, customer_id, region = parts

        # Handle commas in ProductName
        product_name = product_name.replace(",", "")

        # Handle commas in numbers
        qty = qty.replace(",", "")
        price = price.replace(",", "")

        try:
            qty = int(qty)
            price = float(price)
        except:
            continue

        transactions.append({
            "TransactionID": transaction_id.strip(),
            "Date": date.strip(),
            "ProductID": product_id.strip(),
            "ProductName": product_name.strip(),
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": customer_id.strip(),
            "Region": region.strip()
        })

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Returns:
    Tuple (valid_transactions, invalid_count, filter_summary)
    """
    total_input = len(transactions)
    invalid_count = 0
    valid_transactions = []

    # Available regions
    regions = sorted(set([t.get("Region", "").strip() for t in transactions if t.get("Region", "").strip()]))
    print("Available Regions:", regions)

    # Transaction amount range
    amounts = []
    for t in transactions:
        try:
            amounts.append(t["Quantity"] * t["UnitPrice"])
        except:
            pass

    if amounts:
        print("Transaction Amount Range:", min(amounts), "to", max(amounts))

    # Validation
    for t in transactions:
        try:
            if (
                not t.get("CustomerID") or not t.get("Region") or
                t["Quantity"] <= 0 or
                t["UnitPrice"] <= 0 or
                not t["TransactionID"].startswith("T") or
                not t["ProductID"].startswith("P") or
                not t["CustomerID"].startswith("C")
            ):
                invalid_count += 1
                continue

            valid_transactions.append(t)

        except:
            invalid_count += 1

    filtered_by_region = 0
    filtered_by_amount = 0

    # Apply region filter
    if region:
        before = len(valid_transactions)
        valid_transactions = [t for t in valid_transactions if t["Region"].lower() == region.lower()]
        filtered_by_region = before - len(valid_transactions)
        print(f"After region filter ({region}): {len(valid_transactions)}")

    # Apply amount filters
    if min_amount is not None:
        before = len(valid_transactions)
        valid_transactions = [t for t in valid_transactions if (t["Quantity"] * t["UnitPrice"]) >= min_amount]
        filtered_by_amount += before - len(valid_transactions)
        print(f"After min amount filter ({min_amount}): {len(valid_transactions)}")

    if max_amount is not None:
        before = len(valid_transactions)
        valid_transactions = [t for t in valid_transactions if (t["Quantity"] * t["UnitPrice"]) <= max_amount]
        filtered_by_amount += before - len(valid_transactions)
        print(f"After max amount filter ({max_amount}): {len(valid_transactions)}")

    summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary
