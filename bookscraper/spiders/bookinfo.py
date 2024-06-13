import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookinfo"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    # custom_settings = {  #use this to overwrite any settings in settings.py
    #     'FEEDS': {
    #         'cleandata.csv': {'format': 'csv', 'overwrite': True}, 
    #     }
    # }
    
    def parse(self, response):
        books=response.css('article.product_pod')
        url='https://books.toscrape.com/'

       
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            
            if 'catalogue/' in relative_url:
                book_url= url + relative_url
                
            else:
                book_url=url + 'catalogue/' + relative_url
                
            yield response.follow(book_url, callback=self.parse_book_page)
        
        
        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url= url + next_page
            else:
                next_page_url=url + 'catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)
            
    def parse_book_page(self,response):
        table_row=response.css('table tr')
        book_item=BookItem()
        
        book_item['url'] = response.url,
        book_item['title']= response.css('.product_main h1::text').get(), #it is comming out as array because of the comma remove it and it will come out as string
        book_item['availability']= table_row[5].css("td ::text").get(),
        book_item['star']= response.xpath("//div[@class='alert alert-warning']/preceding-sibling::p[1]/@class").get(), #can also be written as response.css('p.star-rating ::attr(class)').get()
        book_item['price']=response.css('p.price_color ::text').get()

        yield book_item
    
    
    """"
    if there are multiple tags that are same you can use nth-child(n) for that tag to get the exact one that you want
    for example response.css('ul li:nth-child(3) a::text').get() as there are 3 li in ul tag
    till now we used response.css to extract data using css selectors like above example
    but some times there are better way to get the data using xpath to select nodes
    """
    """"
    response.css('ul li:nth-child(3) a::text').get() can be written in xpath as:
    response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()

    // is used to select all the nodes of a tag name so //ul gets all the tagnames

    //tagname[@attribute="value"] is used to selecting Nodes with Specific Attributes so 
    //ul[@class='breadcrumb'] gets us all the ul tag with class breadcrumb

    /li[@class='active'] goes directly into ul tag for li with class active

    preceding-sibling this is used to get the preceding tag to selected tag

    preceding-sibling::li[1] is used to select the first li element that is a preceding sibling of the current node.

    basically xpath can be usefull when we dont have idea of absolute path and what to extract data using relative path of a tag using its surrounding classes
    """

    #Table can be extracted by table_row=response.css('table tr') this will extract all the table rows