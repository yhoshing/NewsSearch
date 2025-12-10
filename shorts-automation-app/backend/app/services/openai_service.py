"""
OpenAI API 서비스
"""
import os
import json
from typing import List, Dict, Any
from openai import OpenAI


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")

    def generate_ideas(
        self,
        topic: str,
        target_audience: str = None,
        content_style: str = None,
        num_ideas: int = 5
    ) -> List[Dict[str, Any]]:
        """
        채널 주제를 기반으로 쇼츠 아이디어 생성
        """
        prompt = f"""당신은 크리에이티브한 쇼츠 영상 아이디어 생성자입니다.

채널 주제: {topic}
"""

        if target_audience:
            prompt += f"타겟 청중: {target_audience}\n"

        if content_style:
            prompt += f"콘텐츠 스타일: {content_style}\n"

        prompt += f"""
요구사항:
1. 시청자의 관심을 끄는 강렬한 주제
2. 30-60초 분량의 짧은 영상에 적합
3. 바이럴 가능성이 높은 콘텐츠
4. 명확한 메시지 전달

{num_ideas}개의 아이디어를 다음 JSON 형식으로 생성해주세요:
[
  {{
    "title": "제목",
    "hook": "강렬한 오프닝 문구 (3-5초 분량)",
    "content": "핵심 내용 요약",
    "cta": "행동 유도 문구",
    "keywords": ["키워드1", "키워드2", "키워드3"]
  }}
]

JSON만 출력해주세요."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a creative content generator. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )

            content = response.choices[0].message.content.strip()

            # JSON 추출
            json_match = content
            if "```json" in content:
                json_match = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_match = content.split("```")[1].split("```")[0].strip()

            ideas = json.loads(json_match)
            return ideas

        except Exception as e:
            print(f"Error generating ideas: {e}")
            return []

    def generate_script(
        self,
        title: str,
        hook: str,
        content: str,
        cta: str,
        duration: int = 60
    ) -> Dict[str, Any]:
        """
        아이디어를 쇼츠 스크립트로 변환
        """
        prompt = f"""선택된 아이디어를 쇼츠 영상 스크립트로 변환해주세요.

제목: {title}
오프닝: {hook}
내용: {content}
CTA: {cta}

요구사항:
1. {duration}초 분량
2. 구어체로 자연스럽게
3. 시청자와의 공감대 형성
4. 명확한 타임라인:
   - 0-5초: 강렬한 훅
   - 5-{duration-10}초: 핵심 메시지
   - {duration-10}-{duration}초: CTA 및 마무리

다음 JSON 형식으로 출력:
{{
  "script": "전체 스크립트 (자연스럽게 읽을 수 있는 형태)",
  "segments": [
    {{"time": "0-5", "text": "훅 문구"}},
    {{"time": "5-{duration-10}", "text": "핵심 내용"}},
    {{"time": "{duration-10}-{duration}", "text": "마무리"}}
  ],
  "visualSuggestions": ["이미지1 설명", "이미지2 설명"]
}}

JSON만 출력해주세요."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional script writer. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            content = response.choices[0].message.content.strip()

            # JSON 추출
            json_match = content
            if "```json" in content:
                json_match = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_match = content.split("```")[1].split("```")[0].strip()

            script_data = json.loads(json_match)
            return script_data

        except Exception as e:
            print(f"Error generating script: {e}")
            return {
                "script": f"{hook} {content} {cta}",
                "segments": [
                    {"time": "0-60", "text": f"{hook} {content} {cta}"}
                ],
                "visualSuggestions": []
            }
