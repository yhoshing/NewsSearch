// ========================================
// 뉴스 쇼츠 자동 생성 백엔드 서버
// ========================================

import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import fetch from "node-fetch";
import OpenAI from "openai";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs/promises";
import { exec } from "child_process";
import { promisify } from "util";

const execPromise = promisify(exec);

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// 프론트엔드 정적 파일 제공
app.use(express.static(path.join(__dirname, "../frontend")));

// OpenAI 클라이언트 초기화
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// ─────────────────────────────────────────────────────────
// 1. SerpAPI로 뉴스 검색 (NewsAPI 대신)
// ─────────────────────────────────────────────────────────
async function fetchNewsWithSerp() {
  const serpKey = process.env.SERPAPI_KEY;
  if (!serpKey) {
    throw new Error("SERPAPI_KEY가 설정되지 않았습니다.");
  }

  // Google News 검색
  const url =
    `https://serpapi.com/search?` +
    `engine=google_news` +
    `&q=한국 뉴스 OR 속보 OR 논란` +
    `&gl=kr` +
    `&hl=ko` +
    `&api_key=${serpKey}`;

  const res = await fetch(url);
  const data = await res.json();

  if (!data.news_results || data.news_results.length === 0) {
    console.error("SerpAPI 뉴스 결과 없음:", data);
    return [];
  }

  // 상위 10개 뉴스 정리
  return data.news_results.slice(0, 10).map((article) => ({
    title: article.title || "",
    snippet: article.snippet || "",
    source: article.source?.name || "알 수 없음",
    link: article.link || "",
    date: article.date || "",
  }));
}

// ─────────────────────────────────────────────────────────
// 2. SerpAPI로 유튜브 급상승 뉴스 쇼츠 검색
// ─────────────────────────────────────────────────────────
async function fetchYoutubeTrendingWithSerp() {
  const serpKey = process.env.SERPAPI_KEY;
  if (!serpKey) {
    throw new Error("SERPAPI_KEY가 설정되지 않았습니다.");
  }

  // YouTube 검색 (뉴스 관련 쇼츠)
  const url =
    `https://serpapi.com/search?` +
    `engine=youtube` +
    `&search_query=속보 뉴스 쇼츠 OR 논란 OR 해킹 OR 이슈` +
    `&hl=ko` +
    `&gl=kr` +
    `&api_key=${serpKey}`;

  const res = await fetch(url);
  const data = await res.json();

  if (!data.video_results || data.video_results.length === 0) {
    console.error("SerpAPI 유튜브 결과 없음:", data);
    return [];
  }

  // 상위 10개 영상 정리
  return data.video_results.slice(0, 10).map((video) => ({
    title: video.title || "",
    link: video.link || "",
    channel: video.channel?.name || "알 수 없음",
    views: video.views || 0,
    publishedTime: video.published_time || "",
    length: video.length || "",
  }));
}

