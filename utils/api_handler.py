import requests
import time


# -----------------------------
# Task 3.1 — Fetch API Products
# -----------------------------
def fetch_all_products():
    """
    Fetches product data from DummyJSON API.
    Retries up to 3 times on failure.
    Returns list of products or empty list on failure.
    """
    url = "https://dummyjson.com/products?limit=100"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            products = data.get("products", [])
            print(f"Fetched {len(products)} products from API")
            return products
        except Exception as e:
            print(f"API attempt {attempt + 1} failed: {e}")
            time.sleep(1)

    print("Failed to fetch products after retries. Proceeding without API enrichment.")
    return []


# ---------------------------------
# Task 3.1 — Create Product Mapping
# ---------------------------------
def create_product_mapping(api_products):
    """
    Converts API product list into a mapping keyed by product ID.
    """
    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is None:
            continue

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
        }

    return product_mapping


# ---------------------------------
# Task 3.2 — Enrich Sales Data
# ---------------------------------
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches sales transactions using API product metadata.
    """
    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        # Extract numeric ID: "P101" → 101
        product_id_raw = tx.get("ProductID", "")
        try:
            product_id = int(product_id_raw.replace("P", ""))
        except ValueError:
            product_id = None

        if product_id in product_mapping:
            api_data = product_mapping[product_id]
            enriched_tx["API_Title"] = api_data["title"]
            enriched_tx["API_Category"] = api_data["category"]
            enriched_tx["API_Brand"] = api_data["brand"]
            enriched_tx["API_Rating"] = api_data["rating"]
            enriched_tx["API_Match"] = True
        else:
            enriched_tx["API_Title"] = None
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched_transactions.append(enriched_tx)

    return enriched_transactions


# ---------------------------------
# Task 3.2 — Save Enriched Data
# ---------------------------------
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to pipe-separated text file.
    """
    if not enriched_transactions:
        print("No enriched data to save.")
        return

    headers = list(enriched_transactions[0].keys())

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = [
                str(tx.get(col, "")) if tx.get(col) is not None else ""
                for col in headers
            ]
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
