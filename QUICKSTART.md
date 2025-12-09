# 🚀 빠른 시작 가이드

5분 안에 뉴스 쇼츠 생성기를 실행해보세요!

## 1단계: API 키 발급 (5분)

### SerpAPI (필수) - 뉴스 + 유튜브 검색
1. https://serpapi.com/ 접속
2. 회원가입 (Google 로그인 가능)
3. Dashboard에서 API Key 복사
4. **무료 플랜**: 월 100회 검색 가능

### OpenAI (필수) - GPT-4 + DALL-E 3
1. https://platform.openai.com/ 접속
2. 회원가입 및 로그인
3. API Keys 메뉴에서 새 키 생성
4. **비용**: 사용량 기반 (쇼츠 1개당 약 $0.20)

### ElevenLabs (선택) - TTS 음성
1. https://elevenlabs.io/ 접속
2. 회원가입
3. Profile → API Keys에서 키 생성
4. Voices 메뉴에서 Voice ID 확인 (한국어 지원 음성)
5. **무료 플랜**: 월 10,000 글자

## 2단계: FFmpeg 설치 (선택 - 비디오 생성시 필요)

완전 자동 쇼츠 생성 기능을 사용하려면 FFmpeg가 필요합니다:

**Windows:**
```bash
# Chocolatey로 설치 (권장)
choco install ffmpeg

# 또는 https://ffmpeg.org/download.html 에서 다운로드
```

**Mac:**
```bash
brew install ffmpeg
```

**확인:**
```bash
ffmpeg -version
```

## 3단계: 설치 및 환경 설정 (2분)

```bash
# 백엔드 디렉토리로 이동
cd backend

# Node.js 패키지 설치
npm install

# 환경 변수 파일 생성
cp .env.example .env
```

## 4단계: API 키 입력 (1분)

`backend/.env` 파일을 열고 API 키를 입력하세요:

```env
PORT=3000

# SerpAPI (필수)
SERPAPI_KEY=your_actual_serpapi_key_here

# OpenAI (필수)
OPENAI_API_KEY=sk-your_actual_openai_key_here

# ElevenLabs (TTS 사용시)
ELEVENLABS_API_KEY=your_actual_elevenlabs_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here
```

## 5단계: 서버 실행 (1분)

```bash
# 백엔드 디렉토리에서
npm start
```

서버가 시작되면 이런 메시지가 보입니다:

```
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   🎬 뉴스 쇼츠 자동 생성 서버                         ║
║                                                       ║
║   서버 주소: http://localhost:3000                    ║
║   API 문서: http://localhost:3000/api/health         ║
║                                                       ║
║   준비 완료! 프론트엔드에서 접속하세요.               ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

## 5단계: 웹 브라우저에서 접속

```
http://localhost:3000
```

브라우저에서 열면 3개의 큰 버튼이 보입니다:

- 📰 **오늘 뉴스 기반**
- 🎬 **유튜브 급상승 기반**
- 🔥 **뉴스 + 급상승 결합**

아무 버튼이나 클릭하면 자동으로 스크립트가 생성됩니다!

## 🎉 완료!

이제 30초 쇼츠 스크립트, 제목 3개, 썸네일 문구 5개가 자동으로 생성됩니다.

## 💡 추가 기능 테스트

생성된 스크립트 아래에서:

1. **🎙️ 음성 생성** 버튼 → TTS 음성 파일 생성
2. **🎨 썸네일 생성** 버튼 → DALL-E 이미지 생성
3. **⚡ 전체 자동 생성** 버튼 → 스크립트 + 음성 + 이미지 한 번에

## 🐛 문제 해결

### "SERPAPI_KEY가 설정되지 않았습니다" 오류
→ `.env` 파일에 API 키가 올바르게 입력되었는지 확인
→ 서버 재시작 (Ctrl+C 후 `npm start`)

### "포트 3000이 이미 사용 중입니다" 오류
```bash
# .env 파일에서 PORT 변경
PORT=3001
```

### "Cannot GET /" 오류
→ 서버가 제대로 시작되었는지 확인
→ 터미널에서 오류 메시지 확인

### API 응답이 느림
→ SerpAPI와 OpenAI 서버 응답 시간 때문입니다 (30초~1분 정도 소요)
→ 로딩 스피너가 표시되는 것이 정상입니다

## 🔧 개발 모드 (자동 재시작)

코드를 수정하면서 테스트하려면:

```bash
npm run dev
```

파일이 수정될 때마다 서버가 자동으로 재시작됩니다.

## 📝 다음 단계

웹이 잘 작동하면:

1. 스크립트 톤 커스터마이징
2. 뉴스 검색 키워드 변경
3. 영상 길이 조정 (30초 → 60초)
4. 멀티 채널 기능 추가
5. FFmpeg 비디오 합성 기능

필요한 기능이 있으면 말씀해주세요!
