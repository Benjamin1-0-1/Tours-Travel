import os
import sys
from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api
from models.ext import db
from config import Config

# Suppose you have a list of (namespace, path) in 'namespaces.py'
from namespaces import all_namespaces
from routes.auth_routes import auth_bp

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# If your frontend is at 3000:
CORS(app, origins=["http://localhost:3000"])

# Register auth blueprint
app.register_blueprint(auth_bp)

api = Api(
    app,
    version="1.0",
    title="Tours API",
    description="User Profile Operations",
    prefix="/apis",  # => /apis
)

# Register your namespaces
for ns, path in all_namespaces:
    api.add_namespace(ns, path=path)  # => e.g. /apis/tours/v1/tours

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Running on port 5500
    app.run(port=5500, debug=True)
