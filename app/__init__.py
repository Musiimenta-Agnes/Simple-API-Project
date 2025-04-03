from flask import Flask
from app.extensions import db,migrate




def create_app():

    
    app = Flask(__name__)
    app.config.from_object('config:Config')
    db.init_app(app)
    migrate.init_app(app,db)


    from app.models.brothers_model import Brother
    from app.models.sister_model import Sister



  

    @app.route('/')
    def index():
        return "My name is Simple"


    
    return app

