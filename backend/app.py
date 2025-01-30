import os
import sys
from flask import Flask
# from models import * # noqa
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api
from models.ext import db
from config import Config
from namespaces import all_namespaces


load_dotenv()


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance")
if not os.path.exists(instance_path):
    os.makedirs(instance_path)


app = Flask(__name__, instance_path=instance_path)
app.config.from_object(Config)
migrate = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
CORS(app, origins=["http://localhost:3000"])

api = Api(
    app,
    version="1.0",
    title="Tours API",
    description="User Profile Operations",
    prefix="/apis",
)


for ns, path in all_namespaces:
    api.add_namespace(ns, path=path)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5500, debug=True)
