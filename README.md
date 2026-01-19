Sales Analytics System
Overview

This repository contains an end-to-end Python-based Sales Analytics System.
The application demonstrates structured data handling, validation, analytics, API integration, enrichment, and report generation using a clean, modular design.

The project strictly follows separation of concerns, with main.py acting as the orchestration layer and all business logic implemented within reusable utility modules.

In addition to the core requirements, the solution includes bonus analytical components to provide deeper business insights.

Project Structure
sales-analytics-system/

├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
└── utils/
    ├── __init__.py
    ├── file_handler.py
    ├── data_processor.py
    ├── api_handler.py
    └── report_generator.py

Features Implemented
1. File Handling and Preprocessing

Reads sales data from a text file with encoding safety

Handles malformed rows and inconsistent formatting

Cleans numeric fields containing commas

Converts data to appropriate types

Prints a clear summary of total, invalid, and valid records

2. Data Validation and Filtering

Applies validation rules on quantity and pricing

Supports optional filtering by region and transaction amount

Outputs a structured validation and filter summary

3. Core Sales Analytics

Total revenue calculation

Region-wise revenue analysis

Product-level sales aggregation

Customer-level revenue analysis

Date-based transaction trends

4. Bonus Analytics (Additional Insights)

Peak sales day identification

Low-performing product detection using quantity thresholds

Average transaction value analysis by region

Reuse of analytical outputs inside the final report

5. API Integration and Data Enrichment

Fetches product metadata from a public API

Implements retry logic and timeout handling

Creates an efficient product ID mapping

Enriches sales transactions with:

Product title

Category

Brand

Rating

Gracefully handles missing or unavailable API data

Saves enriched output to a separate data file

6. Report Generation

Generates a comprehensive, formatted text report containing:

Header with generation timestamp

Overall sales summary

Region-wise performance table

Top products and customers

Daily sales trends

Product performance analysis

API enrichment summary

7. Main Application Flow

Centralized execution via main.py

No business logic inside the main script

Sequential execution of all processing stages

End-to-end execution without crashes, even on API failure

How to Run the Project
Prerequisites

Python 3.9 or higher

Internet access (required for API enrichment)

Setup and Execution
pip install -r requirements.txt
python main.py

Output Files
data/enriched_sales_data.txt

Contains sales transactions enriched with external product metadata.

output/sales_report.txt

Contains the final formatted sales analytics report with all required sections.

Dependencies

The project uses the following external library:

requests — for API integration

All dependencies are listed in requirements.txt.

Design Notes

Business logic is fully modularized under the utils directory

main.py is used strictly for orchestration

Defensive programming practices are applied throughout

API failures do not break the execution flow

The structure is optimized for readability, evaluation, and extensibility

Status

All required assignment sections are implemented

Bonus analytics are included and integrated

The application runs end-to-end successfully

All required output files are generated correctly

Author

Pavan Akella
