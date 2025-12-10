"""
Ideas API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Idea
from ..schemas import IdeaCreate, IdeaWithScript

router = APIRouter()


@router.post("/", response_model=IdeaWithScript)
def create_idea(idea: IdeaCreate, db: Session = Depends(get_db)):
    """새 아이디어 생성"""
    db_idea = Idea(**idea.dict())
    db.add(db_idea)
    db.commit()
    db.refresh(db_idea)
    return db_idea


@router.get("/", response_model=List[IdeaWithScript])
def list_ideas(
    channel_id: int = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """아이디어 목록 조회"""
    query = db.query(Idea)

    if channel_id:
        query = query.filter(Idea.channel_id == channel_id)

    if status:
        query = query.filter(Idea.status == status)

    ideas = query.offset(skip).limit(limit).all()
    return ideas


@router.get("/{idea_id}", response_model=IdeaWithScript)
def get_idea(idea_id: int, db: Session = Depends(get_db)):
    """아이디어 상세 조회"""
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea


@router.put("/{idea_id}/status")
def update_idea_status(idea_id: int, status: str, db: Session = Depends(get_db)):
    """아이디어 상태 변경"""
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    idea.status = status
    db.commit()
    db.refresh(idea)
    return idea


@router.delete("/{idea_id}")
def delete_idea(idea_id: int, db: Session = Depends(get_db)):
    """아이디어 삭제"""
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    db.delete(idea)
    db.commit()
    return {"message": "Idea deleted successfully"}
