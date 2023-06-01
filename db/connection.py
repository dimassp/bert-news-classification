import psycopg2

def get_connection_and_cursor():
    connection =psycopg2.connect(
    dbname='postgis_4', user='postgres', 
    host='localhost', password='zulfiramdani900')
    cursor = connection.cursor()
    return connection, cursor

def insert_news(news_id: str, news_content: str):
    connection = None
    try:
        connection, cursor = get_connection_and_cursor()
        sql = f"""INSERT INTO table_test(news_id, news_content) VALUES (%s,%s) ON CONFILCT (news_id)
        DO UPDATE SET news_content = {news_content}"""
        cursor.execute(sql,(news_id, news_content))
        connection.commit()
        
        cursor.close()
    except:
        pass
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed')

def update_news(news_id: str, feedback_content_type: str, feedback_event_category: str, news_content: str):
    connection, cursor = get_connection_and_cursor()
    cursor.execute(
    "UPDATE news SET feedback_content_type_id=(%s), feedback_event_category_id=(%s), content_text=(%s)"
    " WHERE news_id = (%s)", 
    (feedback_content_type.lower(), feedback_event_category.lower(), news_content, news_id,));
    connection.commit()
    
    print(f"row Updated")
    cursor.close()
    if connection is not None:
        connection.close()
        
def get_all_news():
    connection, cursor = get_connection_and_cursor()
    cursor.execute(
        """SELECT 
        news_id,
        content_type_id, 
        feedback_content_type_id, 
        event_category_id, 
        feedback_event_category_id, 
        content_text 
        FROM news"""
    )
    all_data = cursor.fetchall()
    connection.close()
    return all_data

def get_news(news_id: str):
    connection, cursor = get_connection_and_cursor()
    
    cursor.execute(
        f"""SELECT 
        news_id,
        content_type_id, 
        feedback_content_type_id, 
        event_category_id, 
        feedback_event_category_id, 
        content_text 
        FROM news 
        WHERE news_id='{news_id}'"""
    )
    
    data = cursor.fetchone()
    # print(f"print data from connection: {data}")
    connection.close()
    cursor.close()
    return data

def delete_news(news_id: str):
    connection, cursor = get_connection_and_cursor()
    
    cursor.execute(
        f"""DELETE FROM table_test WHERE news_id='{news_id}'"""
    )
    connection.commit()
    connection.close()
    cursor.close()