import psycopg2
import os

configs = {
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE"),
    "user": os.getenv("USER"),
    "password":os.getenv("PASSWORD")
}


class DatabaseConnector():
    @classmethod
    def get_conn_cur(cls):
        cls.conn = psycopg2.connect(**configs)
        cls.cur = cls.conn.cursor()

    def close_conn_cur(cls):
        cls.conn.close()
        cls.cur.close()