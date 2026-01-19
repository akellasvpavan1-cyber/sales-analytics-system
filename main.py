from utils.file_handler import read_sales_file
from utils.data_processor import (
    clean_sales_data,
    analyze_revenue_by_region,
    validate_and_filter,
    calculate_total_revenue
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

def main():
    # Step 1: Read raw sales file (Q1)
    file_path = "data/sales_data.txt"
    lines = read_sales_file(file_path)

    # Step 2: Clean and parse data (Q1)
    valid_records = clean_sales_data(lines)

    # Step 3: Analytics (Q1 bonus)
    analyze_revenue_by_region(valid_records)

    # Optional: Total revenue (Q3 utility demo)
    total_revenue = calculate_total_revenue(valid_records)
    print(f"\nTotal Revenue: ₹{total_revenue:,.2f}")

    # Step 4: Validation & filtering (Q2)
    filtered_records, invalid_count, summary = validate_and_filter(
        valid_records,
        region="North",
        min_amount=10000
    )

    print("\nFilter Summary:")
    print(summary)

    # Step 5: Fetch API data (Q4)
    api_products = fetch_all_products()
    product_mapping = create_product_mapping(api_products)

    # Step 6: Enrich sales data & save output (Q4)
    enriched_transactions = enrich_sales_data(valid_records, product_mapping)
    save_enriched_data(enriched_transactions)

if __name__ == "__main__":
    main()
