// ========================================
// 뉴스 쇼츠 자동 생성기 - 프론트엔드 로직
// ========================================

const API_BASE_URL = "http://localhost:3000/api";

// 전역 상태
let currentResult = null;
let currentMode = null;

// ========================================
// DOM 요소
// ========================================
const elements = {
  btnNews: document.getElementById("btnNews"),
  btnYoutube: document.getElementById("btnYoutube"),
  btnMixed: document.getElementById("btnMixed"),
  btnGenerateVoice: document.getElementById("btnGenerateVoice"),
  btnGenerateThumbnail: document.getElementById("btnGenerateThumbnail"),
  btnGenerateComplete: document.getElementById("btnGenerateComplete"),
  btnDownloadResults: document.getElementById("btnDownloadResults"),
  btnReset: document.getElementById("btnReset"),
  btnRetry: document.getElementById("btnRetry"),

  statusSection: document.getElementById("statusSection"),
  statusText: document.getElementById("statusText"),
  resultSection: document.getElementById("resultSection"),
  errorSection: document.getElementById("errorSection"),
  errorText: document.getElementById("errorText"),

  scriptContent: document.getElementById("scriptContent"),
  scriptLength: document.getElementById("scriptLength"),
  titlesContent: document.getElementById("titlesContent"),
  thumbnailsContent: document.getElementById("thumbnailsContent"),
  imagePromptContent: document.getElementById("imagePromptContent"),
  generatedFilesBox: document.getElementById("generatedFilesBox"),
  generatedFilesContent: document.getElementById("generatedFilesContent"),

  toast: document.getElementById("toast"),
};

// ========================================
// 유틸리티 함수
// ========================================

function showToast(message, isError = false) {
  elements.toast.textContent = message;
  elements.toast.classList.add("show");
  if (isError) {
    elements.toast.classList.add("error");
  } else {
    elements.toast.classList.remove("error");
  }

  setTimeout(() => {
    elements.toast.classList.remove("show");
  }, 3000);
}

function showLoading(message = "생성 중입니다...") {
  elements.statusText.textContent = message;
  elements.statusSection.style.display = "block";
  elements.resultSection.style.display = "none";
  elements.errorSection.style.display = "none";

  // 모든 버튼 비활성화
  disableAllButtons();
}

function hideLoading() {
  elements.statusSection.style.display = "none";

  // 모든 버튼 활성화
  enableAllButtons();
}

function showResult() {
  hideLoading();
  elements.resultSection.style.display = "block";
  elements.errorSection.style.display = "none";
}

function showError(message) {
  hideLoading();
  elements.errorSection.style.display = "block";
  elements.errorText.textContent = message;
  elements.resultSection.style.display = "none";
}

function disableAllButtons() {
  document.querySelectorAll("button").forEach((btn) => {
    btn.disabled = true;
  });
}

function enableAllButtons() {
  document.querySelectorAll("button").forEach((btn) => {
    btn.disabled = false;
  });
}

// ========================================
// API 호출 함수
// ========================================

async function callAPI(endpoint, method = "POST", body = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  const data = await response.json();

  if (!response.ok || !data.success) {
    throw new Error(data.detail || data.error || "API 호출 실패");
  }

  return data;
}

// ========================================
// 스크립트 생성
// ========================================

async function generateScript(mode) {
  try {
    currentMode = mode;

    let endpoint;
    let loadingMessage;

    if (mode === "news") {
      endpoint = "/generate/news";
      loadingMessage = "📰 최신 뉴스를 분석하여 스크립트 생성 중...";
    } else if (mode === "youtube") {
      endpoint = "/generate/youtube";
      loadingMessage = "🎬 유튜브 급상승 영상을 분석하여 스크립트 생성 중...";
    } else if (mode === "mixed") {
      endpoint = "/generate/mixed";
      loadingMessage = "🔥 뉴스와 트렌드를 결합하여 스크립트 생성 중...";
    }

    showLoading(loadingMessage);

    const result = await callAPI(endpoint);

    currentResult = result;
    displayResult(result);
    showResult();
    showToast("✅ 스크립트 생성 완료!");
  } catch (error) {
    console.error("스크립트 생성 오류:", error);
    showError(`스크립트 생성 실패: ${error.message}`);
    showToast(`❌ 생성 실패: ${error.message}`, true);
  }
}

