"""
데이터베이스 모델
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from .database import Base


class Channel(Base):
    """채널 모델"""
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)  # 채널 카테고리 (5개 중 선택)
    topic = Column(String(500), nullable=False)  # 채널 주제
    description = Column(Text)
    target_audience = Column(String(200))  # 타겟 청중
    content_style = Column(String(200))  # 콘텐츠 스타일
    keywords = Column(JSON)  # 키워드 리스트

    # 설정
    schedule_hours = Column(Integer, default=6)  # 실행 주기 (시간)
    schedule_time = Column(String(10))  # 시작 시간 (예: "09:00", "14:30")
    auto_upload = Column(Boolean, default=False)  # 자동 업로드 여부
    video_duration = Column(Integer, default=60)  # 영상 길이 (초)
    privacy_status = Column(String(20), default="private")  # YouTube 공개 상태

    # Google Sheets 연동
    google_sheet_id = Column(String(200))  # 구글시트 ID
    save_to_sheets = Column(Boolean, default=False)  # 시트 저장 여부

    # 템플릿
    creatomate_template_id = Column(String(100))

    # 통계
    total_videos = Column(Integer, default=0)
    total_views = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    ideas = relationship("Idea", back_populates="channel", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")


class Idea(Base):
    """아이디어 모델"""
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)

    title = Column(String(500), nullable=False)
    hook = Column(Text)  # 오프닝 문구
    content = Column(Text)  # 핵심 내용
    cta = Column(String(500))  # Call to Action
    keywords = Column(JSON)  # 키워드 리스트

    # 스크립트
    script = Column(Text)  # 전체 스크립트
    script_segments = Column(JSON)  # 세그먼트 [{time: "0-5", text: "..."}]

    # 상태
    status = Column(String(20), default="pending")  # pending, in_progress, completed, failed

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    channel = relationship("Channel", back_populates="ideas")
    videos = relationship("Video", back_populates="idea")


class Video(Base):
    """비디오 모델"""
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    idea_id = Column(Integer, ForeignKey("ideas.id"))

    title = Column(String(500), nullable=False)
    description = Column(Text)

    # 파일 경로
    audio_path = Column(String(500))
    subtitle_path = Column(String(500))
    video_path = Column(String(500))

    # 외부 서비스 ID
    creatomate_render_id = Column(String(100))
    youtube_video_id = Column(String(50))

    # 메타데이터
    duration = Column(Integer)  # 초
    file_size = Column(Integer)  # 바이트

    # 상태
    status = Column(String(20), default="pending")  # pending, rendering, completed, uploaded, failed
    error_message = Column(Text)

    # 통계
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    uploaded_at = Column(DateTime)

    # 관계
    channel = relationship("Channel", back_populates="videos")
    idea = relationship("Idea", back_populates="videos")


class WorkflowLog(Base):
    """워크플로우 실행 로그"""
    __tablename__ = "workflow_logs"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))

    step = Column(String(100))  # idea_generation, script_creation, tts, rendering, upload
    status = Column(String(20))  # started, completed, failed
    message = Column(Text)
    error = Column(Text)

    execution_time = Column(Integer)  # 실행 시간 (초)

    created_at = Column(DateTime, default=datetime.utcnow)
