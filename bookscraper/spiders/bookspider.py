import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books=response.css('article.product_pod')

        for book in books:
            yield{
                # format here is ('tag.class (and then inside that) .class::text').get()
                # or ('tag (inside that tag) tag2').text
                'name': book.css('h3 a').attrib['title'], #can also be written as book.css('h3 a::attr(href)').get()
                'price': book.css('.product_price .price_color::text').get(),
                'link': book.css('h3 a').attrib['href']
            }