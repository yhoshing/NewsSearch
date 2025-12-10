# 🎬 쇼츠 자동화 설치 가이드 (초보자용)

완전 초보자를 위한 단계별 설치 가이드입니다.

---

## ✅ 사전 준비물

- 컴퓨터 (Windows, Mac, Linux 모두 가능)
- 인터넷 연결
- 신용카드 (API 서비스 가입용, 무료 체험 가능)

---

## 📝 1단계: Docker 설치

### Windows 사용자

1. 브라우저에서 https://www.docker.com/products/docker-desktop/ 접속
2. **"Download for Windows"** 버튼 클릭
3. 다운로드된 `Docker Desktop Installer.exe` 파일 실행
4. 설치 마법사 따라가기 (기본 설정 그대로 OK)
5. 설치 완료 후 **컴퓨터 재시작**
6. Docker Desktop 실행 → 우측 하단에 고래 아이콘이 보이면 성공!

### Mac 사용자

1. 브라우저에서 https://www.docker.com/products/docker-desktop/ 접속
2. **"Download for Mac"** 버튼 클릭
   - M1/M2 맥: Apple Chip 선택
   - Intel 맥: Intel Chip 선택
3. 다운로드된 `Docker.dmg` 파일 실행
4. Docker 아이콘을 Applications 폴더로 드래그
5. Applications에서 Docker 실행
6. 상단 메뉴바에 고래 아이콘이 보이면 성공!

### 설치 확인

터미널(Mac) 또는 명령 프롬프트(Windows)를 열고 다음 명령어 입력:

```bash
docker --version
```

다음과 같이 나오면 성공:
```
Docker version 24.0.6, build xxx
```

---

## 📝 2단계: API 키 발급받기

### 2-1. OpenAI API 키 (필수)

**가입 및 설정:**

1. https://platform.openai.com/ 접속
2. **"Sign up"** 클릭 → 구글 계정 또는 이메일로 가입
3. 로그인 후 우측 상단 프로필 클릭
4. **"View API keys"** 선택
5. **"+ Create new secret key"** 클릭
6. Name: `shorts-automation` 입력 → **Create**
7. **생성된 키를 복사** (한 번만 보여주므로 반드시 저장!)

**메모장에 다음 형식으로 저장:**
```
OpenAI API Key: sk-proj-xxxxxxxxxxxxx
```

**비용:**
- 신규 가입시 $5 크레딧 제공
- GPT-4 사용료: 요청당 약 $0.06
- 월 100개 영상 기준: 약 $6-10

### 2-2. ElevenLabs API 키 (필수)

**가입 및 설정:**

1. https://elevenlabs.io/ 접속
2. **"Get Started"** 클릭 → 구글 계정으로 가입
3. 로그인 후 우측 상단 프로필 아이콘 클릭
4. **"Profile"** 선택
5. **API Key** 섹션에서 키 복사

**음성 ID 찾기:**

1. 왼쪽 메뉴에서 **"Voices"** 클릭
2. 사용할 음성 선택 (한국어 지원 음성 선택)
3. 음성 이름 옆 설정 버튼 → **Voice ID** 복사

**메모장에 저장:**
```
ElevenLabs API Key: xxxxxxxxxxxxx
ElevenLabs Voice ID: xxxxxxxxxxxxx
```

**비용:**
- 무료 플랜: 월 10,000 글자
- Starter 플랜: 월 $5 (30,000 글자)

### 2-3. Creatomate API 키 (필수)

**가입 및 설정:**

1. https://creatomate.com/ 접속
2. **"Start Free Trial"** 클릭 → 이메일로 가입
3. 로그인 후 좌측 메뉴 **"API Keys"** 클릭
4. API Key 복사

**템플릿 ID 찾기:**

1. 좌측 메뉴 **"Templates"** 클릭
2. **"+ Create Template"** 또는 기존 템플릿 선택
3. 템플릿 이름 옆의 ID 복사 (예: `abc123xyz`)

**메모장에 저장:**
```
Creatomate API Key: xxxxxxxxxxxxx
Creatomate Template ID: abc123xyz
```

**비용:**
- 무료 체험: 25 렌더
- Starter 플랜: 월 $19 (200 렌더)

### 2-4. YouTube API (선택사항)

자동 업로드 기능을 사용하려면:

1. https://console.cloud.google.com/ 접속
2. 새 프로젝트 생성
3. YouTube Data API v3 활성화
4. OAuth 2.0 클라이언트 ID 생성 (데스크톱 앱)
5. `credentials.json` 다운로드 → 나중에 사용

---

## 📝 3단계: 프로젝트 설정

### 3-1. 터미널 열기

**Windows:**
- `Win + R` → `cmd` 입력 → Enter

**Mac:**
- `Command + Space` → `terminal` 입력 → Enter

### 3-2. 프로젝트 폴더로 이동

터미널에 다음 명령어 입력:

```bash
cd /home/user/NewsSearch/shorts-automation-app
```

### 3-3. 환경 변수 파일 생성

```bash
cp .env.example .env
```

### 3-4. API 키 입력

**방법 1: 텍스트 에디터로 열기 (추천)**

