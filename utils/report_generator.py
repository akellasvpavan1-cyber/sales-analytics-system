from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_revenue = sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)
    total_tx = len(transactions)
    avg_order = total_revenue / total_tx if total_tx else 0

    dates = sorted(tx["Date"] for tx in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    # Region-wise
    region_data = {}
    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        region_data.setdefault(region, {"revenue": 0, "count": 0})
        region_data[region]["revenue"] += revenue
        region_data[region]["count"] += 1

    # Products
    product_data = {}
    for tx in transactions:
        p = tx["ProductName"]
        product_data.setdefault(p, {"qty": 0, "revenue": 0})
        product_data[p]["qty"] += tx["Quantity"]
        product_data[p]["revenue"] += tx["Quantity"] * tx["UnitPrice"]

    top_products = sorted(product_data.items(), key=lambda x: x[1]["revenue"], reverse=True)[:5]

    # Customers
    customer_data = {}
    for tx in transactions:
        c = tx["CustomerID"]
        customer_data.setdefault(c, {"spent": 0, "orders": 0})
        customer_data[c]["spent"] += tx["Quantity"] * tx["UnitPrice"]
        customer_data[c]["orders"] += 1

    top_customers = sorted(customer_data.items(), key=lambda x: x[1]["spent"], reverse=True)[:5]

    # Daily trend
    daily = {}
    for tx in transactions:
        d = tx["Date"]
        daily.setdefault(d, {"revenue": 0, "count": 0, "customers": set()})
        daily[d]["revenue"] += tx["Quantity"] * tx["UnitPrice"]
        daily[d]["count"] += 1
        daily[d]["customers"].add(tx["CustomerID"])

    best_day = max(daily.items(), key=lambda x: x[1]["revenue"])[0]

    # API enrichment
    enriched = [tx for tx in enriched_transactions if tx.get("API_Match")]
    failed = [tx["ProductName"] for tx in enriched_transactions if not tx.get("API_Match")]
    success_rate = (len(enriched) / len(enriched_transactions)) * 100 if enriched_transactions else 0

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("="*50 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Records Processed: {total_tx}\n")
        f.write("="*50 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_tx}\n")
        f.write(f"Average Order Value: ₹{avg_order:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        for r, v in sorted(region_data.items(), key=lambda x: x[1]["revenue"], reverse=True):
            pct = (v["revenue"] / total_revenue) * 100
            f.write(f"{r} | ₹{v['revenue']:,.2f} | {pct:.2f}% | {v['count']}\n")

        f.write("\nTOP 5 PRODUCTS\n")
        for i, (p, v) in enumerate(top_products, 1):
            f.write(f"{i}. {p} | Qty: {v['qty']} | ₹{v['revenue']:,.2f}\n")

        f.write("\nTOP 5 CUSTOMERS\n")
        for i, (c, v) in enumerate(top_customers, 1):
            f.write(f"{i}. {c} | ₹{v['spent']:,.2f} | Orders: {v['orders']}\n")

        f.write("\nDAILY SALES TREND\n")
        for d, v in sorted(daily.items()):
            f.write(f"{d} | ₹{v['revenue']:,.2f} | {v['count']} | {len(v['customers'])}\n")

        f.write("\nPRODUCT PERFORMANCE ANALYSIS\n")
        f.write(f"Best Selling Day: {best_day}\n")

        f.write("\nAPI ENRICHMENT SUMMARY\n")
        f.write(f"Total Products Enriched: {len(enriched)}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        if failed:
            f.write("Failed Products:\n")
            for p in set(failed):
                f.write(f"- {p}\n")