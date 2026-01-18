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

def calculate_total_revenue(transactions):
    total_revenue = 0.0
    for tx in transactions:
        total_revenue += tx["Quantity"] * tx["UnitPrice"]
    return total_revenue


def region_wise_sales(transactions):
    region_sales = {}

    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_sales:
            region_sales[region] = 0.0

        region_sales[region] += revenue

    return region_sales

def top_selling_products(transactions, n=5):
    product_revenue = {}

    for tx in transactions:
        product = tx["ProductName"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_revenue:
            product_revenue[product] = 0.0

        product_revenue[product] += revenue

    sorted_products = sorted(
        product_revenue.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_products[:n]

def customer_analysis(transactions):
    customer_revenue = {}

    for tx in transactions:
        customer = tx["CustomerID"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if customer not in customer_revenue:
            customer_revenue[customer] = 0.0

        customer_revenue[customer] += revenue

    return customer_revenue
def daily_sales_trend(transactions):
    daily_trend = {}

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily_trend:
            daily_trend[date] = {
                "revenue": 0.0,
                "transactions": 0
            }

        daily_trend[date]["revenue"] += revenue
        daily_trend[date]["transactions"] += 1

    return dict(sorted(daily_trend.items()))


def find_peak_sales_day(transactions):
    daily_trend = daily_sales_trend(transactions)

    peak_day = None
    max_revenue = 0.0

    for date, data in daily_trend.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            peak_day = date

    return (peak_day, max_revenue)

def low_performing_products(transactions, threshold=10):
    product_quantity = {}

    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]

        if product not in product_quantity:
            product_quantity[product] = 0

        product_quantity[product] += quantity

    low_performers = [
        (product, qty)
        for product, qty in product_quantity.items()
        if qty < threshold
    ]

    return sorted(low_performers, key=lambda x: x[1])
