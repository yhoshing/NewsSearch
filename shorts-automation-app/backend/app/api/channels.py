"""
Channels API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Channel
from ..schemas import ChannelCreate, ChannelUpdate, Channel as ChannelSchema, ChannelStats

router = APIRouter()


@router.post("/", response_model=ChannelSchema)
def create_channel(channel: ChannelCreate, db: Session = Depends(get_db)):
    """새 채널 생성"""
    db_channel = Channel(**channel.dict())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel


@router.get("/", response_model=List[ChannelSchema])
def list_channels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """채널 목록 조회"""
    channels = db.query(Channel).offset(skip).limit(limit).all()
    return channels


@router.get("/{channel_id}", response_model=ChannelSchema)
def get_channel(channel_id: int, db: Session = Depends(get_db)):
    """채널 상세 조회"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel


@router.put("/{channel_id}", response_model=ChannelSchema)
def update_channel(channel_id: int, channel_update: ChannelUpdate, db: Session = Depends(get_db)):
    """채널 수정"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    update_data = channel_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(channel, key, value)

    db.commit()
    db.refresh(channel)
    return channel


@router.delete("/{channel_id}")
def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    """채널 삭제"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    db.delete(channel)
    db.commit()
    return {"message": "Channel deleted successfully"}


@router.get("/{channel_id}/stats", response_model=ChannelStats)
def get_channel_stats(channel_id: int, db: Session = Depends(get_db)):
    """채널 통계 조회"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    # 최근 비디오 조회
    recent_videos = channel.videos[:10]

    # 평균 조회수 계산
    total_views = sum(v.views for v in channel.videos)
    avg_views = total_views / len(channel.videos) if channel.videos else 0

    total_likes = sum(v.likes for v in channel.videos)

    return {
        "total_videos": channel.total_videos,
        "total_views": total_views,
        "total_likes": total_likes,
        "avg_views_per_video": avg_views,
        "recent_videos": recent_videos
    }
