from flask import Flask
from datasource.db import db
from web.route.game_route import game_bp
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    app.register_blueprint(game_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
