# utils/api_handler.py

import requests


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: List of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print("✓ Successfully fetched products from API")
        return products

    except Exception as e:
        print(f"✗ API fetch failed: {e}")
        return []


def create_product_mapping(all_products):
    """
    Creates a mapping of product ID to product info
    """
    mapping = {}

    for p in all_products:
        pid = p.get("id")
        if pid is None:
            continue

        mapping[pid] = {
            "title": p.get("title"),
            "category": p.get("category"),
            "brand": p.get("brand"),
            "rating": p.get("rating")
        }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with product information
    Saves enriched data to a new file
    """
    enriched_transactions = []

    for t in transactions:
        try:
            # Extract numeric product id from P101 -> 101
            prod_raw = t["ProductID"].replace("P", "")
            prod_id = int(prod_raw)

            base = {
                "transactionID": t["TransactionID"],
                "productID": prod_id,
                "productName": t["ProductName"],
                "quantity": t["Quantity"],
                "customer": t["CustomerID"]
            }

            if prod_id in product_mapping:
                info = product_mapping[prod_id]
                base.update({
                    "rating": info.get("rating"),
                    "category": info.get("category"),
                    "brand": info.get("brand"),
                    "title": info.get("title"),
                    "enriched": True
                })
            else:
                base.update({
                    "rating": None,
                    "category": None,
                    "brand": None,
                    "title": None,
                    "enriched": False
                })

            enriched_transactions.append(base)

        except:
            enriched_transactions.append({
                "transactionID": t.get("TransactionID"),
                "productID": None,
                "productName": t.get("ProductName"),
                "quantity": t.get("Quantity"),
                "customer": t.get("CustomerID"),
                "rating": None,
                "category": None,
                "brand": None,
                "title": None,
                "enriched": False
            })

    save_enriched_data(enriched_transactions)
    return enriched_transactions


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    header = "transactionID|productID|productName|quantity|customer|rating|brand|category|title|enriched\n"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(header)
            for t in enriched_transactions:
                line = (
                    f"{t.get('transactionID')}|{t.get('productID')}|{t.get('productName')}|"
                    f"{t.get('quantity')}|{t.get('customer')}|{t.get('rating')}|"
                    f"{t.get('brand')}|{t.get('category')}|{t.get('title')}|{t.get('enriched')}\n"
                )
                f.write(line)

    except Exception as e:
        print(f"Error writing enriched file: {e}")
