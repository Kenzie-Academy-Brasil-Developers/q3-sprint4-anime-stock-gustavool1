from enum import unique
from app.models.anime_model import Anime
from flask import jsonify, request
from http import HTTPStatus
from psycopg2.errors import UniqueViolation, UndefinedColumn
def before_request():
    Anime.create_table_if_not_exists()

def create_anime():
    data = request.get_json()
    try:
        anime = Anime(**data)
        inserted_anime = anime.create_anime()
        inserted_anime = Anime.serialize_anime(inserted_anime)
        print(inserted_anime)
        return inserted_anime, HTTPStatus.CREATED

    except TypeError:
        # accepted_fields = ["anime", "seasons"]
        # wrong_fields = [key for key in data.keys() if key not in accepted_fields]
        return Anime.is_data_valid(data), HTTPStatus.UNPROCESSABLE_ENTITY

    except UniqueViolation:
        return {"error":"Anime with this title already exists"}, HTTPStatus.CONFLICT
    return 'create anime'

def get_animes():
    anime_list = Anime.get_animes()
    anime_list = Anime.serialize_anime(anime_list)
    print(anime_list)
    return jsonify(anime_list), HTTPStatus.OK



def get_anime_id(id):

    anime = Anime.get_anime_id(id)

    if not anime:
        return {"error":"id not found"}, HTTPStatus.NOT_FOUND 

    anime = Anime.serialize_anime(anime)
    return anime, HTTPStatus.OK



def updated_anime(id):
    try:
        data = request.get_json()
        if data.get("anime"):
            data["anime"] = data["anime"].title()
        anime_updated = Anime.update_anime(id, data)    

        if not anime_updated:
            return {"error":"id not found"}, HTTPStatus.NOT_FOUND 


        anime_updated = Anime.serialize_anime(anime_updated)
        return anime_updated, HTTPStatus.OK
    
    except UndefinedColumn:
        return  Anime.is_data_valid(data), HTTPStatus.UNPROCESSABLE_ENTITY
    
    except UniqueViolation:
        return {"msg": "This anime name already exists on our database, try another one."}, HTTPStatus.CONFLICT


def delete_anime(id):
    anime = Anime.delete_anime(id)
    if not anime:
        return {"error":"id not found"}, HTTPStatus.NOT_FOUND 

    return jsonify(None),HTTPStatus.NO_CONTENT