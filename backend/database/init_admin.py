import os
from datetime import datetime
from sqlalchemy.orm import Session
from .db import SessionLocal
from .db_models import User, ReceptionHour, ExamSchedule, FAQ, Room
from ..services.auth_service import get_password_hash, verify_password


def init_root_admin(db: Session):
    """
    Ensures the root admin user exists based on .env configuration.
    Uses a fixed student_id as a unique identifier to allow email 
    and password updates via .env without creating duplicate users.
    """
    # Load configurations from environment variables
    root_email = os.getenv("ROOT_ADMIN_EMAIL", "root@campus.ac.il")
    root_pass = os.getenv("ROOT_ADMIN_PASSWORD", "admin123")
    
    # Immutable identifier for the system's root account
    ROOT_ADMIN_ID = "00000000" 

    # 1. Search for the admin using the fixed student_id instead of the email
    user = db.query(User).filter(User.student_id == ROOT_ADMIN_ID).first()
    
    if not user:
        # 2. If no admin exists with this ID, create a new one
        hashed_pw = get_password_hash(root_pass)
        new_root = User(
            email=root_email, 
            hashed_password=hashed_pw, 
            is_admin=True, 
            student_id=ROOT_ADMIN_ID
        )
        db.add(new_root)
        db.commit()
        print(f"[*] Bootstrapped NEW ROOT Admin: {root_email}")
    else:
        # 3. Synchronize existing admin with .env if any value differs
        # We check all conditions at once to minimize database overhead
        if (user.email != root_email or 
            not verify_password(root_pass, user.hashed_password) or 
            not user.is_admin):
            
            user.email = root_email
            user.hashed_password = get_password_hash(root_pass)
            user.is_admin = True
            
            db.commit()
            print(f"[*] ROOT Admin synchronized and updated from .env")
        else:
            print(f"[*] ROOT Admin verified: {root_email}")

