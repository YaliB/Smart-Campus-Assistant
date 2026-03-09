from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# Import database connection and models
from database.db import get_db
from database.db_models import User

# Import authentication logic
from services.auth_service import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # This dependency automatically parses form data for 'username' and 'password' fields, which is the standard for OAuth2 password flow.
    db: Session = Depends(get_db)
):
    """
    Authenticates an admin user and returns a JWT token.
    OAuth2PasswordRequestForm naturally uses 'username' and 'password'.
    We will treat 'username' as the user's email address.
    """
    # 1. Search for the user in the database by email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # 2. Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Verify the user has admin privileges
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admin privileges required",
        )

    # 4. Generate the JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, # The 'sub' (subject) claim is commonly used to identify the principal that is the subject of the JWT. Here, we use the user's email as the unique identifier.
        expires_delta=access_token_expires
    )
    
    # 5. Return the token in the exact format expected by OAuth2
    return {"access_token": access_token, "token_type": "bearer"}