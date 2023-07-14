import scrapy
from pathlib  import Path


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"Books-{page}.html"

        # Saved the content as only files
        # Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        # a= response.css(".product_pod").get()
        # print(a)
        details = []
        cards = response.css(".product_pod")

        for card in cards:
            title = card.css("h3>a::text").get()
            print(title)
            
            image = card.css(".image_container img")
            src= image.attrib['src']
            print(src)
            
            link = card.css(".image_container a")
            href = link.attrib['href']
            print(href)
            rating = card.css(".star-rating").attrib['class']
            star_rating= rating.split(" ")[1]
            print(star_rating)
            product_price= card.css(".price_color::text").get()
            print(product_price)

            details.append({
                    "Book-Title" : title,
                    "Book_Image_link": src,
                    "Book_link": href,
                    "Book_Rating": star_rating,
                    "Book_Price": product_price

                })
        
        df=pd.DataFrame.from_dict(details)
        df.to_csv('Scrapy.csv', index=None)

            
    