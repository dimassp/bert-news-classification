import sys
import psycopg2
sys.path.insert(0,r'D:\PROGRAMMING\python\bert_news_type_and_topic_classification\news_portal')
# print(sys.path)
from scrape2 import Scrape
# from news_portal.scrape import Scrape
def print_name():
    print("Dimas Surya Prayitna")

def scrape_and_classify():
    scrape = Scrape()
    # scraped_news = scrape.scrape_news(['detiknewsjabar','prbandung','antaranewsjabar','sekitarbandung'])
    scraped_news = scrape.scrape_news(['detiknewsjabar'])
    print(f'total news scraped: {len(scraped_news)}')
    if len(scraped_news) >0:
        # print(scraped_news[0])
        insert_record(scraped_news[:2])

def insert_record(news: list):
    print(f"total news: {len(news)}")
    connection =psycopg2.connect(
    dbname='postgis_3', user='postgres', 
    host='localhost', password='zulfiramdani900')
    
    for *news_data, portal_or_account_name in news:
        print(f"news_data: {tuple(news_data)}")
        print(f"portal_or_account_name: {portal_or_account_name}")
    cursor = connection.cursor()
    tables = ['ref_event_category', 'news_source_platform', 'news_source', 'news']
    ref_event_category_column_total = "%s," * 2
    ref_event_category_column_total = ref_event_category_column_total[:-1]
    
    news_source_platform_column_total = "%s," * 2
    news_source_platform_column_total = news_source_platform_column_total[:-1]
    
    news_source_column_total = "%s," * 5
    news_source_column_total = news_source_column_total[:-1]
    
    news_table_column_total = "%s," * 6
    news_table_column_total = news_table_column_total[:-1]
    # print(news_table_column_total)
    
    # '(news_id, text.text, news_type, news_topic, news_link['href'], self.datetime_extracted, portal)'
    ref_event_category_insert_args = ','.join(cursor.mogrify(f"({ref_event_category_column_total})", tuple([news_topic,news_topic]))
                                              .decode('utf-8') 
                                              for news_id, text, news_type, news_topic, news_link, datetime_extracted, portal in news)
    
    news_source_platform_table_insert_args = ','.join(cursor.mogrify(f"({news_source_platform_column_total})", tuple([portal,portal]))
                                              .decode('utf-8')
                                              for news_id, text, news_type, news_topic, news_link, datetime_extracted, portal in news)
    
    news_source_table_insert_args = ','.join(cursor.mogrify(f"({news_source_column_total})", tuple([news_id, portal, 
                                                            news_link, portal , True]))
                                              .decode('utf-8') 
                                              for news_id, text, news_type, news_topic, news_link, datetime_extracted, portal in news)
    
    news_table_insert_args = ','.join(cursor.mogrify(f"({news_table_column_total})", tuple(news_data))
                                             .decode('utf-8') 
                                             for *news_data, portal_or_account_name in news)
    
    ref_event_category_table = 'ref_event_category'
    news_source_platform_table = 'news_source_platform'
    news_source_table = 'news_source'
    news_table = 'news'
    # sql_get_all = f'SELECT * FROM {table}'
    sql_insert_ref_event_category_table = f"""
        INSERT INTO {ref_event_category_table} (event_category_id, description) values {ref_event_category_insert_args} ON CONFLICT DO NOTHING """
        
    sql_insert_news_source_platform_table = f"""
        INSERT INTO {news_source_platform_table} (news_source_platform_id, description) values {news_source_platform_table_insert_args} 
        ON CONFLICT DO NOTHING 
    """
    
    sql_insert_news_source_table = f"""
        INSERT INTO {news_source_table} (news_source_id, description, url, news_source_platform_id, is_active) 
        values {news_source_table_insert_args} ON CONFLICT DO NOTHING 
    """
    
    sql_insert_news_table = f"""
        INSERT INTO {news_table} (news_source_id, content_text, content_type_id, event_category_id, news_source_url, datetime_extracted) 
        values {news_table_insert_args}
    """

    cursor.execute(sql_insert_ref_event_category_table)
    cursor.execute(sql_insert_news_source_platform_table)
    cursor.execute(sql_insert_news_source_table)
    cursor.execute(sql_insert_news_table)
    connection.commit()
    cursor.close()
    connection.close()
    print('data successfully inserted')

    # cursro.execute(sql_)
    # cursor.execute(sql_get_all)
    # items = cursor.fetchall()
    # print(f"items: {items}")
def column_total():
    pass
def insert_args():
    pass
def sql_insert():
    pass
# scrape_and_classify()