import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables (like DATABASE_URL if it exists)
load_dotenv()

# Get the database URL from the environment.
# If it's not set in the .env file, fallback to the local SQLite database.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./database/campus_data.db"
)

# Check if the engine is SQLite to apply specific arguments
is_sqlite = SQLALCHEMY_DATABASE_URL.startswith("sqlite")

if is_sqlite:
    # SQLite requires check_same_thread=False for FastAPI's async environment
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Other databases (like PostgreSQL/MySQL) don't need that argument
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal class will be used to create actual database sessions for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to get a database session and close it after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()