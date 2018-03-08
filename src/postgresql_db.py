import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def auth():
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_port = os.environ.get('DB_PORT')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')

    return connect_db(
        db_host,
        db_name,
        db_port,
        db_user,
        db_password,
    )


def connect_db(db_host, db_name, db_port, db_user, db_password):
    try:
        print('Connecting to db...')
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
        )
        return conn
    except (psycopg2.OperationalError):
        error_string = 'Creating new db: {}.'
        print(error_string.format(db_name))

        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        setup_database(conn, db_name)
        conn.close()

        new_conn = new_db_connection(
            db_host,
            db_name,
            db_port,
            db_user,
            db_password,
        )
        create_table(new_conn, 'src/corpus_table.sql')
        return new_conn


def new_db_connection(db_host, db_name, db_port, db_user, db_password):
    return psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
    )


def setup_database(conn, database_name):
    with conn.cursor() as cur:
        cur.execute('CREATE DATABASE {} ;'.format(database_name))


def create_table(conn, sql_file):
    with conn.cursor() as cur:
        cur.execute(open(sql_file, 'r').read())


def insert_many(conn, table_data):
    table_header = table_data[0].keys()
    table_columns = ','.join(table_header)

    table_values = ')s, %('.join(table_header)
    table_values = '%({})s'.format(table_values)
    with conn.cursor() as cur:
        for entry in table_data:
            insert_statement = "INSERT INTO existential_corpus ({table_columns}) VALUES ({table_values})"
            # Try insert new data, on error rollback to continue with insert.
            try:
                insert_statement = insert_statement.format(
                    table_columns=table_columns,
                    table_values=table_values
                )
                cur.execute(insert_statement, entry)
                conn.commit()
            except psycopg2.IntegrityError:
                conn.rollback()


def extract_data(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT text FROM existential_corpus;")
        rows = [row[0] for row in cur.fetchall()]
    return ' '.join(rows)


#   execute select
#   return corpus

