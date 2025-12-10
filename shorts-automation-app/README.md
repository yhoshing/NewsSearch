# 🎬 Shorts Automation App

AI 기반 쇼츠 영상 자동 생성 웹 애플리케이션

n8n 워크플로우를 웹앱으로 구현한 시스템으로, 5개 이상의 채널을 운영하며 각 채널별로 주제에 맞는 쇼츠 영상을 자동으로 생성합니다.

## 주요 기능

### 채널 관리
- **다중 채널 지원**: 5개 이상의 채널을 동시에 운영
- **채널별 주제 설정**: 각 채널마다 고유한 주제, 타겟 청중, 콘텐츠 스타일 설정
- **자동화 스케줄**: 채널별로 실행 주기 설정 (예: 6시간마다)

### 아이디어 생성
- **AI 아이디어 생성**: GPT-4를 활용한 창의적인 콘텐츠 아이디어 자동 생성
- **재사용 모드**: 기존에 생성된 아이디어를 활용
- **아이디어 보관함**: 생성된 모든 아이디어 관리

### 자동화 워크플로우
1. **아이디어 생성**: GPT-4로 채널 주제에 맞는 아이디어 생성
2. **스크립트 작성**: 아이디어를 30-60초 분량의 스크립트로 변환
3. **음성 합성**: ElevenLabs TTS로 자연스러운 음성 생성
4. **비디오 렌더링**: Creatomate로 템플릿 기반 영상 생성
5. **YouTube 업로드**: 완성된 영상을 자동으로 YouTube에 업로드

### 대시보드
- 전체 채널 통계 (총 채널, 비디오, 조회수)
- 최근 생성된 비디오 목록
- 채널별 상세 정보

## 기술 스택

### Backend
- **FastAPI**: REST API 서버
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **SQLite**: 데이터베이스
- **Python 3.10+**

### Frontend
- **React 18**: UI 프레임워크
- **React Router**: 라우팅
- **Axios**: HTTP 클라이언트

### AI & Services
- **OpenAI GPT-4**: 아이디어 및 스크립트 생성
- **ElevenLabs**: 음성 합성 (TTS)
- **Creatomate**: 템플릿 기반 비디오 생성
- **YouTube Data API**: 자동 업로드

## 설치 및 실행

### 1. 사전 요구사항

- Docker & Docker Compose
- API 키:
  - OpenAI API Key
  - ElevenLabs API Key
  - Creatomate API Key
  - YouTube OAuth 2.0 인증 (선택사항)

### 2. 프로젝트 설정

```bash
# 레포지토리 클론
cd shorts-automation-app

# 환경 변수 설정
cp .env.example .env
# .env 파일에 API 키 입력

# Docker Compose로 실행
docker-compose up -d
```

### 3. 접속

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API 문서: http://localhost:8000/docs

### 4. 첫 채널 만들기

1. 웹 브라우저에서 http://localhost:3000 접속
2. "채널 관리" 메뉴 클릭
3. "+ 새 채널 만들기" 버튼 클릭
4. 채널 정보 입력:
   - **채널 이름**: 예) "AI 뉴스 채널"
   - **주제**: 예) "인공지능과 기술 관련 최신 뉴스를 재미있게 전달"
   - **타겟 청중**: 예) "20-30대 IT 종사자"
   - **콘텐츠 스타일**: 예) "유머러스하고 친근한"
   - **Creatomate 템플릿 ID**: 사용할 템플릿 ID
5. 저장

## 사용 방법

### 워크플로우 실행

1. **채널 상세 페이지 접속**
   - 대시보드 또는 채널 목록에서 채널 선택

2. **워크플로우 시작**
   - **신규 아이디어**: "워크플로우 실행 (신규 아이디어)" 버튼 클릭
   - **기존 아이디어**: "워크플로우 실행 (기존 아이디어)" 버튼 클릭

3. **진행 상황 확인**
   - 채널 상세 페이지에서 실시간 진행 상황 확인
   - 생성된 아이디어와 비디오 목록 확인

### 채널별 설정

각 채널마다 다음을 설정할 수 있습니다:

- **실행 주기**: 1시간 ~ 168시간 (1주일)
- **영상 길이**: 15초 ~ 300초 (5분)
- **YouTube 공개 상태**: 비공개, 일부 공개, 전체 공개
- **자동 업로드**: 켜기/끄기

## 프로젝트 구조

```
shorts-automation-app/
├── backend/
│   ├── app/
│   │   ├── api/               # API 라우터
│   │   │   ├── channels.py
│   │   │   ├── ideas.py
│   │   │   ├── videos.py
│   │   │   └── workflow.py
│   │   ├── services/          # 외부 API 서비스
│   │   │   ├── openai_service.py
│   │   │   ├── elevenlabs_service.py
│   │   │   ├── creatomate_service.py
│   │   │   └── youtube_service.py
│   │   ├── workflow/          # 자동화 엔진
│   │   │   └── automation.py
│   │   ├── models.py          # 데이터베이스 모델
│   │   ├── schemas.py         # Pydantic 스키마
│   │   ├── database.py        # 데이터베이스 설정
│   │   └── main.py           # FastAPI 앱
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/        # React 컴포넌트
│   │   ├── pages/            # 페이지 컴포넌트
│   │   ├── services/         # API 클라이언트
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## API 엔드포인트

### Channels
- `GET /api/channels` - 채널 목록
- `POST /api/channels` - 채널 생성
- `GET /api/channels/{id}` - 채널 상세
- `PUT /api/channels/{id}` - 채널 수정
- `DELETE /api/channels/{id}` - 채널 삭제

### Ideas
- `GET /api/ideas` - 아이디어 목록
- `POST /api/ideas` - 아이디어 생성
- `GET /api/ideas/{id}` - 아이디어 상세

### Videos
- `GET /api/videos` - 비디오 목록
- `GET /api/videos/{id}` - 비디오 상세

### Workflow
- `POST /api/workflow/start` - 전체 워크플로우 시작
- `POST /api/workflow/generate-ideas/{channel_id}` - 아이디어 생성
- `POST /api/workflow/create-script/{idea_id}` - 스크립트 생성
- `POST /api/workflow/generate-audio/{idea_id}` - 음성 생성
- `POST /api/workflow/render-video/{idea_id}` - 비디오 렌더링
- `POST /api/workflow/upload-youtube/{video_id}` - YouTube 업로드
- `GET /api/workflow/status/{channel_id}` - 워크플로우 상태

## 비용 예상 (월 100개 쇼츠 기준)

| 서비스 | 사용량 | 예상 비용 |
|--------|--------|-----------|
| OpenAI GPT-4 | ~200 요청 | $6-10 |
| ElevenLabs | ~20,000 글자 | $5 |
| Creatomate | ~100 렌더 | $19 |
| YouTube API | ~100 업로드 | 무료 |
| **합계** | | **$30-34/월** |

## 트러블슈팅

### 데이터베이스 초기화 오류
```bash
# 데이터베이스 디렉토리 삭제 후 재생성
docker-compose down -v
docker-compose up -d
```

### API 키 오류
- `.env` 파일에 올바른 API 키가 설정되어 있는지 확인
- Docker 컨테이너 재시작: `docker-compose restart`

### Creatomate 렌더링 실패
- 템플릿 ID가 올바른지 확인
- Creatomate 대시보드에서 템플릿의 레이어 이름 확인

## 라이선스

MIT License

## 기여

Pull Request를 환영합니다!

## 문의

이슈가 있으시면 GitHub Issues에 등록해주세요.
