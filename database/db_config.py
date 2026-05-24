from sqlalchemy import create_engine

username = "root"
password = "password"
host = "localhost"
port = "3306"
database = "crypto_dashboard"

DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)