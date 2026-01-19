# Sales Analytics System (Assignment 3)

Student Name: Agnik Banerjee
Student ID: bitsom_ba_25071681
Email: agnik631@gmail.com
Date: January 20, 2026

--------------------------------------------------------------------

1. Project Overview
This project implements a Sales Analytics System that reads sales transactions from a text file, cleans and validates the data, performs analytics, enriches sales records using an external API (DummyJSON), and generates a detailed sales report.

The complete solution is implemented using Python and follows a modular structure using utility modules inside the utils/ folder.

--------------------------------------------------------------------

2. Folder Structure
sales-analytics-system/
  README.md
  main.py
  utils/
    file_handler.py
    data_processor.py
    api_handler.py
    __init__.py
  data/
    sales_data.txt
    enriched_sales_data.txt   (generated after execution)
  output/
    sales_report.txt          (generated after execution)
  requirements.txt

--------------------------------------------------------------------

3. Input File Format
Input file location:
data/sales_data.txt

Header format (must be present):
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region

Example:
T001|2024-01-01|P101|Laptop|2|50000|C001|North

--------------------------------------------------------------------

4. Modules and Functionalities

4.1 File Handling & Data Cleaning (utils/file_handler.py)
- Reads sales records from data/sales_data.txt
- Handles encoding issues using: utf-8, latin-1, cp1252
- Skips header row and ignores empty lines
- Parses records separated by "|"
- Removes commas from ProductName when present (example: Mouse,Wireless)
- Removes commas from numeric fields when present (example: 1,916)
- Converts Quantity to int and UnitPrice to float

4.2 Data Validation and Filtering
Validation rules:
- Quantity must be greater than 0
- UnitPrice must be greater than 0
- CustomerID and Region must not be empty
- TransactionID must start with "T"
- ProductID must start with "P"
- CustomerID must start with "C"

Filtering supported:
- Region filter (example: North/South/East/West)
- Minimum transaction amount filter
- Maximum transaction amount filter

4.3 Sales Data Analytics (utils/data_processor.py)
The following analytics are performed:
- Total revenue calculation
- Region-wise sales performance (sales, % contribution, transaction count)
- Top 5 selling products (by quantity sold)
- Customer analysis:
  - total spent
  - purchase count
  - average order value
  - products bought
- Daily sales trend:
  - transaction count per day
  - unique customers per day
- Peak sales day (highest revenue day)
- Low performing products (products with quantity sold below threshold)

4.4 API Integration and Product Enrichment (utils/api_handler.py)
- Fetches products from DummyJSON API:
  https://dummyjson.com/products?limit=100
- Creates a product mapping of ProductID to:
  - title
  - brand
  - category
  - rating
- Enriches sales transactions with product details
- Saves enriched output to:
  data/enriched_sales_data.txt

Note:
If internet is not available, API fetch may fail but the program will still run and generate the report.

4.5 Report Generation
A final report is generated at:
output/sales_report.txt

Report sections include:
- Overall summary (total revenue, total transactions, average order value, date range)
- Region-wise performance table
- Top 5 products table
- Top 5 customers table
- Daily sales trend table
- Peak sales day summary
- Enrichment success summary

--------------------------------------------------------------------

5. How to Run the Project (Local System)

Step 1: Install dependencies
pip install -r requirements.txt

Step 2: Run the project
python main.py

Step 3: Provide input when asked
Do you want to filter data? (y/n):

- Enter n to run without filtering
- Enter y to apply filters (region / min amount / max amount)

--------------------------------------------------------------------

6. How to Run the Project in Google Colab (Virtual Execution)

Step 1: Open Google Colab and create a new notebook

Step 2: Upload the project ZIP file
sales-analytics-system.zip

Step 3: Extract the ZIP
!unzip -o sales-analytics-system.zip

Step 4: Go inside the project folder
%cd sales-analytics-system

Step 5: Install dependencies
!pip install -r requirements.txt

Step 6: Run the program
!python main.py

Step 7: Download Output Files

Download report:
from google.colab import files
files.download("output/sales_report.txt")

Download enriched data:
from google.colab import files
files.download("data/enriched_sales_data.txt")

--------------------------------------------------------------------

7. Output Files Generated

1) Enriched File:
data/enriched_sales_data.txt

2) Final Report:
output/sales_report.txt

--------------------------------------------------------------------

8. Conclusion
This project successfully:
- Reads and cleans sales transaction data
- Validates and filters invalid records
- Performs sales analytics calculations
- Enriches product information using API
- Generates a complete sales report and enriched dataset output