```bash
# Mac
open -a TextEdit .env

# Windows
notepad .env
```

**방법 2: nano 에디터 사용**

```bash
nano .env
```

**다음 내용을 입력** (아까 메모장에 저장한 키 사용):

```env
# OpenAI API
OPENAI_API_KEY=sk-proj-여기에_실제_키_붙여넣기

# ElevenLabs TTS
ELEVENLABS_API_KEY=여기에_실제_키_붙여넣기
ELEVENLABS_VOICE_ID=여기에_실제_음성ID_붙여넣기

# Creatomate
CREATOMATE_API_KEY=여기에_실제_키_붙여넣기

# Database (그대로 두기)
DATABASE_URL=sqlite:///./database/shorts_automation.db

# Frontend (그대로 두기)
REACT_APP_API_URL=http://localhost:8000/api
```

**저장하기:**
- TextEdit/Notepad: `Ctrl+S` (Windows) 또는 `Cmd+S` (Mac)
- nano: `Ctrl+X` → `Y` → Enter

---

## 📝 4단계: 프로그램 실행

### 4-1. Docker Compose로 실행

터미널에서 다음 명령어 입력:

```bash
docker-compose up -d
```

**처음 실행시 시간이 걸립니다 (5-10분)**
- Docker 이미지 다운로드 중...
- 패키지 설치 중...
- 잠시 기다려주세요!

### 4-2. 실행 확인

```bash
docker-compose ps
```

다음과 같이 나오면 성공:
```
NAME                              STATUS
shorts-automation-app-backend-1   Up
shorts-automation-app-frontend-1  Up
```

---

## 📝 5단계: 웹브라우저에서 접속

### 5-1. Frontend 접속

브라우저에서 다음 주소 입력:

```
http://localhost:3000
```

**쇼츠 자동화 대시보드**가 나타나면 성공! 🎉

### 5-2. Backend API 문서 확인

```
http://localhost:8000/docs
```

API 문서를 볼 수 있습니다.

---

## 📝 6단계: 첫 채널 만들기

### 6-1. 채널 생성

1. http://localhost:3000 접속
2. 상단 메뉴 **"채널 관리"** 클릭
3. **"+ 새 채널 만들기"** 버튼 클릭
4. 채널 정보 입력:

```
채널 이름: AI 뉴스 채널
주제: 인공지능과 기술 관련 최신 뉴스를 재미있게 전달
타겟 청중: 20-30대 IT 종사자
콘텐츠 스타일: 유머러스하고 친근한
키워드: AI, 기술, 뉴스
실행 주기: 6시간
영상 길이: 60초
Creatomate 템플릿 ID: 아까 복사한 템플릿 ID
자동 업로드: 체크 해제 (처음엔 수동으로)
```

5. **"저장"** 버튼 클릭

### 6-2. 워크플로우 실행

1. 생성한 채널 클릭
2. **"🚀 워크플로우 실행 (신규 아이디어)"** 버튼 클릭
3. 워크플로우가 시작됩니다!

**진행 순서:**
1. 아이디어 생성 (1-2분)
2. 스크립트 작성 (1-2분)
3. 음성 합성 (30초-1분)
4. 비디오 렌더링 (2-5분)

### 6-3. 결과 확인

1. 하단 **"비디오"** 섹션에서 생성된 영상 확인
2. 상태가 **"completed"**가 되면 완료!

---

## 📝 7단계: 프로그램 정지/재시작

### 정지하기

```bash
docker-compose down
```

### 재시작하기

```bash
docker-compose up -d
```

### 로그 확인하기

```bash
# Backend 로그
docker-compose logs backend

# Frontend 로그
docker-compose logs frontend

# 실시간 로그
docker-compose logs -f
```

---

## 🆘 문제 해결

### 문제: "docker: command not found"

**해결:**
- Docker가 설치되지 않았습니다
- 1단계로 돌아가서 Docker 설치

### 문제: "port is already allocated"

**해결:**
```bash
# 실행 중인 프로세스 종료
docker-compose down

# 다시 시작
docker-compose up -d
```

### 문제: "API key is invalid"

**해결:**
- `.env` 파일을 다시 확인
- API 키가 정확한지 확인
- 공백이나 따옴표가 없는지 확인

### 문제: Frontend가 안 열립니다

**해결:**
```bash
# 상태 확인
docker-compose ps

# Frontend 재시작
docker-compose restart frontend

# 로그 확인
docker-compose logs frontend
```

### 문제: "Module not found" 오류

**해결:**
```bash
# 컨테이너 재빌드
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📞 추가 도움

문제가 계속되면:

1. 터미널에서 로그 확인:
   ```bash
   docker-compose logs
   ```

2. 로그를 복사해서 ChatGPT나 GitHub Issues에 질문

3. 완전히 재시작:
   ```bash
   docker-compose down -v
   docker-compose up -d --build
   ```

---

## 🎓 다음 단계

1. 여러 채널 만들어보기
2. 각 채널마다 다른 주제 설정
3. 워크플로우 자동 실행 설정
4. YouTube 자동 업로드 설정

---

**축하합니다! 🎉**

이제 AI 기반 쇼츠 영상 자동화 시스템을 사용할 준비가 되었습니다!
