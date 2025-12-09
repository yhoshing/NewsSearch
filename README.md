# 뉴스 쇼츠 자동 생성 워크플로우

최신 논란이 되는 뉴스를 자동으로 검색하고, AI를 활용하여 30초 분량의 쇼츠 영상을 자동 생성하는 n8n 워크플로우입니다.

## 주요 기능

- 📰 **자동 뉴스 수집**: NewsAPI를 통해 한국 최신 뉴스 자동 검색
- 🔍 **스마트 필터링**: 논란 키워드를 포함한 이슈 뉴스만 선별
- 🤖 **AI 스크립트 생성**: OpenAI GPT-4로 자연스러운 30초 쇼츠 스크립트 작성
- 🎙️ **음성 합성**: ElevenLabs의 고품질 TTS로 자연스러운 한국어 음성 생성
- 🎨 **이미지 생성**: DALL-E 3로 뉴스 주제에 맞는 시각 자료 생성
- 🎬 **비디오 합성**: FFmpeg로 이미지와 음성을 결합하여 완성된 쇼츠 영상 생성
- ⏰ **자동화**: 6시간마다 자동 실행 (설정 변경 가능)

## 워크플로우 구조

```
┌─────────────────┐
│  6시간마다 실행  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  뉴스 API 호출  │
│   (NewsAPI)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 논란 뉴스 필터링 │
│ (키워드 검색)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI 스크립트    │
│     생성        │
└────┬───────┬────┘
     │       │
     ▼       ▼
┌─────┐   ┌─────┐
│ TTS │   │이미지│
│음성 │   │생성 │
└──┬──┘   └──┬──┘
   │         │
   └────┬────┘
        ▼
   ┌─────────┐
   │ 비디오  │
   │  합성   │
   └────┬────┘
        ▼
   ┌─────────┐
   │  완료   │
   └─────────┘
```

## 필수 요구사항

### 1. n8n 설치

```bash
# Docker로 설치 (권장)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# 또는 npm으로 설치
npm install -g n8n
```

### 2. FFmpeg 설치

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# https://ffmpeg.org/download.html 에서 다운로드
```

### 3. API 키 발급

다음 서비스들의 API 키가 필요합니다:

#### NewsAPI
- 사이트: https://newsapi.org/
- 무료 플랜: 월 1,000개 요청
- 가입 후 API 키 발급

#### OpenAI
- 사이트: https://platform.openai.com/
- GPT-4 API 키 필요
- DALL-E 3 이미지 생성 포함
- 사용량 기반 과금

#### ElevenLabs
- 사이트: https://elevenlabs.io/
- 고품질 TTS 서비스
- 무료 플랜: 월 10,000 글자
- 한국어 음성 지원 확인 필요

## 설치 및 설정

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd NewsSearch
```

### 2. 환경 변수 설정

`.env.example` 파일을 `.env`로 복사하고 API 키를 입력합니다:

```bash
cp .env.example .env
```

`.env` 파일 편집:

```env
# NewsAPI 설정
NEWSAPI_KEY=your_newsapi_key_here

# OpenAI 설정
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs 설정
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=your_preferred_voice_id

# 출력 디렉토리
OUTPUT_DIR=/home/user/NewsSearch/output
```

### 3. n8n에 워크플로우 임포트

1. n8n 실행: `n8n start`
2. 브라우저에서 `http://localhost:5678` 접속
3. 우측 상단 메뉴 → **Import from File** 선택
4. `workflows/news-shorts-workflow.json` 파일 선택
5. 임포트 완료

### 4. n8n에 환경 변수 설정

n8n에서 환경 변수를 사용하는 방법:

**방법 1: Docker 환경 변수**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e NEWSAPI_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  -e ELEVENLABS_API_KEY=your_key \
  -e ELEVENLABS_VOICE_ID=your_voice_id \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**방법 2: n8n 설정 파일**

`~/.n8n/config` 파일 생성:
```json
{
  "env": {
    "NEWSAPI_KEY": "your_key",
    "OPENAI_API_KEY": "your_key",
    "ELEVENLABS_API_KEY": "your_key",
    "ELEVENLABS_VOICE_ID": "your_voice_id"
  }
}
```

### 5. 워크플로우 활성화

1. n8n 워크플로우 편집 화면에서
2. 우측 상단 **Inactive** 버튼 클릭
3. **Active**로 변경

## 사용 방법

### 자동 실행

워크플로우를 활성화하면 6시간마다 자동으로 실행됩니다.

### 수동 실행

1. n8n 워크플로우 편집 화면에서
2. 좌측 상단 **Execute Workflow** 버튼 클릭
3. 실행 결과 확인

### 생성된 영상 확인

생성된 쇼츠 영상은 `output/` 디렉토리에 저장됩니다:

```bash
ls -lh output/
# video_1702123456789.mp4
# video_1702234567890.mp4
```

## 커스터마이징

### 실행 주기 변경

워크플로우에서 "매 6시간마다 실행" 노드를 클릭하고 간격을 조정합니다:
- 매일 1회: `hours: 24`
- 매일 2회: `hours: 12`
- 매시간: `hours: 1`

### 논란 키워드 수정

"논란 뉴스 필터링" 노드의 코드에서 `controversialKeywords` 배열을 수정합니다:

```javascript
const controversialKeywords = [
  '논란', '갈등', '비판', '반발', // 기본 키워드
  '충격', '폭로', '사과',         // 추가 키워드
  // 여기에 원하는 키워드 추가
];
```

### 영상 길이 조정

"AI 스크립트 생성" 노드에서 프롬프트를 수정합니다:

