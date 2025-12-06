import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv() 

def get_db_connection():

    """ connecting to the database... """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def execute_query(query, params=None, fetch_data=False):
    """
     SQL (SELECT, INSERT, UPDATE, DELETE).
    """
    conn = get_db_connection()
    if conn is None:
        return [] if fetch_data else None

    cursor = conn.cursor(dictionary=True) 

    try:
        cursor.execute(query, params)
        
        if fetch_data:
            result = cursor.fetchall()
            return result
        else:
            conn.commit() 
            return None 

    except mysql.connector.Error as err:
        print(f"MySQL Query Error: {err}")
        print(f"Query was: {query}")
        conn.rollback() 
        return [] if fetch_data else None
        
    finally:
        cursor.close()
        conn.close()