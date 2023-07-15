import scrapy
from pathlib  import Path
import pandas as pd 

# BooksSpider Class is defined that is inherited from the scrapy.Spider
class BooksSpider(scrapy.Spider):
    # Setting the Spider name to books
    name = "books"
    
    # Setting the allowed domain and start url for the spider 
    # These urls are the entry points for the spider to start crawl 
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    """ defining start_requests function to generate the initial requests to start the crawler.
    """
    def start_requests(self):
        urls = [
            "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        ]
        for url in urls:
            # It Yields a scrapy.Request object for each url in the urls list.
            # The callback parameter specifies the function to be called when a reponse is received from each requests
            yield scrapy.Request(url=url, callback= self.parse)
    
    """ Defining the parse function which gets invoked when a response is received for a request
    It is basically responsible for extracting the data and saving it 
    """
    def parse(self, response):
        # Extract the page name from the response URL
        page = response.url.split("/")[-2]
        
        # Generating the file name 
        filename = f"Books-{page}.html"
        
        #Log a message to indicate that the file is saved.
        self.log(f"Saved file {filename}")

        #Creating an empty list to append all the details
        details = []
        cards = response.css(".product_pod")

        for card in cards:
            title = card.css("h3>a::text").get()
            print(title)
            
            image = card.css(".image_container img")
            src= image.attrib['src'].replace("../../../../media", "https://books.toscrape.com/media")
            print(src)
            
            link = card.css(".image_container a")
            href = link.attrib['href'].replace("../../../", "https://books.toscrape.com/catalogue/")
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
        df.to_csv(f'Scrapy-{page}.csv', index=None)

            
    