// ─────────────────────────────────────────────────────────
// 3. GPT-4로 30초 쇼츠 스크립트 + 제목 + 썸네일 생성
// ─────────────────────────────────────────────────────────
async function generateShortsScript({ newsList, youtubeList, mode }) {
  // 뉴스 데이터 포맷팅
  const newsText =
    newsList && newsList.length > 0
      ? newsList
          .slice(0, 5)
          .map(
            (n, i) =>
              `${i + 1}. [${n.source}] ${n.title}\n   ${n.snippet || ""}`
          )
          .join("\n\n")
      : "뉴스 데이터 없음";

  // 유튜브 데이터 포맷팅
  const youtubeText =
    youtubeList && youtubeList.length > 0
      ? youtubeList
          .slice(0, 5)
          .map(
            (v, i) =>
              `${i + 1}. (${v.views} 조회) ${v.title}\n   채널: ${v.channel}`
          )
          .join("\n\n")
      : "유튜브 데이터 없음";

  const systemPrompt = `
당신은 한국의 인기 유튜브 뉴스 쇼츠 채널의 메인 작가입니다.

**핵심 역량:**
- 30초 분량(약 250-350자)의 한국어 쇼츠 스크립트 작성
- 시사 유튜버와 라디오 뉴스의 중간 톤
- 구어체 사용하되 과도한 자극적 표현은 자제
- 첫 3초 안에 시청자의 관심을 끄는 후킹 필수

**출력 형식:**
반드시 아래 형식을 정확히 지켜주세요:

[SCRIPT]
(30초 분량의 스크립트)

[TITLES]
1. (제목1)
2. (제목2)
3. (제목3)

[THUMBNAILS]
1. (4-10글자 썸네일 문구)
2. (4-10글자 썸네일 문구)
3. (4-10글자 썸네일 문구)
4. (4-10글자 썸네일 문구)
5. (4-10글자 썸네일 문구)

[IMAGE_PROMPT]
(DALL-E 3로 썸네일 이미지를 생성하기 위한 영어 프롬프트)
`;

  const userPrompt = `
**생성 모드: ${mode}**

📰 **오늘의 주요 뉴스 (상위 5개)**
${newsText}

🎬 **유튜브에서 조회수가 높은 뉴스 쇼츠 (상위 5개)**
${youtubeText}

---

위 정보를 바탕으로 다음을 생성해주세요:

1. **30초 쇼츠 스크립트** (구어체, 자연스럽게)
   - 0-3초: 강렬한 후킹 (예: "여러분, 방금 이런 일이 벌어졌습니다")
   - 3-25초: 핵심 내용 전달 (가장 중요한 정보만)
   - 25-30초: 시청자 참여 유도 질문 (예: "여러분은 어떻게 생각하시나요?")

2. **영상 제목 3개**
   - 클릭을 유도하는 제목
   - 40자 이내
   - 이모지 사용 가능

3. **썸네일 문구 5개**
   - 각각 4-10글자
   - 강렬한 키워드 위주
   - 대문자 사용 권장

4. **DALL-E 3 이미지 프롬프트**
   - 영어로 작성
   - 뉴스 주제를 시각적으로 표현
   - "dramatic news thumbnail style, bold text overlay, high contrast" 스타일 포함
`;

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
      temperature: 0.8,
      max_tokens: 2000,
    });

    const rawText = completion.choices[0].message.content || "";

    // 파싱
    const parsed = parseGPTResponse(rawText);

    // 뉴스 출처 정보 추가
    const sources = newsList && newsList.length > 0
      ? newsList.slice(0, 5).map(n => ({
          title: n.title,
          source: n.source,
          link: n.link,
          date: n.date
        }))
      : [];

    return {
      success: true,
      mode,
      script: parsed.script,
      titles: parsed.titles,
      thumbnails: parsed.thumbnails,
      imagePrompt: parsed.imagePrompt,
      sources: sources,
      raw: rawText,
    };
  } catch (error) {
    console.error("GPT 생성 오류:", error);
    throw new Error(`GPT 생성 실패: ${error.message}`);
  }
}

// ─────────────────────────────────────────────────────────
// 4. GPT 응답 파싱
// ─────────────────────────────────────────────────────────
function parseGPTResponse(text) {
  const result = {
    script: "",
    titles: [],
    thumbnails: [],
    imagePrompt: "",
  };

  // [SCRIPT] 섹션 추출
  const scriptMatch = text.match(/\[SCRIPT\]([\s\S]*?)(?=\[TITLES\]|$)/i);
  if (scriptMatch) {
    result.script = scriptMatch[1].trim();
  }

  // [TITLES] 섹션 추출
  const titlesMatch = text.match(/\[TITLES\]([\s\S]*?)(?=\[THUMBNAILS\]|$)/i);
  if (titlesMatch) {
    const lines = titlesMatch[1].split("\n").filter((l) => l.trim());
    result.titles = lines
      .map((l) => l.replace(/^\d+\.\s*/, "").trim())
      .filter((l) => l);
  }

  // [THUMBNAILS] 섹션 추출
  const thumbnailsMatch = text.match(
    /\[THUMBNAILS\]([\s\S]*?)(?=\[IMAGE_PROMPT\]|$)/i
  );
  if (thumbnailsMatch) {
    const lines = thumbnailsMatch[1].split("\n").filter((l) => l.trim());
    result.thumbnails = lines
      .map((l) => l.replace(/^\d+\.\s*/, "").trim())
      .filter((l) => l);
  }

  // [IMAGE_PROMPT] 섹션 추출
  const imagePromptMatch = text.match(/\[IMAGE_PROMPT\]([\s\S]*?)$/i);
  if (imagePromptMatch) {
    result.imagePrompt = imagePromptMatch[1].trim();
  }

  return result;
}

