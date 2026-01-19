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
from utils.report_generator import generate_sales_report


def main():
    try:
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # Step 1: Read raw sales file (Q1)
        file_path = "data/sales_data.txt"
        lines = read_sales_file(file_path)

        # Step 2: Clean and parse data (Q1)
        valid_records = clean_sales_data(lines)

        # Step 3: Analytics (Q1 bonus)
        analyze_revenue_by_region(valid_records)

        # Step 4: Total revenue calculation (Q3)
        total_revenue = calculate_total_revenue(valid_records)
        print(f"\nTotal Revenue: ₹{total_revenue:,.2f}")

        # Step 5: User interaction for filtering (Q5 requirement)
        print("\nFilter Options Available:")
        print("- Regions: North, South, East, West")
        print("- Minimum transaction amount")

        apply_filter = input("Do you want to apply filters? (y/n): ").strip().lower()

        if apply_filter == "y":
            filtered_records, invalid_count, summary = validate_and_filter(
                valid_records,
                region="North",
                min_amount=10000
            )
            print("\nFilter Summary:")
            print(summary)
            records_to_use = filtered_records
        else:
            print("\nSkipping filters. Using all valid records.")
            records_to_use = valid_records

        # Step 6: Fetch API data (Q4)
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)

        # Step 7: Enrich sales data & save output (Q4)
        enriched_transactions = enrich_sales_data(records_to_use, product_mapping)
        save_enriched_data(enriched_transactions)

        # Step 8: Generate comprehensive sales report (Q5)
        generate_sales_report(records_to_use, enriched_transactions)
        print("\nSales report generated at output/sales_report.txt")
        print("Process completed successfully.")

    except Exception as e:
        print("An unexpected error occurred during execution:")
        print(e)


if __name__ == "__main__":
    main()