// ========================================
// 결과 표시
// ========================================

function displayResult(result) {
  // 스크립트
  elements.scriptContent.textContent = result.script || "스크립트 없음";
  elements.scriptLength.textContent = `글자 수: ${
    (result.script || "").length
  }자`;

  // 제목
  if (result.titles && result.titles.length > 0) {
    elements.titlesContent.innerHTML =
      "<ul>" +
      result.titles.map((title) => `<li>${title}</li>`).join("") +
      "</ul>";
  } else {
    elements.titlesContent.textContent = "제목 없음";
  }

  // 썸네일 문구
  if (result.thumbnails && result.thumbnails.length > 0) {
    elements.thumbnailsContent.innerHTML = result.thumbnails
      .map((text) => `<div class="thumbnail-item">${text}</div>`)
      .join("");
  } else {
    elements.thumbnailsContent.textContent = "썸네일 문구 없음";
  }

  // 이미지 프롬프트
  elements.imagePromptContent.textContent =
    result.imagePrompt || "이미지 프롬프트 없음";
}

// ========================================
// TTS 음성 생성
// ========================================

async function generateVoice() {
  if (!currentResult || !currentResult.script) {
    showToast("❌ 먼저 스크립트를 생성해주세요", true);
    return;
  }

  try {
    showLoading("🎙️ TTS 음성 생성 중...");

    const result = await callAPI("/generate/voice", "POST", {
      script: currentResult.script,
    });

    hideLoading();
    showToast("✅ 음성 생성 완료!");

    // 생성된 파일 표시
    addGeneratedFile({
      type: "audio",
      filename: result.filename,
      filepath: result.filepath,
      size: result.size,
    });
  } catch (error) {
    console.error("음성 생성 오류:", error);
    showError(`음성 생성 실패: ${error.message}`);
    showToast(`❌ 음성 생성 실패: ${error.message}`, true);
  }
}

// ========================================
// DALL-E 썸네일 생성
// ========================================

async function generateThumbnail() {
  if (!currentResult || !currentResult.imagePrompt) {
    showToast("❌ 먼저 스크립트를 생성해주세요", true);
    return;
  }

  try {
    showLoading("🎨 DALL-E 3로 썸네일 이미지 생성 중...");

    const result = await callAPI("/generate/thumbnail", "POST", {
      prompt: currentResult.imagePrompt,
    });

    hideLoading();
    showToast("✅ 썸네일 생성 완료!");

    // 생성된 파일 표시
    addGeneratedFile({
      type: "image",
      filename: result.filename,
      filepath: result.filepath,
      url: result.url,
      size: result.size,
    });
  } catch (error) {
    console.error("썸네일 생성 오류:", error);
    showError(`썸네일 생성 실패: ${error.message}`);
    showToast(`❌ 썸네일 생성 실패: ${error.message}`, true);
  }
}

// ========================================
// 전체 자동 생성
// ========================================

async function generateComplete() {
  if (!currentMode) {
    showToast("❌ 먼저 스크립트를 생성해주세요", true);
    return;
  }

  try {
    showLoading("⚡ 전체 자동 생성 중 (스크립트 + 음성 + 썸네일)...");

    const result = await callAPI("/generate/complete", "POST", {
      mode: currentMode,
    });

    // 결과 표시
    currentResult = result.script;
    displayResult(result.script);

    // 생성된 파일들 표시
    if (result.voice) {
      addGeneratedFile({
        type: "audio",
        filename: result.voice.filename,
        filepath: result.voice.filepath,
        size: result.voice.size,
      });
    }

    if (result.thumbnail) {
      addGeneratedFile({
        type: "image",
        filename: result.thumbnail.filename,
        filepath: result.thumbnail.filepath,
        url: result.thumbnail.url,
        size: result.thumbnail.size,
      });
    }

    showResult();
    showToast("✅ 전체 자동 생성 완료!");
  } catch (error) {
    console.error("전체 자동 생성 오류:", error);
    showError(`전체 자동 생성 실패: ${error.message}`);
    showToast(`❌ 생성 실패: ${error.message}`, true);
  }
}