// ─────────────────────────────────────────────────────────
// 5. ElevenLabs TTS로 음성 생성
// ─────────────────────────────────────────────────────────
async function generateVoiceWithElevenLabs(script) {
  const apiKey = process.env.ELEVENLABS_API_KEY;
  const voiceId = process.env.ELEVENLABS_VOICE_ID;

  if (!apiKey || !voiceId) {
    throw new Error("ElevenLabs API 키 또는 Voice ID가 설정되지 않았습니다.");
  }

  const url = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`;

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": apiKey,
    },
    body: JSON.stringify({
      text: script,
      model_id: "eleven_multilingual_v2",
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.75,
      },
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`ElevenLabs API 오류: ${error}`);
  }

  const audioBuffer = await response.arrayBuffer();
  const timestamp = Date.now();
  const filename = `voice_${timestamp}.mp3`;
  const filepath = path.join(__dirname, "../output", filename);

  // 출력 디렉토리 확인
  await fs.mkdir(path.join(__dirname, "../output"), { recursive: true });

  // 파일 저장
  await fs.writeFile(filepath, Buffer.from(audioBuffer));

  return {
    success: true,
    filename,
    filepath,
    size: audioBuffer.byteLength,
  };
}

// ─────────────────────────────────────────────────────────
// 6. DALL-E 3로 썸네일 이미지 생성
// ─────────────────────────────────────────────────────────
async function generateThumbnailWithDALLE(prompt) {
  try {
    const response = await openai.images.generate({
      model: "dall-e-3",
      prompt: prompt,
      size: "1024x1024",
      quality: "standard",
      n: 1,
    });

    const imageUrl = response.data[0].url;

    // 이미지 다운로드
    const imageResponse = await fetch(imageUrl);
    const imageBuffer = await imageResponse.arrayBuffer();

    const timestamp = Date.now();
    const filename = `thumbnail_${timestamp}.png`;
    const filepath = path.join(__dirname, "../output", filename);

    // 출력 디렉토리 확인
    await fs.mkdir(path.join(__dirname, "../output"), { recursive: true });

    // 파일 저장
    await fs.writeFile(filepath, Buffer.from(imageBuffer));

    return {
      success: true,
      filename,
      filepath,
      url: imageUrl,
      size: imageBuffer.byteLength,
    };
  } catch (error) {
    console.error("DALL-E 생성 오류:", error);
    throw new Error(`DALL-E 생성 실패: ${error.message}`);
  }
}

// ─────────────────────────────────────────────────────────
// 7. FFmpeg로 비디오 합성 (이미지 + 음성 → MP4)
// ─────────────────────────────────────────────────────────
async function createVideoWithFFmpeg(imagePath, audioPath) {
  try {
    const timestamp = Date.now();
    const outputFilename = `shorts_${timestamp}.mp4`;
    const outputPath = path.join(__dirname, "../output", outputFilename);

    // 출력 디렉토리 확인
    await fs.mkdir(path.join(__dirname, "../output"), { recursive: true });

    // FFmpeg 명령어
    // -loop 1: 이미지 반복
    // -i image: 입력 이미지
    // -i audio: 입력 오디오
    // -c:v libx264: H.264 비디오 코덱
    // -tune stillimage: 정지 이미지 최적화
    // -c:a aac: AAC 오디오 코덱
    // -b:a 192k: 오디오 비트레이트
    // -pix_fmt yuv420p: 호환성을 위한 픽셀 포맷
    // -shortest: 가장 짧은 스트림에 맞춤 (오디오 길이)
    // -vf scale: 1080x1920 세로 영상 (쇼츠용)
    const ffmpegCommand = `ffmpeg -loop 1 -i "${imagePath}" -i "${audioPath}" \
      -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p \
      -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" \
      -shortest -t 60 -y "${outputPath}"`;

    console.log("🎬 FFmpeg 비디오 합성 시작...");
    console.log(`명령어: ${ffmpegCommand}`);

    // FFmpeg 실행
    const { stdout, stderr } = await execPromise(ffmpegCommand);

    if (stderr && !stderr.includes('frame=')) {
      console.log("FFmpeg stderr:", stderr);
    }

    // 파일 크기 확인
    const stats = await fs.stat(outputPath);

    console.log("✅ FFmpeg 비디오 합성 완료");

    return {
      success: true,
      filename: outputFilename,
      filepath: outputPath,
      size: stats.size,
    };
  } catch (error) {
    console.error("❌ FFmpeg 비디오 합성 오류:", error);
    throw new Error(`비디오 합성 실패: ${error.message}`);
  }
}

