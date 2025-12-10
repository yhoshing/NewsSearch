"""
Creatomate API 서비스
"""
import os
import time
import requests
from typing import Dict, Any, List, Optional


class CreatomateService:
    def __init__(self):
        self.api_key = os.getenv("CREATOMATE_API_KEY")
        self.base_url = "https://api.creatomate.com/v1"

    def create_render(
        self,
        template_id: str,
        modifications: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        렌더링 작업 생성

        Args:
            template_id: 템플릿 ID
            modifications: 수정 사항

        Returns:
            렌더링 정보
        """
        if not self.api_key:
            raise ValueError("CREATOMATE_API_KEY가 설정되지 않았습니다.")

        url = f"{self.base_url}/renders"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "template_id": template_id,
            "modifications": modifications
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error creating render: {e}")
            raise

    def get_render_status(self, render_id: str) -> Dict[str, Any]:
        """
        렌더링 상태 확인

        Args:
            render_id: 렌더링 ID

        Returns:
            렌더링 상태 정보
        """
        url = f"{self.base_url}/renders/{render_id}"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error getting render status: {e}")
            raise

    def wait_for_render(
        self,
        render_id: str,
        max_wait_time: int = 600,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """
        렌더링 완료 대기

        Args:
            render_id: 렌더링 ID
            max_wait_time: 최대 대기 시간 (초)
            poll_interval: 폴링 간격 (초)

        Returns:
            완료된 렌더링 정보
        """
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time

            if elapsed > max_wait_time:
                raise TimeoutError(f"렌더링이 {max_wait_time}초 내에 완료되지 않았습니다.")

            status = self.get_render_status(render_id)

            if status.get("status") == "succeeded":
                return status

            if status.get("status") == "failed":
                error = status.get("error_message", "알 수 없는 오류")
                raise RuntimeError(f"렌더링 실패: {error}")

            print(f"Rendering status: {status.get('status')} (elapsed: {elapsed:.1f}s)")
            time.sleep(poll_interval)

    def download_video(self, url: str, output_path: str) -> str:
        """
        렌더링된 비디오 다운로드

        Args:
            url: 비디오 URL
            output_path: 저장 경로

        Returns:
            저장된 파일 경로
        """
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            # 디렉토리 생성
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 파일 저장
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Video downloaded to: {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"Error downloading video: {e}")
            raise

    def create_shorts_video(
        self,
        template_id: str,
        script_segments: List[Dict],
        audio_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        쇼츠 영상 생성 (간편 메서드)

        Args:
            template_id: 템플릿 ID
            script_segments: 스크립트 세그먼트 리스트
            audio_url: 오디오 파일 URL (옵션)

        Returns:
            렌더링 정보
        """
        modifications = {}

        # 텍스트 세그먼트 추가
        for i, segment in enumerate(script_segments, start=1):
            text = segment.get("text", "") if isinstance(segment, dict) else str(segment)
            modifications[f"Text-{i}"] = text

        # 오디오 추가
        if audio_url:
            modifications["Audio"] = audio_url

        return self.create_render(template_id, modifications)
