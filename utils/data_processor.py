# utils/data_processor.py

def calculate_total_revenue(transactions):
    total = 0.0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total


def region_wise_sales(transactions):
    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in region_stats:
            region_stats[region] = {"total_sales": 0.0, "transaction_count": 0}

        region_stats[region]["total_sales"] += amount
        region_stats[region]["transaction_count"] += 1

    for r in region_stats:
        region_stats[r]["percentage"] = (region_stats[r]["total_sales"] / total_revenue) * 100 if total_revenue else 0

    # Sort by total_sales descending
    sorted_regions = dict(sorted(region_stats.items(), key=lambda x: x[1]["total_sales"], reverse=True))
    return sorted_regions


def top_selling_products(transactions, n=5):
    product_stats = {}

    for t in transactions:
        product = t["ProductName"]
        qty = t["Quantity"]
        revenue = t["Quantity"] * t["UnitPrice"]

        if product not in product_stats:
            product_stats[product] = {"qty": 0, "revenue": 0.0}

        product_stats[product]["qty"] += qty
        product_stats[product]["revenue"] += revenue

    result = []
    for p in product_stats:
        result.append((p, product_stats[p]["qty"], product_stats[p]["revenue"]))

    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]


def customer_analysis(transactions):
    customer_stats = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]
        product = t["ProductName"]

        if cid not in customer_stats:
            customer_stats[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_stats[cid]["total_spent"] += amount
        customer_stats[cid]["purchase_count"] += 1
        customer_stats[cid]["products_bought"].add(product)

    final = {}
    for cid in customer_stats:
        total_spent = customer_stats[cid]["total_spent"]
        count = customer_stats[cid]["purchase_count"]
        final[cid] = {
            "total_spent": total_spent,
            "purchase_count": count,
            "average_value": total_spent / count if count else 0,
            "products_bought": sorted(list(customer_stats[cid]["products_bought"]))
        }

    # Sort by total_spent descending
    sorted_customers = dict(sorted(final.items(), key=lambda x: x[1]["total_spent"], reverse=True))
    return sorted_customers


def daily_sales_trend(transactions):
    trend = {}

    for t in transactions:
        date = t["Date"]
        cid = t["CustomerID"]

        if date not in trend:
            trend[date] = {"transaction_count": 0, "unique_customers": set()}

        trend[date]["transaction_count"] += 1
        trend[date]["unique_customers"].add(cid)

    # Convert unique_customers set to count
    result = {}
    for d in sorted(trend.keys()):
        result[d] = {
            "transaction_count": trend[d]["transaction_count"],
            "unique_customers": len(trend[d]["unique_customers"])
        }

    return result


def find_peak_sales_day(transactions):
    daily_revenue = {}
    daily_count = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]

        daily_revenue[date] = daily_revenue.get(date, 0.0) + amount
        daily_count[date] = daily_count.get(date, 0) + 1

    peak_date = max(daily_revenue, key=daily_revenue.get)
    return (peak_date, daily_revenue[peak_date], daily_count[peak_date])


def low_performing_products(transactions, threshold=10):
    product_stats = {}

    for t in transactions:
        product = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if product not in product_stats:
            product_stats[product] = {"qty": 0, "revenue": 0.0}

        product_stats[product]["qty"] += qty
        product_stats[product]["revenue"] += revenue

    low_products = []
    for p in product_stats:
        if product_stats[p]["qty"] < threshold:
            low_products.append((p, product_stats[p]["qty"], product_stats[p]["revenue"]))

    low_products.sort(key=lambda x: x[1])
    return low_products
