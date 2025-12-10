"""
자동화 워크플로우 엔진
"""
import os
import time
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from ..models import Channel, Idea, Video, WorkflowLog
from ..services.openai_service import OpenAIService
from ..services.elevenlabs_service import ElevenLabsService
from ..services.creatomate_service import CreatomateService
from ..services.youtube_service import YouTubeService


class WorkflowEngine:
    """워크플로우 자동화 엔진"""

    def __init__(self, db: Session):
        self.db = db
        self.openai = OpenAIService()
        self.elevenlabs = ElevenLabsService()
        self.creatomate = CreatomateService()
        self.youtube = None  # 필요시 초기화

    def log_step(
        self,
        channel_id: int,
        video_id: int,
        step: str,
        status: str,
        message: str = None,
        error: str = None,
        execution_time: int = None
    ):
        """워크플로우 단계 로그 기록"""
        log = WorkflowLog(
            channel_id=channel_id,
            video_id=video_id,
            step=step,
            status=status,
            message=message,
            error=error,
            execution_time=execution_time
        )
        self.db.add(log)
        self.db.commit()

    def generate_ideas(
        self,
        channel_id: int,
        num_ideas: int = 3
    ) -> List[Idea]:
        """
        채널의 주제를 기반으로 아이디어 생성

        Args:
            channel_id: 채널 ID
            num_ideas: 생성할 아이디어 수

        Returns:
            생성된 아이디어 리스트
        """
        start_time = time.time()

        try:
            # 채널 정보 조회
            channel = self.db.query(Channel).filter(Channel.id == channel_id).first()
            if not channel:
                raise ValueError(f"채널을 찾을 수 없습니다: {channel_id}")

            self.log_step(channel_id, None, "idea_generation", "started",
                         f"{num_ideas}개의 아이디어 생성 시작")

            # OpenAI로 아이디어 생성
            ideas_data = self.openai.generate_ideas(
                topic=channel.topic,
                target_audience=channel.target_audience,
                content_style=channel.content_style,
                num_ideas=num_ideas
            )

            # 데이터베이스에 저장
            ideas = []
            for idea_data in ideas_data:
                idea = Idea(
                    channel_id=channel_id,
                    title=idea_data.get("title"),
                    hook=idea_data.get("hook"),
                    content=idea_data.get("content"),
                    cta=idea_data.get("cta"),
                    keywords=idea_data.get("keywords", []),
                    status="pending"
                )
                self.db.add(idea)
                ideas.append(idea)

            self.db.commit()

            execution_time = int(time.time() - start_time)
            self.log_step(channel_id, None, "idea_generation", "completed",
                         f"{len(ideas)}개의 아이디어 생성 완료", execution_time=execution_time)

            return ideas

        except Exception as e:
            execution_time = int(time.time() - start_time)
            self.log_step(channel_id, None, "idea_generation", "failed",
                         error=str(e), execution_time=execution_time)
            raise

    def create_script(
        self,
        idea_id: int
    ) -> Idea:
        """
        아이디어를 스크립트로 변환

        Args:
            idea_id: 아이디어 ID

        Returns:
            스크립트가 추가된 아이디어
        """
        start_time = time.time()

        try:
            # 아이디어 조회
            idea = self.db.query(Idea).filter(Idea.id == idea_id).first()
            if not idea:
                raise ValueError(f"아이디어를 찾을 수 없습니다: {idea_id}")

            # 채널 정보 조회
            channel = self.db.query(Channel).filter(Channel.id == idea.channel_id).first()

            self.log_step(idea.channel_id, None, "script_creation", "started",
                         f"아이디어 '{idea.title}' 스크립트 생성 시작")

            # OpenAI로 스크립트 생성
            script_data = self.openai.generate_script(
                title=idea.title,
                hook=idea.hook,
                content=idea.content,
                cta=idea.cta,
                duration=channel.video_duration
            )

            # 아이디어 업데이트
            idea.script = script_data.get("script")
            idea.script_segments = script_data.get("segments", [])
            idea.status = "script_ready"
            self.db.commit()

            execution_time = int(time.time() - start_time)
            self.log_step(idea.channel_id, None, "script_creation", "completed",
                         f"스크립트 생성 완료", execution_time=execution_time)

            return idea

        except Exception as e:
            execution_time = int(time.time() - start_time)
            if idea:
                self.log_step(idea.channel_id, None, "script_creation", "failed",
                             error=str(e), execution_time=execution_time)
            raise

    def generate_audio(
        self,
        idea_id: int,
        output_dir: str = "./output/audio"
    ) -> str:
        """
        스크립트를 음성으로 변환

        Args:
            idea_id: 아이디어 ID
            output_dir: 출력 디렉토리

        Returns:
            오디오 파일 경로
        """
        start_time = time.time()

        try:
            # 아이디어 조회
            idea = self.db.query(Idea).filter(Idea.id == idea_id).first()
            if not idea:
                raise ValueError(f"아이디어를 찾을 수 없습니다: {idea_id}")

            if not idea.script:
                raise ValueError("스크립트가 없습니다. 먼저 스크립트를 생성하세요.")

            self.log_step(idea.channel_id, None, "tts", "started",
                         f"음성 합성 시작")

            # 출력 파일 경로
            timestamp = int(time.time())
            output_path = os.path.join(output_dir, f"audio_{idea.id}_{timestamp}.mp3")

            # ElevenLabs로 음성 생성
            audio_path = self.elevenlabs.generate_audio(
                text=idea.script,
                output_path=output_path
            )

            execution_time = int(time.time() - start_time)
            self.log_step(idea.channel_id, None, "tts", "completed",
                         f"음성 생성 완료: {audio_path}", execution_time=execution_time)

            return audio_path

        except Exception as e:
            execution_time = int(time.time() - start_time)
            if idea:
                self.log_step(idea.channel_id, None, "tts", "failed",
                             error=str(e), execution_time=execution_time)
            raise

    def render_video(
        self,
        idea_id: int,
        audio_path: str,
        output_dir: str = "./output/videos"
    ) -> Video:
        """
        Creatomate로 비디오 렌더링

        Args:
            idea_id: 아이디어 ID
            audio_path: 오디오 파일 경로
            output_dir: 출력 디렉토리

        Returns:
            비디오 객체
        """
        start_time = time.time()
        video = None

        try:
            # 아이디어 조회
            idea = self.db.query(Idea).filter(Idea.id == idea_id).first()
            if not idea:
                raise ValueError(f"아이디어를 찾을 수 없습니다: {idea_id}")

            # 채널 정보 조회
            channel = self.db.query(Channel).filter(Channel.id == idea.channel_id).first()
            if not channel.creatomate_template_id:
                raise ValueError("채널에 Creatomate 템플릿 ID가 설정되지 않았습니다.")

            # 비디오 객체 생성
            video = Video(
                channel_id=channel.id,
                idea_id=idea.id,
                title=idea.title,
                description=idea.content,
                audio_path=audio_path,
                status="rendering"
            )
            self.db.add(video)
            self.db.commit()

            self.log_step(channel.id, video.id, "rendering", "started",
                         f"비디오 렌더링 시작")

            # TODO: 오디오 파일을 URL로 업로드 (S3, Cloudinary 등)
            # 여기서는 로컬 경로를 사용한다고 가정
            audio_url = audio_path

            # Creatomate로 렌더링
            render_response = self.creatomate.create_shorts_video(
                template_id=channel.creatomate_template_id,
                script_segments=idea.script_segments or [],
                audio_url=audio_url
            )

            render_id = render_response.get("id")
            video.creatomate_render_id = render_id
            self.db.commit()

            # 렌더링 완료 대기
            render_result = self.creatomate.wait_for_render(render_id)

            # 비디오 다운로드
            video_url = render_result.get("url")
            if not video_url:
                raise ValueError("렌더링된 비디오 URL을 찾을 수 없습니다.")

            timestamp = int(time.time())
            output_path = os.path.join(output_dir, f"video_{video.id}_{timestamp}.mp4")

            video_path = self.creatomate.download_video(video_url, output_path)

            # 비디오 업데이트
            video.video_path = video_path
            video.status = "completed"
            self.db.commit()

            execution_time = int(time.time() - start_time)
            self.log_step(channel.id, video.id, "rendering", "completed",
                         f"비디오 렌더링 완료: {video_path}", execution_time=execution_time)

            return video

        except Exception as e:
            execution_time = int(time.time() - start_time)
            if video:
                video.status = "failed"
                video.error_message = str(e)
                self.db.commit()
                self.log_step(video.channel_id, video.id, "rendering", "failed",
                             error=str(e), execution_time=execution_time)
            raise

    def upload_to_youtube(
        self,
        video_id: int
    ) -> Video:
        """
        YouTube에 비디오 업로드

        Args:
            video_id: 비디오 ID

        Returns:
            업로드된 비디오 객체
        """
        start_time = time.time()

        try:
            # 비디오 조회
            video = self.db.query(Video).filter(Video.id == video_id).first()
            if not video:
                raise ValueError(f"비디오를 찾을 수 없습니다: {video_id}")

            if not video.video_path:
                raise ValueError("비디오 파일이 없습니다.")

            # 채널 정보 조회
            channel = self.db.query(Channel).filter(Channel.id == video.channel_id).first()

            self.log_step(channel.id, video.id, "upload", "started",
                         f"YouTube 업로드 시작")

            # YouTube 서비스 초기화
            if not self.youtube:
                self.youtube = YouTubeService()

            # 업로드
            upload_result = self.youtube.upload_video(
                video_file=video.video_path,
                title=video.title,
                description=video.description or "",
                keywords=video.idea.keywords if video.idea else [],
                privacy_status=channel.privacy_status
            )

            # 비디오 업데이트
            video.youtube_video_id = upload_result['id']
            video.status = "uploaded"
            video.uploaded_at = datetime.utcnow()
            self.db.commit()

            # 채널 통계 업데이트
            channel.total_videos += 1
            self.db.commit()

            execution_time = int(time.time() - start_time)
            self.log_step(channel.id, video.id, "upload", "completed",
                         f"YouTube 업로드 완료: {upload_result['url']}", execution_time=execution_time)

            return video

        except Exception as e:
            execution_time = int(time.time() - start_time)
            if video:
                video.status = "upload_failed"
                video.error_message = str(e)
                self.db.commit()
                self.log_step(video.channel_id, video.id, "upload", "failed",
                             error=str(e), execution_time=execution_time)
            raise

    def run_full_workflow(
        self,
        channel_id: int,
        mode: str = "generate",
        num_ideas: int = 3
    ) -> List[Video]:
        """
        전체 워크플로우 실행

        Args:
            channel_id: 채널 ID
            mode: 모드 (generate: 새 아이디어 생성, reuse: 기존 아이디어 사용)
            num_ideas: 생성할 비디오 수

        Returns:
            생성된 비디오 리스트
        """
        videos = []

        try:
            # 1. 아이디어 생성 또는 불러오기
            if mode == "generate":
                ideas = self.generate_ideas(channel_id, num_ideas)
            else:
                # 대기 중인 아이디어 조회
                ideas = self.db.query(Idea).filter(
                    Idea.channel_id == channel_id,
                    Idea.status == "pending"
                ).limit(num_ideas).all()

            # 2. 각 아이디어에 대해 워크플로우 실행
            for idea in ideas:
                try:
                    # 스크립트 생성
                    if not idea.script:
                        idea = self.create_script(idea.id)

                    # 음성 생성
                    audio_path = self.generate_audio(idea.id)

                    # 비디오 렌더링
                    video = self.render_video(idea.id, audio_path)

                    # 자동 업로드 설정이 되어 있으면 업로드
                    channel = self.db.query(Channel).filter(Channel.id == channel_id).first()
                    if channel.auto_upload:
                        video = self.upload_to_youtube(video.id)

                    videos.append(video)

                except Exception as e:
                    print(f"Error processing idea {idea.id}: {e}")
                    continue

            return videos

        except Exception as e:
            print(f"Error running workflow: {e}")
            raise
