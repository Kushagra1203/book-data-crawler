# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter 
import MySQLdb

class BookscraperPipeline:
    def process_item(self, item, spider):

        #usage for itemadapter is given above
        adapter=ItemAdapter(item) 
        
        # to remove whitespace
        field_names=adapter.field_names()
        for field_name in field_names:
            if field_name != 'title':
                value=adapter.get(field_name)
                if isinstance(value, tuple):
                    adapter[field_name]=value[0].strip() #being returned as tuple
                else:
                    adapter[field_name]=value.strip()
                
        # to convert star from upper case to lower case
        value=adapter.get('star').split(" ") # "star-rating Two" -> ["star-rating","Two"]
        adapter['star']=value[1].lower()
        
        #to save price data as float
        value = adapter.get('price')
        print(f"Before replace: {value}")
        value = value.replace('£', '')
        print(f"After replace: {value}")
        adapter['price'] = value
            
        #to remove char in availabitly(exact number of books in stock)
        available=adapter.get('availability').split('(') # "In stock (20 available)" -> ["In stock ", "20 available)"]
        if len(available)<2:
            adapter['availability']=0
        else:
            availability_array = available[1].split(' ')
            adapter['availability']=int(availability_array[0])
        
        #convert star rating into int
        star=adapter.get('star')
        if star == 'zero' : #already lowercased above
            adapter['star']=0
        elif star == 'one' :
            adapter['star'] = 1
        elif star == 'two' :
            adapter['star'] = 2
        elif star == 'three' :
            adapter['star'] = 3
        elif star == 'four' :
            adapter['star'] = 4
        elif star == 'five' :
            adapter['star'] = 5
        
        return item



class MySqlPipeline:

    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost',
                                    user='root',
                                    passwd='',
                                    db='books')
        self.cur = self.conn.cursor()

        self.cur.execute('DROP TABLE IF EXISTS books')
        
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INT NOT NULL auto_increment,
                url TEXT,
                title VARCHAR(255),
                price DECIMAL(5, 2),
                availability INT,
                star INT,
                PRIMARY KEY (id)
            )
        ''')
    
    def process_item(self, item, spider):
        self.cur.execute(
            """
            INSERT INTO books(
            url, 
            title, 
            price, 
            availability, 
            star
            ) 
            VALUES(%s, %s, %s, %s, %s)
            """,
            (
                item['url'], 
                item['title'], 
                item['price'], 
                item['availability'], 
                item['star']
            )
        )
            
        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()