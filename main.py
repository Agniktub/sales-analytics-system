# main.py

from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data
from datetime import datetime
from pathlib import Path


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order = total_revenue / total_transactions if total_transactions else 0

    dates = sorted([t["Date"] for t in transactions])
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, n=5)

    customers = customer_analysis(transactions)
    top_customers_list = list(customers.items())[:5]

    daily_trend = daily_sales_trend(transactions)
    peak_day, peak_rev, peak_count = find_peak_sales_day(transactions)

    enriched_success = sum(1 for t in enriched_transactions if t.get("enriched") is True)
    total_enriched = len(enriched_transactions)
    success_rate = (enriched_success / total_enriched) * 100 if total_enriched else 0

    not_enriched_products = sorted(set([t.get("productName") for t in enriched_transactions if not t.get("enriched")]))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("========================================\n")
        f.write("        SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Records Processed: {total_transactions}\n")
        f.write("========================================\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("----------------------------------------\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("----------------------------------------\n")
        f.write(f"{'Region':10} {'Sales':12} {'% of Total':10} {'Transactions'}\n")
        for r, stats in region_stats.items():
            f.write(f"{r:10} ₹{stats['total_sales']:,.0f}   {stats['percentage']:.2f}%      {stats['transaction_count']}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("----------------------------------------\n")
        f.write(f"{'Rank':5} {'Product Name':20} {'Qty Sold':10} {'Revenue'}\n")
        for i, (name, qty, rev) in enumerate(top_products, start=1):
            f.write(f"{i:<5} {name:20} {qty:<10} ₹{rev:,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("----------------------------------------\n")
        f.write(f"{'Rank':5} {'Customer ID':12} {'Total Spent':15} {'Order Count'}\n")
        for i, (cid, stats) in enumerate(top_customers_list, start=1):
            f.write(f"{i:<5} {cid:12} ₹{stats['total_spent']:,.2f}     {stats['purchase_count']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("----------------------------------------\n")
        f.write(f"{'Date':12} {'Transactions':12} {'Unique Customers'}\n")
        for d, stats in daily_trend.items():
            f.write(f"{d:12} {stats['transaction_count']:<12} {stats['unique_customers']}\n")
        f.write("\n")

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("----------------------------------------\n")
        f.write(f"Best selling day: {peak_day} | Revenue: ₹{peak_rev:,.2f} | Transactions: {peak_count}\n\n")

        f.write("ENRICHMENT SUMMARY\n")
        f.write("----------------------------------------\n")
        f.write(f"Total products enriched: {enriched_success}/{total_enriched}\n")
        f.write(f"Success rate: {success_rate:.2f}%\n")
        f.write("Products that couldn't be enriched:\n")
        for p in not_enriched_products:
            f.write(f"- {p}\n")


def main():
    try:
        print("=====================================")
        print("SALES ANALYTICS SYSTEM")
        print("=====================================\n")

        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions\n")

        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records\n")

        want_filter = input("Do you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amount = None
        max_amount = None

        if want_filter == "y":
            region = input("Enter region (or leave blank): ").strip()
            region = region if region else None

            min_amt = input("Enter minimum amount (or leave blank): ").strip()
            min_amount = float(min_amt) if min_amt else None

            max_amt = input("Enter maximum amount (or leave blank): ").strip()
            max_amount = float(max_amt) if max_amt else None

        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions, region=region, min_amount=min_amount, max_amount=max_amount
        )
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}\n")

        print("[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions)
        print("✓ Analysis complete\n")

        print("[6/10] Fetching product data from API...")
        products = fetch_all_products()
        print(f"✓ Fetched {len(products)} products\n")

        product_mapping = create_product_mapping(products)

        print("[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        enriched_success = sum(1 for t in enriched_transactions if t.get("enriched"))
        print(f"✓ Enriched {enriched_success}/{len(valid_transactions)} transactions\n")

        print("[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        Path("output").mkdir(exist_ok=True)
        print("[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt\n")

        print("[10/10] Process Complete!")
        print("=====================================")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
