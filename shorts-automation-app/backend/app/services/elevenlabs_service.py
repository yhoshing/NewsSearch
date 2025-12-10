"""
ElevenLabs TTS 서비스
"""
import os
import requests
from typing import Optional


class ElevenLabsService:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID")
        self.base_url = "https://api.elevenlabs.io/v1"

    def generate_audio(
        self,
        text: str,
        output_path: str,
        voice_id: Optional[str] = None
    ) -> str:
        """
        텍스트를 음성으로 변환

        Args:
            text: 변환할 텍스트
            output_path: 저장 경로
            voice_id: 음성 ID (없으면 기본값 사용)

        Returns:
            저장된 파일 경로
        """
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY가 설정되지 않았습니다.")

        voice = voice_id or self.voice_id
        if not voice:
            raise ValueError("ELEVENLABS_VOICE_ID가 설정되지 않았습니다.")

        url = f"{self.base_url}/text-to-speech/{voice}"

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()

            # 디렉토리 생성
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 파일 저장
            with open(output_path, 'wb') as f:
                f.write(response.content)

            print(f"Audio saved to: {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"Error generating audio: {e}")
            raise

    def get_voices(self):
        """사용 가능한 음성 목록 조회"""
        url = f"{self.base_url}/voices"

        headers = {
            "xi-api-key": self.api_key
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error getting voices: {e}")
            return {"voices": []}
