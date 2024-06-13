import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider_multipage"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books=response.css('article.product_pod')
        url='https://books.toscrape.com/'

        for book in books:
            yield{
                'name': book.css('h3 a').attrib['title'],
                'price': book.css('.product_price .price_color::text').get(),
                'link': book.css('h3 a').attrib['href']
            }
        
        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url= url + next_page
            else:
                next_page_url=url + 'catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)