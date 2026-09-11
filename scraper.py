import csv
import requests
from bs4 import BeautifulSoup

# 1. Target URL
url = "http://books.toscrape.com/"

# 2. Fetch page content
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
response = requests.get(url, headers=headers)

# 3. Check status and extract data
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    scraped_data = []

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.replace("£", "$")
        availability = book.find("p", class_="instock availability").text.strip()

        scraped_data.append(
            {"Title": title, "Price": price, "Status": availability}
        )

    # 4. Save to CSV
    csv_file = "scraped_books_data.csv"
    fieldnames = ["Title", "Price", "Status"]

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scraped_data)

    print(
        f"Success! {len(scraped_data)} items extracted and saved to {csv_file}"
    )

else:
    print(f"Failed to fetch page. Status code: {response.status_code}")