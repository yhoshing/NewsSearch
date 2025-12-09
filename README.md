# 🎬 뉴스 쇼츠 자동 생성기

AI 기반으로 최신 뉴스를 분석하여 30초 분량의 유튜브 쇼츠 스크립트를 자동으로 생성하는 웹 애플리케이션입니다.

## ✨ 주요 기능

### 🎯 3가지 생성 모드

1. **📰 오늘 뉴스 기반**
   - SerpAPI로 최신 한국 뉴스 검색
   - 논란/이슈가 되는 뉴스 자동 분석
   - 뉴스 기반 30초 쇼츠 스크립트 생성

2. **🎬 유튜브 급상승 기반**
   - 유튜브에서 조회수가 높은 뉴스 쇼츠 분석
   - 트렌드 분석을 통한 바이럴 요소 추출
   - 급상승 트렌드 기반 스크립트 생성

3. **🔥 뉴스 + 급상승 결합**
   - 최신 뉴스와 유튜브 트렌드를 결합
   - 최적화된 바이럴 콘텐츠 스크립트 생성
   - 뉴스의 신뢰성 + 트렌드의 매력 결합

### 🤖 AI 자동 생성

- **스크립트**: GPT-4로 30초 분량의 자연스러운 한국어 스크립트 생성
- **제목**: 클릭을 유도하는 영상 제목 3개 추천
- **썸네일 문구**: 강렬한 임팩트를 주는 썸네일 텍스트 5개 제공
- **이미지 프롬프트**: DALL-E 3로 썸네일 이미지 생성을 위한 프롬프트 제공

### 🎙️ 추가 기능

- **TTS 음성 생성**: ElevenLabs로 자연스러운 한국어 음성 합성
- **썸네일 이미지**: DALL-E 3로 고품질 썸네일 이미지 생성
- **전체 자동화**: 클릭 한 번으로 스크립트 + 음성 + 썸네일 한 번에 생성
- **결과 다운로드**: 생성된 모든 결과를 JSON 파일로 저장

## 🏗️ 프로젝트 구조

```
NewsSearch/
├── backend/              # Node.js + Express 백엔드
│   ├── server.js         # 메인 서버 파일
│   ├── package.json      # 의존성 관리
│   └── .env.example      # 환경 변수 템플릿
│
├── frontend/             # 웹 프론트엔드
│   ├── index.html        # 메인 HTML
│   ├── style.css         # 스타일시트
│   └── app.js            # 프론트엔드 로직
│
├── output/               # 생성된 파일 저장
│   ├── voice_*.mp3       # TTS 음성 파일
│   └── thumbnail_*.png   # 썸네일 이미지
│
├── workflows/            # (레거시) n8n 워크플로우
└── scripts/              # 유틸리티 스크립트
```

## 🚀 빠른 시작

### 1. 사전 요구사항

- Node.js 18+ 설치
- API 키 발급 (아래 참조)

### 2. API 키 발급

#### SerpAPI (필수)
- 사이트: https://serpapi.com/
- 무료 플랜: 월 100회 검색
- 뉴스 + 유튜브 검색에 사용

#### OpenAI (필수)
- 사이트: https://platform.openai.com/
- GPT-4 + DALL-E 3 사용
- 스크립트 생성 및 이미지 생성

#### ElevenLabs (선택)
- 사이트: https://elevenlabs.io/
- 무료 플랜: 월 10,000 글자
- TTS 음성 합성에 사용

### 3. 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/yhoshing/NewsSearch.git
cd NewsSearch

# 2. 백엔드 설정
cd backend
npm install

# 3. 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 API 키 입력

# 4. 서버 실행
npm start
# 또는 개발 모드로 실행 (nodemon)
npm run dev
```

### 4. 브라우저에서 접속

```
http://localhost:3000
```

## ⚙️ 환경 변수 설정

`backend/.env` 파일을 생성하고 다음 값을 설정하세요:

```env
# 서버 포트
PORT=3000

# SerpAPI (필수)
SERPAPI_KEY=your_serpapi_key_here

# OpenAI API (필수)
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs (TTS 사용시 필수)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here
```

## 📖 사용 방법

### 기본 사용법

1. **웹 인터페이스 접속**
   - http://localhost:3000 접속

2. **생성 모드 선택**
   - 📰 오늘 뉴스 기반
   - 🎬 유튜브 급상승 기반
   - 🔥 뉴스 + 급상승 결합

3. **결과 확인**
   - 30초 스크립트
   - 추천 제목 3개
   - 썸네일 문구 5개
   - DALL-E 이미지 프롬프트

4. **추가 기능 사용**
   - 🎙️ 음성 생성 버튼 클릭
   - 🎨 썸네일 이미지 생성 버튼 클릭
   - ⚡ 전체 자동 생성 (한 번에 모두 생성)

### API 엔드포인트

백엔드 API를 직접 호출할 수도 있습니다:

```bash
# 뉴스 기반 스크립트 생성
curl -X POST http://localhost:3000/api/generate/news

# 유튜브 급상승 기반
curl -X POST http://localhost:3000/api/generate/youtube

# 결합 모드
curl -X POST http://localhost:3000/api/generate/mixed

# TTS 음성 생성
curl -X POST http://localhost:3000/api/generate/voice \
  -H "Content-Type: application/json" \
  -d '{"script": "여기에 스크립트 입력"}'

# 썸네일 이미지 생성
curl -X POST http://localhost:3000/api/generate/thumbnail \
  -H "Content-Type: application/json" \
  -d '{"prompt": "dramatic news thumbnail"}'

# 전체 자동화
curl -X POST http://localhost:3000/api/generate/complete \
  -H "Content-Type: application/json" \
  -d '{"mode": "mixed"}'
