"""
import requests
from lxml import html
import csv

URL = "https://books.toscrape.com/"

response = requests.get(URL)
tree = html.fromstring(response.content)

books = tree.xpath('//article[@class="product_pod"]')

with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Price', 'Stock', 'Rating', 'Detail Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for book in books:
        title = book.xpath('.//h3/a/@title')[0]
        price = book.xpath('.//p[@class="price_color"]/text()')[0]
        stock_raw = book.xpath('.//p[contains(@class, "instock")]/text()')
        # Stock availability has whitespace text nodes, filter them
        stock = ''.join([s.strip() for s in stock_raw if s.strip() != ''])
        rating_class = book.xpath('.//p[contains(@class, "star-rating")]/@class')[0]
        # rating_class example: 'star-rating Three' -> extract 'Three'
        rating = rating_class.split()[-1]
        detail_link = book.xpath('.//h3/a/@href')[0]

        writer.writerow({
            'Title': title,
            'Price': price,
            'Stock': stock,
            'Rating': rating,
            'Detail Link': detail_link
        })
"""

import scrapy
import pandas as pd

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = []
        for book in response.xpath("//article[@class='product_pod']"):
            title = book.xpath("./h3/a/@title").get()
            price = book.xpath(".//p[@class='price_color']/text()").get()
            availability = book.xpath(".//p[contains(@class,'availability')]/text()").re_first(r'\S.*\S')
            rating_class = book.xpath("./p[contains(@class, 'star-rating')]/@class").get()
            # Extract the rating word (e.g., 'Three' from 'star-rating Three')
            rating = rating_class.replace('star-rating', '').strip() if rating_class else None
            detail_link = book.xpath("./h3/a/@href").get()
            detail_link = response.urljoin(detail_link)

            books.append({
                'Title': title,
                'Price': price,
                'Availability': availability,
                'Rating': rating,
                'Detail Link': detail_link
            })

        # Save to Excel
        df = pd.DataFrame(books)
        df.to_excel("books.xlsx", index=False)

        self.log(f"Saved {len(books)} books to books.xlsx")
