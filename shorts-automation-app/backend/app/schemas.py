"""
Pydantic 스키마
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Channel Schemas
class ChannelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., description="카테고리 (psychology_test, history_mystery, health_tips, psychology_law, conspiracy)")
    topic: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    target_audience: Optional[str] = None
    content_style: Optional[str] = None
    keywords: Optional[List[str]] = None


class ChannelCreate(ChannelBase):
    schedule_hours: int = Field(default=6, ge=1, le=168)
    schedule_time: Optional[str] = Field(default=None, description="시작 시간 (예: 09:00)")
    auto_upload: bool = False
    video_duration: int = Field(default=60, ge=15, le=300)
    privacy_status: str = Field(default="private", pattern="^(public|private|unlisted)$")
    creatomate_template_id: Optional[str] = None
    google_sheet_id: Optional[str] = None
    save_to_sheets: bool = False


class ChannelUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    topic: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    content_style: Optional[str] = None
    keywords: Optional[List[str]] = None
    schedule_hours: Optional[int] = None
    schedule_time: Optional[str] = None
    auto_upload: Optional[bool] = None
    video_duration: Optional[int] = None
    privacy_status: Optional[str] = None
    creatomate_template_id: Optional[str] = None
    google_sheet_id: Optional[str] = None
    save_to_sheets: Optional[bool] = None


class Channel(ChannelBase):
    id: int
    schedule_hours: int
    schedule_time: Optional[str]
    auto_upload: bool
    video_duration: int
    privacy_status: str
    creatomate_template_id: Optional[str]
    google_sheet_id: Optional[str]
    save_to_sheets: bool
    total_videos: int
    total_views: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Idea Schemas
class IdeaBase(BaseModel):
    title: str
    hook: Optional[str] = None
    content: Optional[str] = None
    cta: Optional[str] = None
    keywords: Optional[List[str]] = None


class IdeaCreate(IdeaBase):
    channel_id: int


class IdeaWithScript(IdeaBase):
    id: int
    channel_id: int
    script: Optional[str] = None
    script_segments: Optional[List[dict]] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Video Schemas
class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None


class VideoCreate(VideoBase):
    channel_id: int
    idea_id: Optional[int] = None


class Video(VideoBase):
    id: int
    channel_id: int
    idea_id: Optional[int]
    audio_path: Optional[str]
    subtitle_path: Optional[str]
    video_path: Optional[str]
    creatomate_render_id: Optional[str]
    youtube_video_id: Optional[str]
    duration: Optional[int]
    file_size: Optional[int]
    status: str
    error_message: Optional[str]
    views: int
    likes: int
    comments: int
    created_at: datetime
    updated_at: datetime
    uploaded_at: Optional[datetime]

    class Config:
        from_attributes = True


# Workflow Schemas
class WorkflowStart(BaseModel):
    channel_id: int
    mode: str = Field(default="generate", pattern="^(generate|reuse)$")
    num_ideas: int = Field(default=3, ge=1, le=10)


class WorkflowStatus(BaseModel):
    channel_id: int
    status: str
    current_step: Optional[str] = None
    progress: int
    message: Optional[str] = None


# Statistics Schema
class ChannelStats(BaseModel):
    total_videos: int
    total_views: int
    total_likes: int
    avg_views_per_video: float
    recent_videos: List[Video]