```javascript
// 30초 -> 60초로 변경
"요구사항:\n1. 시청자의 관심을 끄는 강렬한 오프닝 (5초)\n2. 핵심 내용 전달 (45초)\n3. 임팩트 있는 마무리 (10초)\n4. 구어체로 자연스럽게 작성\n5. 총 글자수 300-400자 이내"
```

### 비디오 해상도 변경

"비디오 합성 준비" 노드에서 FFmpeg 명령어의 해상도를 조정합니다:

```javascript
// 1080x1920 (세로) -> 1920x1080 (가로)로 변경
'-vf \"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1\"'
```

### AI 모델 변경

**OpenAI 모델 변경**:
- "AI 스크립트 생성" 노드에서 model 선택
- `gpt-4` → `gpt-4-turbo` 또는 `gpt-3.5-turbo`

**이미지 생성 모델 변경**:
- DALL-E 대신 Stability AI 사용 가능
- HTTP Request 노드로 Stability AI API 호출

## 비용 예상

### API 사용 비용 (월 100개 쇼츠 생성 기준)

| 서비스 | 사용량 | 예상 비용 |
|--------|--------|-----------|
| NewsAPI | ~500 요청 | 무료 (무료 플랜 내) |
| OpenAI GPT-4 | ~100 요청 | $3-5 |
| DALL-E 3 | ~100 이미지 | $10-12 |
| ElevenLabs | ~20,000 글자 | $5 (Starter 플랜) |
| **합계** | | **$18-22/월** |

무료 플랜 활용:
- NewsAPI: 월 1,000 요청까지 무료
- ElevenLabs: 월 10,000 글자까지 무료
- OpenAI: 크레딧 제공 (신규 가입시)

## 트러블슈팅

### 문제: 뉴스가 검색되지 않음

**해결책**:
- NewsAPI 키가 올바른지 확인
- API 할당량 초과 여부 확인
- NewsAPI 대시보드에서 사용량 확인

### 문제: 음성이 생성되지 않음

**해결책**:
- ElevenLabs API 키 확인
- Voice ID가 올바른지 확인
- ElevenLabs 대시보드에서 사용 가능한 음성 목록 확인
- 한국어 지원 음성인지 확인

### 문제: FFmpeg 오류

**해결책**:
```bash
# FFmpeg 설치 확인
ffmpeg -version

# 권한 확인
chmod +x /usr/bin/ffmpeg

# 출력 디렉토리 권한 확인
chmod 755 output/
```

### 문제: 환경 변수를 찾을 수 없음

**해결책**:
- n8n 재시작
- Docker 컨테이너 재시작
- 환경 변수 설정 방법 재확인

### 문제: 이미지 생성 실패

**해결책**:
- OpenAI API 키 확인
- DALL-E 3 접근 권한 확인
- 프롬프트가 너무 길지 않은지 확인
- 콘텐츠 정책 위반 여부 확인

## 대체 방안

### NewsAPI 대신 다른 뉴스 소스

**Google News RSS**:
```javascript
// HTTP Request 노드 URL
https://news.google.com/rss/search?q=논란&hl=ko&gl=KR&ceid=KR:ko
```

**네이버 뉴스 API**:
- https://developers.naver.com/
- 네이버 검색 API 활용

### ElevenLabs 대신 다른 TTS

**Google Cloud TTS**:
```bash
# gcloud 설치 후
gcloud auth application-default login
```

**Azure Cognitive Services**:
- https://azure.microsoft.com/ko-kr/services/cognitive-services/text-to-speech/

**무료 대안 - gTTS (Google Text-to-Speech)**:
```python
# Python 스크립트 노드 사용
from gtts import gTTS
tts = gTTS(text='스크립트 내용', lang='ko')
tts.save('output.mp3')
```

## 고급 기능

### YouTube 자동 업로드

YouTube Data API를 사용하여 생성된 영상을 자동으로 업로드할 수 있습니다:

1. Google Cloud Console에서 YouTube Data API v3 활성화
2. OAuth 2.0 인증 설정
3. n8n의 YouTube 노드 추가
4. 워크플로우 끝에 연결

### 자막 추가

FFmpeg로 자막을 추가할 수 있습니다:

```javascript
// 자막 생성
const subtitles = generateSubtitles(script);

// FFmpeg 명령에 자막 추가
-vf "subtitles=subtitles.srt:force_style='FontSize=24,PrimaryColour=&HFFFFFF'"
```

### 배경 음악 추가

```javascript
// FFmpeg 명령에 배경음악 추가
-i background_music.mp3 -filter_complex "[1:a]volume=0.2[bg];[0:a][bg]amix=inputs=2[a]" -map 0:v -map "[a]"
```

### 여러 이미지/클립 사용

정적 이미지 대신 여러 이미지를 슬라이드쇼로 표시:

```javascript
ffmpeg -loop 1 -t 10 -i image1.jpg \
       -loop 1 -t 10 -i image2.jpg \
       -loop 1 -t 10 -i image3.jpg \
       -i audio.mp3 \
       -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]" \
       -map "[v]" -map 3:a output.mp4
```

## 라이센스

MIT License

## 기여

Pull Request를 환영합니다!

## 문의

이슈가 있으시면 GitHub Issues에 등록해주세요.

## 업데이트 로그

### v1.0.0 (2025-12-09)
- 초기 릴리스
- 기본 워크플로우 구현
- 뉴스 검색, AI 스크립트, TTS, 이미지 생성, 비디오 합성 기능

## 향후 계획

- [ ] YouTube 자동 업로드 기능
- [ ] 자막 자동 생성
- [ ] 배경 음악 자동 추가
- [ ] 다양한 영상 스타일 템플릿
- [ ] 웹 대시보드 (생성된 영상 관리)
- [ ] 성능 분석 (조회수, 참여도 추적)
- [ ] 다국어 지원
