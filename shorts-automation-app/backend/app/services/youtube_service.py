"""
YouTube 업로드 서비스
"""
import os
import pickle
from typing import Optional, Dict, Any

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False


SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


class YouTubeService:
    def __init__(self, credentials_file: str = "credentials.json", token_file: str = "token.pickle"):
        if not GOOGLE_LIBS_AVAILABLE:
            raise ImportError("Google 클라이언트 라이브러리가 필요합니다.")

        self.credentials_file = credentials_file
        self.token_file = token_file
        self.youtube = None

    def authenticate(self) -> None:
        """OAuth 2.0 인증 수행"""
        creds = None

        # 저장된 토큰 로드
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        # 유효하지 않은 토큰이면 갱신 또는 재인증
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("토큰 갱신 중...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"OAuth 클라이언트 ID 파일을 찾을 수 없습니다: {self.credentials_file}"
                    )

                print("OAuth 인증 시작...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # 토큰 저장
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        # YouTube API 클라이언트 생성
        self.youtube = build('youtube', 'v3', credentials=creds)
        print("YouTube API 인증 완료")

    def upload_video(
        self,
        video_file: str,
        title: str,
        description: str = "",
        category_id: str = "22",
        keywords: list = None,
        privacy_status: str = "private"
    ) -> Dict[str, Any]:
        """
        비디오 업로드

        Args:
            video_file: 비디오 파일 경로
            title: 비디오 제목
            description: 비디오 설명
            category_id: 카테고리 ID (22 = People & Blogs)
            keywords: 태그 리스트
            privacy_status: 공개 상태 (public, private, unlisted)

        Returns:
            업로드된 비디오 정보
        """
        if not self.youtube:
            self.authenticate()

        if not os.path.exists(video_file):
            raise FileNotFoundError(f"비디오 파일을 찾을 수 없습니다: {video_file}")

        # 비디오 메타데이터
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }

        # 태그 추가
        if keywords:
            body['snippet']['tags'] = keywords

        # 미디어 파일 업로드
        media = MediaFileUpload(
            video_file,
            mimetype='video/*',
            resumable=True,
            chunksize=1024*1024
        )

        print(f"업로드 시작: {video_file}")

        # 업로드 요청
        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )

        # 업로드 진행
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"업로드 진행: {progress}%")

        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"업로드 완료!")
        print(f"비디오 ID: {video_id}")
        print(f"URL: {video_url}")

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'privacyStatus': privacy_status,
            'response': response
        }
