import requests
from lxml import html
import pandas as pd

URL = "https://books.toscrape.com/"

response = requests.get(URL)
tree = html.fromstring(response.content)

books = tree.xpath('//article[@class="product_pod"]')

data = []

for book in books:
    title = book.xpath('.//h3/a/@title')[0]
    price = book.xpath('.//p[@class="price_color"]/text()')[0]
    stock_raw = book.xpath('.//p[contains(@class, "instock")]/text()')
    stock = ''.join([s.strip() for s in stock_raw if s.strip() != ''])
    rating_class = book.xpath('.//p[contains(@class, "star-rating")]/@class')[0]
    rating = rating_class.split()[-1]
    detail_link = book.xpath('.//h3/a/@href')[0]
    
    data.append({
        'Title': title,
        'Price': price,
        'Stock': stock,
        'Rating': rating,
        'Detail Link': detail_link
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to Excel file
df.to_excel('books.xlsx', index=False)

print("Data saved to books.xlsx")
