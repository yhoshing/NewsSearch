"""
FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .api import channels, ideas, videos, workflow

# FastAPI 앱 생성
app = FastAPI(
    title="Shorts Automation API",
    description="쇼츠 영상 자동 생성 시스템 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화
@app.on_event("startup")
async def startup_event():
    init_db()
    print("데이터베이스 초기화 완료")

# API 라우터 등록
app.include_router(channels.router, prefix="/api/channels", tags=["Channels"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["Ideas"])
app.include_router(videos.router, prefix="/api/videos", tags=["Videos"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow"])

@app.get("/")
async def root():
    return {
        "message": "Shorts Automation API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}
