# Book Data Crawler using Scrapy and MySQL

Welcome to my book data crawler project! This repository demonstrates how to use Scrapy to scrape book information from `books.toscrape.com` and store it in a MySQL database.


## Project Structure

bookscraper/  
│── bookscraper/  
│ 	│── spiders/  
│ 	│ 	│── bookspider.py  
│ 	│ 	│── bookspider_multipage.py  
│ 	│ 	└── bookinfo.py  
│ 	│── items.py  
│ 	│── middlewares.py  
│ 	│── pipelines.py  
│ 	│── settings.py  
│ 	└── init.py  
│  
│── README.md  
│── scrapy.cfg  
└── requirements.txt  


## Files Description

- **bookspider.py**: Scrapes basic book details from the main page.
- **bookspider_multipage.py**: Scrapes books from multiple pages and handles pagination.
- **bookinfo.py**: Scrapes detailed book information from individual book pages.
- **items.py**: Defines the data structure (`BookItem`) for scraped data.
- **pipelines.py**: Contains two pipelines: `BookscraperPipeline` for data cleaning and `MySqlPipeline` for storing data in MySQL.
- **settings.py**: Configures project settings including MySQL database connection.
- **scrapy.cfg**: Scrapy project configuration file.


## Features

- Scrape book data including URL, title, price, availability, and star rating.
- Store scraped data in a MySQL database.
- Handle pagination to scrape data from multiple pages.
- Drop and recreate the database table at the start of each run to ensure fresh data.


## Requirements

- Python 3.x
- Scrapy
- MySQL

