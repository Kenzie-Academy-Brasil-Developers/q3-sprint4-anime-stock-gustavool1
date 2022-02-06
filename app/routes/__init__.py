from app.routes.animes_route import bp as bp_anime

def init_app(app):
    app.register_blueprint(bp_anime)