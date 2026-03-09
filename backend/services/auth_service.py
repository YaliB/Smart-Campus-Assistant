import os
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Configuration
# It's crucial to have a strong SECRET_KEY in production (.env)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret_fallback_key_for_development")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt is a secure hashing algorithm that includes salting and multiple rounds of hashing to protect against brute-force attacks.

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the provided plain text password matches the hashed password from the database.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JSON Web Token (JWT) with an expiration time.
    The 'data' dict usually contains the user's email or ID.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add the expiration time to the token payload
    to_encode.update({"exp": expire})
    
    # Generate the encoded token string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt