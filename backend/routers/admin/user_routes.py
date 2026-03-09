from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database.db import get_db
from ...database.db_models import User
from ...api_models.user_schemas import UserCreate, UserResponse, UserUpdate
from ...services.auth_service import get_password_hash

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user. 
    Email must be unique. student_id is optional but must be unique if provided.
    """
    # 1. Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Only check if student_id exists IF it was actually provided
    if user.student_id:
        if db.query(User).filter(User.student_id == user.student_id).first():
            raise HTTPException(status_code=400, detail="Student ID already in use")

    # 3. Hash password and save
    hashed_pw = get_password_hash(user.password)
    
    new_user = User(
        email=user.email,
        hashed_password=hashed_pw,
        student_id=user.student_id, # Will be None if not provided
        is_admin=user.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all registered users.
    """
    return db.query(User).all()

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID. Protects the Root Admin from deletion.
    """
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Security mechanism: Prevent deletion of the ultimate Root Admin
    if user_to_delete.student_id == "00000000":
        raise HTTPException(
            status_code=403, 
            detail="Action forbidden: Cannot delete the Root Admin account"
        )
    
    db.delete(user_to_delete)
    db.commit()
    return

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Security mechanism: Prevent revoking admin privileges from the Root Admin
    if db_user.student_id == "00000000" and user_update.is_admin is False:
        raise HTTPException(status_code=403, detail="Cannot revoke admin privileges from Root Admin")

    update_data = user_update.model_dump(exclude_unset=True)
    
    # If the admin provided a new password, it must be hashed before saving
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # check for uniqueness
    if "email" in update_data and update_data["email"] != db_user.email:
        if db.query(User).filter(User.email == update_data["email"]).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
    # check for uniqueness (but only if it's actually being changed and not set to None)
    if "student_id" in update_data and update_data["student_id"] and update_data["student_id"] != db_user.student_id:
        if db.query(User).filter(User.student_id == update_data["student_id"]).first():
            raise HTTPException(status_code=400, detail="Student ID already in use")

    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user