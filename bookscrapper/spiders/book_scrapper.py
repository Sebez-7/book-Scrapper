import scrapy
import pandas as pd # to save file in exel format


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

            # Extract the rating word ( 'Three' from 'star-rating Three')
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
