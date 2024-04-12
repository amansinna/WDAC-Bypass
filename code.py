import re

def extract_product_id(url):
    # Use regular expression to extract product ID
    match = re.search(r'product::(\d+)/', url)
    if match:
        return match.group(1)
    else:
        return None

def fetch_product_ids(urls):
    product_ids = []
    for url in urls:
        product_id = extract_product_id(url)
        if product_id:
            product_ids.append(product_id)
    return product_ids

# Sample list of URLs
urls = [
    "http://spr2.site.samp.com/#/product/product::1150/summary",
    "http://spr2.site.samp.com/#/product/product::1200/details",
    "http://spr2.site.samp.com/#/product/product::1234/info"
]

# Fetch product IDs
product_ids = fetch_product_ids(urls)

# Print the extracted product IDs
print("Product IDs:")
for product_id in product_ids:
    print(product_id)