```

## 💰 비용 예상

### API 사용 비용 (월 100개 쇼츠 기준)

| 서비스 | 사용량 | 예상 비용 |
|--------|--------|-----------|
| SerpAPI | ~200회 검색 | $50 (Starter 플랜) |
| OpenAI GPT-4 | ~100 요청 | $3-5 |
| DALL-E 3 | ~100 이미지 | $10-12 |
| ElevenLabs | ~20,000 글자 | $5 (Starter 플랜) |
| **합계** | | **$68-72/월** |

### 무료 플랜 활용

- **SerpAPI**: 월 100회까지 무료 (뉴스 + 유튜브 각 50회)
- **ElevenLabs**: 월 10,000 글자까지 무료 (약 50개 쇼츠)
- **OpenAI**: 신규 가입시 크레딧 제공

무료 플랜만 사용하면 월 50개 정도의 쇼츠를 무료로 생성할 수 있습니다!

## 🎨 스크린샷

### 메인 화면
3가지 생성 모드 버튼이 있는 깔끔한 다크 테마 UI

### 결과 화면
- 30초 스크립트 (복사 기능)
- 추천 제목 3개
- 썸네일 문구 5개 (그리드 형식)
- DALL-E 이미지 프롬프트
- 추가 기능 버튼들

## 🔧 커스터마이징

### 스크립트 톤 변경

`backend/server.js`의 `generateShortsScript` 함수에서 `systemPrompt` 수정:

```javascript
const systemPrompt = `
당신은 한국의 인기 유튜브 뉴스 쇼츠 채널의 메인 작가입니다.

**톤 변경 예시:**
- 진지한 뉴스 앵커 톤
- 친근한 유튜버 톤
- 전문가 해설자 톤
...
`;
```

### 뉴스 검색 키워드 변경

`backend/server.js`의 `fetchNewsWithSerp` 함수에서 검색어 수정:

```javascript
const url =
  `https://serpapi.com/search?` +
  `engine=google_news` +
  `&q=한국 뉴스 OR 속보 OR 논란` + // 여기 수정
  `&gl=kr` +
  `&hl=ko` +
  `&api_key=${serpKey}`;
```

### 영상 길이 변경

`systemPrompt`에서 글자 수 조정:

```javascript
// 30초 (250-350자) -> 60초 (500-700자)로 변경
- 30초 분량(약 250-350자)의 한국어 쇼츠 스크립트 작성
+ 60초 분량(약 500-700자)의 한국어 쇼츠 스크립트 작성
```

## 🐛 트러블슈팅

### 문제: SerpAPI 검색 결과가 없음

**해결책**:
```bash
# API 키 확인
curl "https://serpapi.com/search?engine=google&q=test&api_key=YOUR_KEY"

# 할당량 확인
https://serpapi.com/dashboard
```

### 문제: OpenAI API 오류

**해결책**:
- API 키 권한 확인
- GPT-4 접근 권한 확인
- 크레딧 잔액 확인

### 문제: CORS 오류

**해결책**:
프론트엔드와 백엔드를 같은 도메인에서 실행하거나, `backend/server.js`에서 CORS 설정 확인:

```javascript
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
```

### 문제: TTS 음성이 생성되지 않음

**해결책**:
- ElevenLabs API 키 확인
- Voice ID가 올바른지 확인
- 한국어 지원 음성인지 확인

## 🚀 고급 기능 (향후 계획)

### 1. 멀티 채널 관리
- CH001 ~ CH030 채널별 프리셋 저장
- 채널별 톤/스타일 설정
- 채널별 생성 기록 추적

### 2. YouTube 자동 업로드
- YouTube Data API 통합
- 생성된 영상 자동 업로드
- 제목/설명/태그 자동 설정

### 3. FFmpeg 비디오 합성
- 이미지 + 음성 자동 합성
- 자막 자동 생성 및 오버레이
- 배경 음악 추가

### 4. 분석 대시보드
- 생성된 콘텐츠 통계
- API 사용량 모니터링
- 비용 트래킹

### 5. 배치 생성
- 한 번에 여러 개 스크립트 생성
- 스케줄 기반 자동 생성
- 큐 시스템으로 순차 처리

## 📚 기술 스택

### 백엔드
- Node.js 18+
- Express.js
- OpenAI API (GPT-4, DALL-E 3)
- SerpAPI (뉴스/유튜브 검색)
- ElevenLabs API (TTS)

### 프론트엔드
- Vanilla JavaScript (프레임워크 없음)
- Modern CSS (Grid, Flexbox)
- Fetch API

### 개발 도구
- nodemon (개발 모드)
- dotenv (환경 변수)

## 🤝 기여

Pull Request를 환영합니다!

### 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

MIT License - 자유롭게 사용하세요!

## 📞 문의

이슈가 있으시면 GitHub Issues에 등록해주세요.

## 🙏 감사의 말

이 프로젝트는 다음 서비스들을 사용합니다:

- [SerpAPI](https://serpapi.com/) - 뉴스 및 유튜브 검색
- [OpenAI](https://openai.com/) - GPT-4 및 DALL-E 3
- [ElevenLabs](https://elevenlabs.io/) - TTS 음성 합성

## 📈 버전 히스토리

### v2.0.0 (2025-12-09)
- 🎉 웹 애플리케이션으로 완전 재작성
- ✨ SerpAPI 통합 (NewsAPI 대체)
- 🚀 3가지 생성 모드 추가
- 🎨 DALL-E 3 썸네일 생성 추가
- ⚡ 전체 자동화 기능 추가
- 💅 현대적인 다크 테마 UI

### v1.0.0 (2025-12-09)
- 초기 릴리스 (n8n 워크플로우)
- 기본 뉴스 검색 및 스크립트 생성

---

Made with ❤️ by NewsSearch Team
