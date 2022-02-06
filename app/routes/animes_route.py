from flask import Blueprint

from app.controllers.anime_controller import create_anime, before_request, delete_anime, get_anime_id, get_animes, updated_anime

bp = Blueprint("animes",__name__)

bp.before_request(before_request)
bp.post("/animes")(create_anime)
bp.get("/animes")(get_animes)
bp.get("/animes/<int:id>")(get_anime_id)
bp.patch("/animes/<int:id>")(updated_anime)
bp.delete("/animes/<int:id>")(delete_anime)