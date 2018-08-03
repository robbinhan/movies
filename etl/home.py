#!/usr/bin/python

from scrapy.selector import Selector
import mysql.connector
import html.parser


cnx = mysql.connector.connect(user='root', password='123456',
                              host='127.0.0.1',
                              database='zhihu')


def query():
    print("query")
    cursor = cnx.cursor()
    query_data_sql = "select * from `20171218`"
    cursor.execute(query_data_sql)
    
    html_parser = html.parser.HTMLParser()

    for (qid, content) in cursor:
        unescaped = html_parser.unescape(content)
        # print(unescaped)
      
        parse_page(unescaped)
      
    cursor.close()
    cnx.close()


def parse_page(html):
    print("parse_page")
    problem = Selector(text=html)    
    
    feeds = problem.css('.Feed-title').extract()
    
    articles = problem.css('.ContentItem.ArticleItem').extract()
    
    for article in articles:
        feed_selector = Selector(text=article)
        question_title = feed_selector.xpath('//meta[@itemprop="headline"]/@content').extract_first()
        if(question_title is None):
            question_title = feed_selector.xpath('.ContentItem-title/a/@href').extract_first()
            
        question_answer_url = feed_selector.xpath('//meta[@itemprop="url"]/@content').extract_first()
        question_answer_date = feed_selector.xpath('//meta[@itemprop="dateModified"]/@content').extract_first()
        
        print(question_title,question_answer_url,question_answer_date)
    
    
    # 
    # for feed in feeds:
    #     # print(feed)
    #     feed_selector = Selector(text=feed)
    #     name = feed_selector.xpath('//meta[@itemprop="name"]/@content').extract_first()
    #     image = feed_selector.xpath('//meta[@itemprop="image"]/@content').extract_first()
    #     url = feed_selector.xpath('//meta[@itemprop="url"]/@content').extract_first()
    # 
    #     if(name is None):
    #         continue
    # 
    #     print(name,image,url)
    
    
def main():
    query()    
    
if __name__ == "__main__":
    main()    


