from app.models import DatabaseConnector
from datetime import datetime
from psycopg2 import sql
class Anime(DatabaseConnector):

    anime_keys = ["id","anime", "released_date", "seasons"]
    valid_keys = ["anime", "seasons"]
    def __init__(self, anime, seasons) -> None:
        self.anime = anime.title()
        self.seasons = seasons 
        self.released_date = self.setting_releasing_date()

    def setting_releasing_date(self):
        return str(datetime.now().strftime("%d/%m/%Y %H:%M"))

    def create_anime(self):
        self.get_conn_cur()
        query = """
            INSERT INTO animes 
                (anime, seasons, released_date)
            VALUES
                (%s, %s, %s )
            RETURNING *
            """

        values_list = list(self.__dict__.values())
        self.cur.execute(query, values_list)

        inserted_anime = self.cur.fetchone()
        self.conn.commit()

        self.close_conn_cur()
        return inserted_anime
        
    @classmethod    
    def create_table_if_not_exists(cls):
        cls.get_conn_cur()
        query = """
            CREATE TABLE IF NOT EXISTS animes(
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL 
            )
        """
        cls.cur.execute(query)
        cls.conn.commit()
        cls.close_conn_cur(cls)
    

    @classmethod
    def serialize_anime(cls, data):
        
        if type(data) is tuple:
            return  dict(zip(cls.anime_keys, data))
        if type(data) is list:
            return [dict(zip(cls.anime_keys, value)) for value in data]

    @classmethod
    def get_animes(cls):
        cls.get_conn_cur()
        query = "SELECT * FROM animes"
        cls.cur.execute(query)
        anime_list = cls.cur.fetchall()
        cls.conn.commit()
        cls.close_conn_cur(cls)

        return anime_list

    @classmethod
    def get_anime_id(cls,id):
        cls.get_conn_cur()
        query = """SELECT * FROM animes WHERE id=%s"""

        cls.cur.execute(query, [id])
        anime = cls.cur.fetchone()

        cls.conn.commit()
        cls.close_conn_cur(cls)

        return anime

    @classmethod
    def update_anime(cls, id, data):
        cls.get_conn_cur()
        columns = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(values) for values in data.values()]
        query = sql.SQL("""
                UPDATE 
                    animes
                SET 
                    ({columns}) = ROW({values})
                WHERE 
                    id = {id}
                RETURNING *;
        """).format(id = sql.Literal(id), columns = sql.SQL(",").join(columns), values=sql.SQL(",").join(values))
        
        cls.cur.execute(query)
        anime_updated = cls.cur.fetchone()
        cls.conn.commit()
        cls.close_conn_cur(cls)

        return anime_updated

    @classmethod
    def delete_anime(cls, id):
        cls.get_conn_cur()
        query = """DELETE FROM animes WHERE id=%s RETURNING *"""
        cls.cur.execute(query, [id])
        
        anime_deleted = cls.cur.fetchone()
        cls.conn.commit()

        cls.close_conn_cur(cls)
        return anime_deleted
    @classmethod
    def is_data_valid(cls, data):
        wrong_fields = [key for key in data.keys() if key not in cls.valid_keys]
        return {"allowed_fields": cls.valid_keys, "wrong_fields_sended":wrong_fields}
