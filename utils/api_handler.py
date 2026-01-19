import requests

API_URL = "https://dummyjson.com/products?limit=100"


def fetch_all_products():
    """
    Fetch product data from DummyJSON API.
    Returns a list of products or [] on failure.
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])
        print(f"Fetched {len(products)} products from API")
        return products
    except Exception as e:
        print(f"Failed to fetch products from API: {e}")
        return []


def create_product_mapping(api_products):
    """
    Create a mapping of product_id -> selected product details
    """
    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is None:
            continue

        product_mapping[int(product_id)] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
        }

    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enrich sales transactions using API product data.
    """
    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        # Extract numeric product ID (e.g., P101 -> 101)
        product_id_str = tx.get("ProductID", "")
        try:
            product_id = int(product_id_str.replace("P", ""))
        except ValueError:
            product_id = None

        if product_id and product_id in product_mapping:
            api_data = product_mapping[product_id]
            enriched_tx.update(api_data)
            enriched_tx["API_Match"] = True
        else:
            enriched_tx.update({
                "title": None,
                "category": None,
                "brand": None,
                "rating": None,
                "API_Match": False
            })

        enriched_transactions.append(enriched_tx)

    return enriched_transactions


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Save enriched sales data to a pipe-separated file.
    """
    if not enriched_transactions:
        print("No enriched data to save.")
        return

    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "title", "category", "brand", "rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = []
            for header in headers:
                value = tx.get(header)
                row.append("" if value is None else str(value))
            file.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
