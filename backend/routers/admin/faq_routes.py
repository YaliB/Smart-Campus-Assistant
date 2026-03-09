from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database.db import get_db
from ...database.db_models import FAQ
from ...api_models.knowledge_schemas import FAQCreate, FAQResponse, FAQUpdate

router = APIRouter()

@router.post("/", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
def create_faq(faq: FAQCreate, db: Session = Depends(get_db)):
    """
    Create a new FAQ entry.
    """
    new_faq = FAQ(
        question=faq.question,
        answer=faq.answer,
        tags=faq.tags
    )
    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)
    return new_faq

@router.get("/", response_model=List[FAQResponse])
def get_all_faqs(db: Session = Depends(get_db)):
    """
    Retrieve all FAQs.
    """
    return db.query(FAQ).all()

@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    """
    Delete an FAQ by its ID.
    """
    faq_to_delete = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq_to_delete:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    db.delete(faq_to_delete)
    db.commit()
    return

@router.patch("/{faq_id}", response_model=FAQResponse)
def update_faq(faq_id: int, faq_update: FAQUpdate, db: Session = Depends(get_db)):
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    
    update_data = faq_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_faq, key, value)
        
    db.commit()
    db.refresh(db_faq)
    return db_faq