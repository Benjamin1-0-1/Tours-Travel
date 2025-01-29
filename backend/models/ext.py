from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime,timezone

db = SQLAlchemy()
bcrypt = Bcrypt()
