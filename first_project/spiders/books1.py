import scrapy
import pandas as pd

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = [
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    ]

    def __init__(self):
        self.all_data = []  # List to store scraped data

    def parse(self, response):
        page = response.url.split("/")[-2]
        details = []
        cards = response.css(".product_pod")

        for card in cards:
            title = card.css("h3>a::text").get()
            print(title)

            image = card.css(".image_container img")
            src = image.attrib['src'].replace("../../../../media", "https://books.toscrape.com/media")
            print(src)

            link = card.css(".image_container a")
            href = link.attrib['href'].replace("../../../", "https://books.toscrape.com/catalogue/")
            print(href)

            rating = card.css(".star-rating").attrib['class']
            star_rating = rating.split(" ")[1]
            print(star_rating)

            product_price = card.css(".price_color::text").get()
            print(product_price)

            details.append({
                "Book-Title": title,
                "Book_Image_link": src,
                "Book_link": href,
                "Book_Rating": star_rating,
                "Book_Price": product_price
            })

        self.all_data.extend(details)  # Add scraped details to the list

    def closed(self, reason):
        df = pd.DataFrame(self.all_data)  # Convert list to DataFrame
        df.to_csv('Final_Scrapy.csv', index=None)
