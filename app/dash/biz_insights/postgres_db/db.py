import psycopg2
from psycopg2.extras import DictCursor
import pandas as pd
import pandas.io.sql as sqlio

from .log import LOGGER



class Database:
    """PostgreSQL Database class."""

    def __init__(
            self,
            DATABASE_HOST,
            DATABASE_USERNAME,
            DATABASE_PASSWORD,
            DATABASE_PORT,
            DATABASE_NAME
        ):
        self.host = DATABASE_HOST
        self.username = DATABASE_USERNAME
        self.password = DATABASE_PASSWORD
        self.port = DATABASE_PORT
        self.dbname = DATABASE_NAME
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    port=self.port,
                    dbname=self.dbname
                )
            except psycopg2.DatabaseError as e:
                LOGGER.error(e)
                raise e
            finally:
                LOGGER.info('Connection opened successfully.')

    def select_rows(self, query):
        """Run a SQL query to select rows from table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = cur.fetchall()
        cur.close()
        return records

    def select_rows_dict_cursor(self, query):
        """Run SELECT query and return dictionaries."""
        self.connect()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            records = cur.fetchall()
        cur.close()
        return records

    def update_rows(self, query):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return f"{cur.rowcount} rows affected."


    def queryToPD(self,query):
        self.connect()
        dat = sqlio.read_sql_query(query, self.conn)
        return dat

    def deleteTicker(self,ticker):
        """ delete part by part id """
        # create a new cursor
        cur = self.conn.cursor()
        # execute the UPDATE  statement
        cur.execute("DELETE FROM biztickermentions WHERE ticker = '%s'"%(ticker))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        self.conn.commit()
        return rows_deleted
        # Close communication with the PostgreSQL database

  