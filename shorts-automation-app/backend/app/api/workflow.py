"""
Workflow API
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Channel, Video, WorkflowLog
from ..schemas import WorkflowStart, WorkflowStatus
from ..workflow.automation import WorkflowEngine

router = APIRouter()


def run_workflow_background(channel_id: int, mode: str, num_ideas: int, db: Session):
    """백그라운드에서 워크플로우 실행"""
    try:
        engine = WorkflowEngine(db)
        engine.run_full_workflow(channel_id, mode, num_ideas)
    except Exception as e:
        print(f"Workflow error: {e}")
    finally:
        db.close()


@router.post("/start")
async def start_workflow(
    workflow: WorkflowStart,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """워크플로우 시작"""
    # 채널 확인
    channel = db.query(Channel).filter(Channel.id == workflow.channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    # 백그라운드에서 워크플로우 실행
    background_tasks.add_task(
        run_workflow_background,
        workflow.channel_id,
        workflow.mode,
        workflow.num_ideas,
        db
    )

    return {
        "message": "Workflow started",
        "channel_id": workflow.channel_id,
        "mode": workflow.mode,
        "num_ideas": workflow.num_ideas
    }


@router.post("/generate-ideas/{channel_id}")
async def generate_ideas(channel_id: int, num_ideas: int = 3, db: Session = Depends(get_db)):
    """아이디어 생성"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    try:
        engine = WorkflowEngine(db)
        ideas = engine.generate_ideas(channel_id, num_ideas)
        return {"ideas": ideas, "count": len(ideas)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-script/{idea_id}")
async def create_script(idea_id: int, db: Session = Depends(get_db)):
    """스크립트 생성"""
    try:
        engine = WorkflowEngine(db)
        idea = engine.create_script(idea_id)
        return {"idea": idea}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-audio/{idea_id}")
async def generate_audio(idea_id: int, db: Session = Depends(get_db)):
    """음성 생성"""
    try:
        engine = WorkflowEngine(db)
        audio_path = engine.generate_audio(idea_id)
        return {"audio_path": audio_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/render-video/{idea_id}")
async def render_video(idea_id: int, audio_path: str, db: Session = Depends(get_db)):
    """비디오 렌더링"""
    try:
        engine = WorkflowEngine(db)
        video = engine.render_video(idea_id, audio_path)
        return {"video": video}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-youtube/{video_id}")
async def upload_youtube(video_id: int, db: Session = Depends(get_db)):
    """YouTube 업로드"""
    try:
        engine = WorkflowEngine(db)
        video = engine.upload_to_youtube(video_id)
        return {"video": video}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{channel_id}")
async def get_workflow_status(channel_id: int, db: Session = Depends(get_db)):
    """워크플로우 상태 조회"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    # 최근 로그 조회
    recent_logs = db.query(WorkflowLog).filter(
        WorkflowLog.channel_id == channel_id
    ).order_by(WorkflowLog.created_at.desc()).limit(10).all()

    # 진행 중인 비디오 확인
    in_progress_videos = db.query(Video).filter(
        Video.channel_id == channel_id,
        Video.status.in_(["pending", "rendering"])
    ).count()

    status = "idle"
    current_step = None
    progress = 0

    if recent_logs:
        latest_log = recent_logs[0]
        if latest_log.status == "started":
            status = "running"
            current_step = latest_log.step
            progress = 50  # 간단한 진행률

    return {
        "channel_id": channel_id,
        "status": status,
        "current_step": current_step,
        "progress": progress,
        "in_progress_videos": in_progress_videos,
        "recent_logs": recent_logs
    }


@router.get("/logs/{channel_id}")
async def get_workflow_logs(
    channel_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """워크플로우 로그 조회"""
    logs = db.query(WorkflowLog).filter(
        WorkflowLog.channel_id == channel_id
    ).order_by(WorkflowLog.created_at.desc()).offset(skip).limit(limit).all()

    return {"logs": logs, "count": len(logs)}
