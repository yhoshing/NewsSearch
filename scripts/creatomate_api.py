#!/usr/bin/env python3
"""
Creatomate API 통합 스크립트

Creatomate를 사용하여 템플릿 기반 비디오를 생성합니다.
"""

import os
import sys
import json
import time
import requests
from typing import Dict, Any, Optional


class CreatomateAPI:
    """Creatomate API 클라이언트"""

    def __init__(self, api_key: str):
        """
        초기화

        Args:
            api_key: Creatomate API 키
        """
        self.api_key = api_key
        self.base_url = "https://api.creatomate.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def create_render(
        self,
        template_id: str,
        modifications: Dict[str, Any],
        output_format: str = "mp4"
    ) -> Dict[str, Any]:
        """
        렌더링 작업 생성

        Args:
            template_id: Creatomate 템플릿 ID
            modifications: 템플릿 수정 사항
            output_format: 출력 포맷 (mp4, gif 등)

        Returns:
            렌더링 작업 정보
        """
        url = f"{self.base_url}/renders"

        payload = {
            "template_id": template_id,
            "modifications": modifications,
            "output_format": output_format
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()

        return response.json()

    def get_render_status(self, render_id: str) -> Dict[str, Any]:
        """
        렌더링 상태 확인

        Args:
            render_id: 렌더링 ID

        Returns:
            렌더링 상태 정보
        """
        url = f"{self.base_url}/renders/{render_id}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

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

        Raises:
            TimeoutError: 최대 대기 시간 초과
            RuntimeError: 렌더링 실패
        """
        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time

            if elapsed_time > max_wait_time:
                raise TimeoutError(
                    f"렌더링이 {max_wait_time}초 내에 완료되지 않았습니다."
                )

            status = self.get_render_status(render_id)

            print(f"렌더링 상태: {status.get('status')} (경과 시간: {elapsed_time:.1f}초)")

            if status.get("status") == "succeeded":
                return status

            if status.get("status") == "failed":
                error_message = status.get("error_message", "알 수 없는 오류")
                raise RuntimeError(f"렌더링 실패: {error_message}")

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
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"비디오가 저장되었습니다: {output_path}")
        return output_path

    def create_shorts_video(
        self,
        template_id: str,
        script_segments: list,
        audio_url: Optional[str] = None,
        background_video: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        쇼츠 영상 생성 (간편 메서드)

        Args:
            template_id: 템플릿 ID
            script_segments: 스크립트 세그먼트 리스트
            audio_url: 오디오 파일 URL (옵션)
            background_video: 배경 비디오 URL (옵션)

        Returns:
            렌더링 정보
        """
        modifications = {}

        # 텍스트 세그먼트 추가
        for i, segment in enumerate(script_segments, start=1):
            if isinstance(segment, dict):
                modifications[f"Text-{i}"] = segment.get("text", "")
            else:
                modifications[f"Text-{i}"] = str(segment)

        # 오디오 추가
        if audio_url:
            modifications["Audio"] = audio_url

        # 배경 비디오 추가
        if background_video:
            modifications["Background"] = background_video

        return self.create_render(template_id, modifications)


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description="Creatomate API를 사용한 비디오 생성")
    parser.add_argument("--api-key", help="Creatomate API 키 (환경 변수 CREATOMATE_API_KEY 사용 가능)")
    parser.add_argument("--template-id", required=True, help="템플릿 ID")
    parser.add_argument("--modifications", help="수정 사항 JSON 파일")
    parser.add_argument("--script", help="스크립트 JSON 파일 (segments 포함)")
    parser.add_argument("--audio-url", help="오디오 파일 URL")
    parser.add_argument("--wait", action="store_true", help="렌더링 완료 대기")
    parser.add_argument("--download", help="렌더링 완료 후 다운로드 경로")
    parser.add_argument("--output", "-o", help="렌더링 정보 출력 JSON 파일")

    args = parser.parse_args()

    # API 키 확인
    api_key = args.api_key or os.getenv("CREATOMATE_API_KEY")
    if not api_key:
        print("오류: API 키가 필요합니다. (--api-key 또는 CREATOMATE_API_KEY 환경 변수)", file=sys.stderr)
        sys.exit(1)

    # API 클라이언트 초기화
    client = CreatomateAPI(api_key)

    # 수정 사항 준비
    modifications = {}

    if args.modifications:
        with open(args.modifications, 'r', encoding='utf-8') as f:
            modifications = json.load(f)

    elif args.script:
        with open(args.script, 'r', encoding='utf-8') as f:
            script_data = json.load(f)

        segments = script_data.get("segments", [])

        # 세그먼트를 텍스트 레이어로 변환
        for i, segment in enumerate(segments, start=1):
            if isinstance(segment, dict):
                modifications[f"Text-{i}"] = segment.get("text", "")
            else:
                modifications[f"Text-{i}"] = str(segment)

        # 오디오 URL이 있으면 추가
        if args.audio_url:
            modifications["Audio"] = args.audio_url
        elif "audioUrl" in script_data:
            modifications["Audio"] = script_data["audioUrl"]

    else:
        print("오류: --modifications 또는 --script 중 하나가 필요합니다.", file=sys.stderr)
        sys.exit(1)

    # 렌더링 생성
    print(f"렌더링 생성 중... (템플릿: {args.template_id})")
    render_info = client.create_render(args.template_id, modifications)

    render_id = render_info.get("id")
    print(f"렌더링 ID: {render_id}")
    print(f"상태: {render_info.get('status')}")

    # 완료 대기
    if args.wait or args.download:
        print("\n렌더링 완료 대기 중...")
        try:
            final_render_info = client.wait_for_render(render_id)
            print(f"\n렌더링 완료!")
            print(f"비디오 URL: {final_render_info.get('url')}")

            # 다운로드
            if args.download:
                video_url = final_render_info.get("url")
                if video_url:
                    client.download_video(video_url, args.download)
                else:
                    print("오류: 비디오 URL을 찾을 수 없습니다.", file=sys.stderr)
                    sys.exit(1)

            render_info = final_render_info

        except (TimeoutError, RuntimeError) as e:
            print(f"\n오류: {e}", file=sys.stderr)
            sys.exit(1)

    # 결과 출력
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(render_info, f, indent=2, ensure_ascii=False)
        print(f"\n렌더링 정보가 저장되었습니다: {args.output}")
    else:
        print("\n렌더링 정보:")
        print(json.dumps(render_info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
