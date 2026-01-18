from utils.file_handler import read_sales_file
from utils.data_processor import (
    clean_sales_data,
    analyze_revenue_by_region,
    validate_and_filter,
    calculate_total_revenue
)

def main():
    # Step 1: Read raw file
    file_path = "data/sales_data.txt"
    lines = read_sales_file(file_path)

    # Step 2: Clean and parse data (Q1)
    valid_records = clean_sales_data(lines)

    # Step 3: Analytics (Q1 bonus)
    analyze_revenue_by_region(valid_records)

    # Optional: Total revenue (Q3 demo)
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

if __name__ == "__main__":
    main()
