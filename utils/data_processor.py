def clean_sales_data(lines):
    total_records = 0
    invalid_records = 0
    valid_records = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        total_records += 1
        parts = line.split('|')

        if len(parts) != 8:
            invalid_records += 1
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        product_name = product_name.replace(',', '')
        quantity = quantity.replace(',', '')
        unit_price = unit_price.replace(',', '')

        if not transaction_id.startswith('T'):
            invalid_records += 1
            continue

        if not customer_id or not region:
            invalid_records += 1
            continue

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            invalid_records += 1
            continue

        if quantity <= 0 or unit_price <= 0:
            invalid_records += 1
            continue

        valid_records.append({
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        })

    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records

def analyze_revenue_by_region(valid_records):
    revenue_by_region = {}

    for record in valid_records:
        region = record["Region"]
        revenue = record["Quantity"] * record["UnitPrice"]

        if region not in revenue_by_region:
            revenue_by_region[region] = 0

        revenue_by_region[region] += revenue

    print("\nRevenue by Region:")
    for region, total in revenue_by_region.items():
       print(f"{region}: ₹{total:,.2f}")

# Q2: Data Validation and Filtering
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    for tx in transactions:
        # Calculate transaction amount
        amount = tx["Quantity"] * tx["UnitPrice"]

        # Validation rules
        if tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0:
            invalid_count += 1
            continue

        # Optional filters
        if region and tx["Region"] != region:
            continue

        if min_amount and amount < min_amount:
            continue

        if max_amount and amount > max_amount:
            continue

        valid_transactions.append(tx)

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary
