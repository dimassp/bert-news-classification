import sys

sys.path.insert(0,r'D:\PROGRAMMING\python\bert_news_type_and_topic_classification\news_portal')
sys.path.insert(0,r'D:\PROGRAMMING\python\bert_news_type_and_topic_classification\db')
# print(sys.path)
from scrape2 import Scrape
from connection import get_connection_and_cursor
# from news_portal.scrape import Scrape


def print_name():
    print("Dimas Surya Prayitna")

def scrape_and_classify():
    scrape = Scrape()
    # scraped_news = scrape.scrape_news(['detiknewsjabar','prbandung','antaranewsjabar','sekitarbandung'])
    scraped_news = scrape.scrape_news(['detiknewsjabar','prbandung','antaranewsjabar'])
    # scraped_news = scrape.scrape_news(['detiknewsjabar'])
    
    if len(scraped_news) >0:
        insert_record(scraped_news)

def insert_record(news: list):
    tables = ['ref_content_type','ref_event_category', 'news_source_platform', 'news_source', 'news']
    connection, cursor = get_connection_and_cursor()
    for table in tables:
        column_total_ = column_total(table)
        insert_argument_ = insert_args(table, column_total_, news, cursor)
        sql_insert_argument = sql_insert(table, insert_argument_)
        cursor.execute(sql_insert_argument)
    connection.commit()
    cursor.close()
    connection.close()
    print('data successfully inserted')
    
def column_total(table):
    total_column_of_tables = {
        'ref_content_type': 2, 
        'ref_event_category': 2, 
        'news_source_platform': 2, 
        'news_source' : 5,
        'news': 7
    }
    total_columns = "%s," * total_column_of_tables[table]
    total_columns = total_columns[:-1]
    return total_columns

def insert_args(table, column_total_each_table, news, cursor):
    insert_argument_ = ''
    if table == 'ref_content_type':
        print(f"column total of {table}: {column_total_each_table}")
        insert_argument_ = ','.join(cursor.mogrify(f"({column_total_each_table})", tuple([news_type,news_type]))
                            .decode('utf-8') 
                            for news_id, text, news_type, news_topic, news_link, datetime_extracted, portal in news)

    if table == 'ref_event_category':
        print(f"column total of {table}: {column_total_each_table}")
        insert_argument_ = ','.join(cursor.mogrify(f"({column_total_each_table})", tuple([news_topic,news_topic]))
                            .decode('utf-8') 
                            for news_id, text, news_type, news_topic, news_link, datetime_extracted, portal in news)

    elif table == 'news_source_platform':
        print(f"column total of {table}: {column_total_each_table}")
        insert_argument_ = ','.join(cursor.mogrify(f"({column_total_each_table})", tuple([portal,portal]))
                            .decode('utf-8') 
                            for news_id, text, news_type, news_topic, news_link, datetime_extracted, portal in news)

    elif table == 'news_source':
        print(f"column total of {table}: {column_total_each_table}")
        insert_argument_ = ','.join(cursor.mogrify(f"({column_total_each_table})", tuple([news_id, portal, news_link, portal , True]))
                            .decode('utf-8') 
                            for news_id, text, news_type, news_topic, news_link, datetime_extracted, portal in news)

    elif table == 'news' :
        print(f"column total of {table}: {column_total_each_table}")
        insert_argument_ = ','.join(cursor.mogrify(f"({column_total_each_table})", tuple([news_id, news_id, text, news_type, news_topic, news_link, datetime_extracted]))
                            .decode('utf-8') 
                            for news_id, text, news_type, news_topic, news_link, datetime_extracted, portal in news)
   
    return insert_argument_
def sql_insert(table, insert_argument_):
    print(f"insert argument of table {table}: {insert_argument_}")
    insert_string = f"INSERT INTO {table} "
    on_conflict_string = "ON CONFLICT DO NOTHING"
    columns = {
        'ref_content_type': "(content_type_id, description)", 
        'ref_event_category': "(event_category_id, description)", 
        'news_source_platform': "(news_source_platform_id, description)", 
        'news_source' : "(news_source_id, description, url, news_source_platform_id, is_active)",
        'news' :"(news_id, news_source_id, content_text, content_type_id, event_category_id, news_source_url, datetime_extracted)"
    }
    columns_to_be_inserted = columns[table]
    sql_insert_argument = f"{insert_string} {columns_to_be_inserted} values {insert_argument_} {on_conflict_string}"
   
    return sql_insert_argument
# scrape_and_classify()