// ═════════════════════════════════════════════════════════
// API 라우트
// ═════════════════════════════════════════════════════════

// 헬스체크
app.get("/api/health", (req, res) => {
  res.json({
    status: "ok",
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
});

// ─────────────────────────────────────────────────────────
// 라우트 1: 오늘 뉴스 기반 스크립트 생성
// ─────────────────────────────────────────────────────────
app.post("/api/generate/news", async (req, res) => {
  try {
    console.log("📰 뉴스 기반 스크립트 생성 시작...");

    const newsList = await fetchNewsWithSerp();
    const result = await generateShortsScript({
      newsList,
      youtubeList: [],
      mode: "오늘 뉴스 기반",
    });

    console.log("✅ 뉴스 기반 스크립트 생성 완료");
    res.json(result);
  } catch (error) {
    console.error("❌ 뉴스 기반 생성 오류:", error);
    res.status(500).json({
      success: false,
      error: "생성 실패",
      detail: error.message,
    });
  }
});

// ─────────────────────────────────────────────────────────
// 라우트 2: 유튜브 급상승 기반 스크립트 생성
// ─────────────────────────────────────────────────────────
app.post("/api/generate/youtube", async (req, res) => {
  try {
    console.log("🎬 유튜브 급상승 기반 스크립트 생성 시작...");

    const youtubeList = await fetchYoutubeTrendingWithSerp();
    const result = await generateShortsScript({
      newsList: [],
      youtubeList,
      mode: "유튜브 급상승 기반",
    });

    console.log("✅ 유튜브 급상승 기반 스크립트 생성 완료");
    res.json(result);
  } catch (error) {
    console.error("❌ 유튜브 급상승 생성 오류:", error);
    res.status(500).json({
      success: false,
      error: "생성 실패",
      detail: error.message,
    });
  }
});

// ─────────────────────────────────────────────────────────
// 라우트 3: 뉴스 + 유튜브 결합 스크립트 생성
// ─────────────────────────────────────────────────────────
app.post("/api/generate/mixed", async (req, res) => {
  try {
    console.log("🔥 뉴스 + 유튜브 결합 스크립트 생성 시작...");

    const [newsList, youtubeList] = await Promise.all([
      fetchNewsWithSerp(),
      fetchYoutubeTrendingWithSerp(),
    ]);

    const result = await generateShortsScript({
      newsList,
      youtubeList,
      mode: "뉴스 + 유튜브 급상승 결합",
    });

    console.log("✅ 결합 스크립트 생성 완료");
    res.json(result);
  } catch (error) {
    console.error("❌ 결합 생성 오류:", error);
    res.status(500).json({
      success: false,
      error: "생성 실패",
      detail: error.message,
    });
  }
});

// ─────────────────────────────────────────────────────────
// 라우트 4: TTS 음성 생성
// ─────────────────────────────────────────────────────────
app.post("/api/generate/voice", async (req, res) => {
  try {
    const { script } = req.body;

    if (!script) {
      return res.status(400).json({
        success: false,
        error: "스크립트가 필요합니다.",
      });
    }

    console.log("🎙️ TTS 음성 생성 시작...");
    const result = await generateVoiceWithElevenLabs(script);

    console.log("✅ TTS 음성 생성 완료");
    res.json(result);
  } catch (error) {
    console.error("❌ TTS 생성 오류:", error);
    res.status(500).json({
      success: false,
      error: "TTS 생성 실패",
      detail: error.message,
    });
  }
});

// ─────────────────────────────────────────────────────────
// 라우트 5: DALL-E 3 썸네일 생성
// ─────────────────────────────────────────────────────────
app.post("/api/generate/thumbnail", async (req, res) => {
  try {
    const { prompt } = req.body;

    if (!prompt) {
      return res.status(400).json({
        success: false,
        error: "이미지 프롬프트가 필요합니다.",
      });
    }

    console.log("🎨 DALL-E 3 썸네일 생성 시작...");
    const result = await generateThumbnailWithDALLE(prompt);

    console.log("✅ 썸네일 생성 완료");
    res.json(result);
  } catch (error) {
    console.error("❌ 썸네일 생성 오류:", error);
    res.status(500).json({
      success: false,
      error: "썸네일 생성 실패",
      detail: error.message,
    });
  }
});

// ─────────────────────────────────────────────────────────
// 라우트 6: 전체 자동화 (스크립트 + 음성 + 썸네일)
// ─────────────────────────────────────────────────────────
app.post("/api/generate/complete", async (req, res) => {
  try {
    const { mode } = req.body;

    console.log(`🚀 전체 자동화 시작 (모드: ${mode})...`);

    // 1단계: 스크립트 생성
    let scriptResult;
    if (mode === "news") {
      const newsList = await fetchNewsWithSerp();
      scriptResult = await generateShortsScript({
        newsList,
        youtubeList: [],
        mode: "오늘 뉴스 기반",
      });
    } else if (mode === "youtube") {
      const youtubeList = await fetchYoutubeTrendingWithSerp();
      scriptResult = await generateShortsScript({
        newsList: [],
        youtubeList,
        mode: "유튜브 급상승 기반",
      });
    } else if (mode === "mixed") {
      const [newsList, youtubeList] = await Promise.all([
        fetchNewsWithSerp(),
        fetchYoutubeTrendingWithSerp(),
      ]);
      scriptResult = await generateShortsScript({
        newsList,
        youtubeList,
        mode: "뉴스 + 유튜브 급상승 결합",
      });
    }

    // 2단계: TTS 음성 생성
    console.log("🎙️ 음성 생성 중...");
    const voiceResult = await generateVoiceWithElevenLabs(scriptResult.script);

    // 3단계: 썸네일 생성
    console.log("🎨 썸네일 생성 중...");
    const thumbnailResult = await generateThumbnailWithDALLE(
      scriptResult.imagePrompt
    );

    // 4단계: 비디오 합성
    console.log("🎬 비디오 합성 중...");
    const videoResult = await createVideoWithFFmpeg(
      thumbnailResult.filepath,
      voiceResult.filepath
    );

    console.log("✅ 전체 자동화 완료! (스크립트 + 음성 + 이미지 + 비디오)");

    res.json({
      success: true,
      script: scriptResult,
      voice: voiceResult,
      thumbnail: thumbnailResult,
      video: videoResult,
    });
  } catch (error) {
    console.error("❌ 전체 자동화 오류:", error);
    res.status(500).json({
      success: false,
      error: "전체 자동화 실패",
      detail: error.message,
    });
  }
});

// ─────────────────────────────────────────────────────────
// 정적 파일 다운로드 (생성된 음성/이미지)
// ─────────────────────────────────────────────────────────
app.use("/output", express.static(path.join(__dirname, "../output")));

// ═════════════════════════════════════════════════════════
// 서버 시작
// ═════════════════════════════════════════════════════════
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   🎬 뉴스 쇼츠 자동 생성 서버                         ║
║                                                       ║
║   서버 주소: http://localhost:${PORT}                    ║
║   API 문서: http://localhost:${PORT}/api/health         ║
║                                                       ║
║   준비 완료! 프론트엔드에서 접속하세요.               ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
  `);
});
