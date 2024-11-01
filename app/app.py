from flask import Flask
import os
from models.db import db
from models.User import User
from models.Item import Item
from models.Game import Game
from models.Quiz import Quiz
from controllers.UserController import UserController
from controllers.ItemController import ItemController
from controllers.ControllerAdvice import ControllerAdvice
from controllers.GameController import GameController 
from flask_cors import CORS
from dotenv import load_dotenv
from utils.s3 import bucket_pi_accessing

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8081"}})
dir = os.path.abspath(os.path.dirname(__file__))

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["PERMANENT_SESSIONLIFETIME"] = os.environ.get("PERMANENT_SESSIONLIFETIME")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(dir, 'models/db.sqlite3')

if __name__ == '__main__':
    db.init_app(app=app)
    UserController.init_app(app)
    ItemController.init_app(app)
    GameController.init_app(app)
    ControllerAdvice.init_app(app)
    bucket_pi_accessing.init_s3()
    with app.test_request_context():
        db.create_all()
        User.seed_user()
        Item.seed_item()
        Game.seed_game()
        Quiz.seed_quiz()
    app.run(host='localhost', port=4000, debug=True)