from utils.file_handler import read_sales_file
from utils.data_processor import clean_sales_data, analyze_revenue_by_region

def main():
    file_path = "data/sales_data.txt"
    lines = read_sales_file(file_path)
    valid_records = clean_sales_data(lines)
    analyze_revenue_by_region(valid_records)

if __name__ == "__main__":
    main()