// ========================================
// 생성된 파일 추가
// ========================================

function addGeneratedFile(file) {
  elements.generatedFilesBox.style.display = "block";

  const fileItem = document.createElement("div");
  fileItem.className = "file-item";

  const sizeInKB = (file.size / 1024).toFixed(2);

  fileItem.innerHTML = `
    <div class="file-info">
      <span class="file-name">${file.type === "audio" ? "🎙️" : "🖼️"} ${
    file.filename
  }</span>
      <span class="file-size">${sizeInKB} KB</span>
    </div>
    <a href="/output/${file.filename}" class="btn-download" download>다운로드</a>
  `;

  elements.generatedFilesContent.appendChild(fileItem);
}

// ========================================
// 결과 다운로드 (JSON)
// ========================================

function downloadResults() {
  if (!currentResult) {
    showToast("❌ 다운로드할 결과가 없습니다", true);
    return;
  }

  const dataStr = JSON.stringify(currentResult, null, 2);
  const blob = new Blob([dataStr], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `shorts-script-${Date.now()}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  showToast("✅ 결과 다운로드 완료!");
}

// ========================================
// 복사 기능
// ========================================

function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      showToast("✅ 클립보드에 복사되었습니다!");
    })
    .catch((err) => {
      console.error("복사 실패:", err);
      showToast("❌ 복사 실패", true);
    });
}

// ========================================
// 초기화
// ========================================

function reset() {
  currentResult = null;
  currentMode = null;
  elements.resultSection.style.display = "none";
  elements.errorSection.style.display = "none";
  elements.statusSection.style.display = "none";
  elements.generatedFilesBox.style.display = "none";
  elements.generatedFilesContent.innerHTML = "";
  showToast("🔄 초기화 완료");
}

// ========================================
// 이벤트 리스너
// ========================================

// 스크립트 생성 버튼
elements.btnNews.addEventListener("click", () => generateScript("news"));
elements.btnYoutube.addEventListener("click", () => generateScript("youtube"));
elements.btnMixed.addEventListener("click", () => generateScript("mixed"));

// 추가 기능 버튼
elements.btnGenerateVoice.addEventListener("click", generateVoice);
elements.btnGenerateThumbnail.addEventListener("click", generateThumbnail);
elements.btnGenerateComplete.addEventListener("click", generateComplete);
elements.btnDownloadResults.addEventListener("click", downloadResults);
elements.btnReset.addEventListener("click", reset);
elements.btnRetry.addEventListener("click", () => {
  if (currentMode) {
    generateScript(currentMode);
  }
});

// 복사 버튼
document.querySelectorAll(".btn-copy").forEach((btn) => {
  btn.addEventListener("click", () => {
    const copyType = btn.getAttribute("data-copy");

    let text = "";
    if (copyType === "script") {
      text = elements.scriptContent.textContent;
    } else if (copyType === "titles") {
      text = currentResult.titles.join("\n");
    } else if (copyType === "thumbnails") {
      text = currentResult.thumbnails.join("\n");
    } else if (copyType === "imagePrompt") {
      text = elements.imagePromptContent.textContent;
    }

    copyToClipboard(text);
  });
});

// ========================================
// 초기화
// ========================================

console.log("🎬 뉴스 쇼츠 자동 생성기 준비 완료!");
console.log("API 서버:", API_BASE_URL);
