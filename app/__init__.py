from flask import Flask
from app.extensions import db,migrate
from app.controllers.brother.brother_controller import bro
from app.controllers.sister.sister_controller import sister




def create_app():

    
    app = Flask(__name__)
    app.config.from_object('config:Config')
    db.init_app(app)
    migrate.init_app(app,db)


    from app.models.brothers_model import Brother
    from app.models.sister_model import Sister


    #Register blue prints
    app.register_blueprint(bro)
    app.register_blueprint(sister)



    @app.route('/')
    def index():
        return "My name is Simple"


    
    return app

