"""
Videos API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Video
from ..schemas import VideoCreate, Video as VideoSchema

router = APIRouter()


@router.post("/", response_model=VideoSchema)
def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    """새 비디오 생성"""
    db_video = Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


@router.get("/", response_model=List[VideoSchema])
def list_videos(
    channel_id: int = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """비디오 목록 조회"""
    query = db.query(Video)

    if channel_id:
        query = query.filter(Video.channel_id == channel_id)

    if status:
        query = query.filter(Video.status == status)

    videos = query.order_by(Video.created_at.desc()).offset(skip).limit(limit).all()
    return videos


@router.get("/{video_id}", response_model=VideoSchema)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """비디오 상세 조회"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.delete("/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):
    """비디오 삭제"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    db.delete(video)
    db.commit()
    return {"message": "Video deleted successfully"}
