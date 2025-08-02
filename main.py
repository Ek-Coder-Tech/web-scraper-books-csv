import requests
from bs4 import BeautifulSoup
import csv
print("📡 Fetching data from: http://books.toscrape.com")

base_url = "http://books.toscrape.com/catalogue/page-{}.html"
all_books = []

for page in range(1, 51):  # 50 pages × 20 books = 1,000 books
    url = base_url.format(page)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"⚠️ Failed to retrieve page {page}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.select("article.product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.strip()
        availability = book.select_one(".availability").text.strip()

        all_books.append({
            "title": title,
            "price": price,
            "availability": availability
        })

    print(f"✅ Page {page} scraped successfully.")

# ✅ Export to CSV
with open("books_data.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Availability"])  # Header

    for book in all_books:
        writer.writerow([book["title"], book["price"], book["availability"]])

print("📁 books_data.csv created successfully with", len(all_books), "books.")
