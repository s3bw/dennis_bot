
import psycopg2


conn = psycopg2.connect(
    host='localhost',
    database='postgres',
    user='postgres',
    password='postgres',
)

cur = conn.cursor()



# import postgresql module


# def connect
#   return connection


# def process_new_data
#   add_id hash
#   break into sentences
#   check for duplicates
#   add date


# def create_table


# def insert_to_table


# def export_data_for_training
#   return corpus
