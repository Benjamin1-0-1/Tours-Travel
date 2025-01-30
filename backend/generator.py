import os
import secrets
from cryptography.fernet import Fernet


def generate_or_update_env_file():
    env_file_path = os.path.join(os.path.dirname(__file__), ".env")

    secret_key = secrets.token_urlsafe(26)
    db_uri = "sqlite:///Travels.db"
    jwt_secret_key = secrets.token_urlsafe(26)
    fernet_key = Fernet.generate_key().decode()

    env_variables = {
        "SECRET_KEY": secret_key,
        "FLASK_ENV": "development",
        "JWT_SECRET_KEY": jwt_secret_key,
        "SQLALCHEMY_DATABASE_URI": db_uri,
        "JWT_ACCESS_TOKEN_EXPIRES": 86400,
        "JWT_REFRESH_TOKEN_EXPIRES": 2592000,
        "SQLALCHEMY_TRACK_MODIFICATIONS": "False",
        "FERNET_KEY": fernet_key,
    }

    if os.path.exists(env_file_path):
        print(".env file found. Updating values...")

        with open(env_file_path, "r") as f:
            existing_vars = dict(
                line.strip().split("=", 1) for line in f if line.strip() and "=" in line
            )

        with open(env_file_path, "w") as f:
            for key, value in env_variables.items():
                if key in existing_vars:
                    f.write(f"{key}={existing_vars[key]}\n")
                else:
                    f.write(f"{key}={value}\n")
            print(".env file updated successfully!")

    else:
        print(".env file not found. Creating a new file...")

        with open(env_file_path, "w") as f:
            for key, value in env_variables.items():
                f.write(f"{key}={value}\n")

        print(".env file generated successfully!")


if __name__ == "__main__":
    generate_or_update_env_file()
