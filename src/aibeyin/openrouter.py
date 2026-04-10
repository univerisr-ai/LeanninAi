import json
import os
import urllib.request
from typing import Dict, List

from .models import ConceptDraft, SourceItem
from .utils import safe_slug


class OpenRouterClient:
    def __init__(self, config: Dict) -> None:
        self.base_url = config.get("base_url", "https://openrouter.ai/api/v1/chat/completions")
        self.primary_model = config.get("primary_model", "qwen/qwen3-coder-480b-a35b:free")
        self.fallback_model = config.get("fallback_model", "stepfun/step-3.5-flash:free")
        self.max_tokens = int(config.get("max_tokens", 1200))
        self.temperature = float(config.get("temperature", 0.2))
        self.timeout_seconds = int(config.get("request_timeout_seconds", 45))
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

    def create_draft(
        self,
        source: SourceItem,
        existing_titles: List[str],
        dry_run: bool,
        memory_context: str = "",
    ) -> ConceptDraft:
        if dry_run:
            return self._fallback_draft(source, model_name="dry-run")
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is required for non-dry-run execution")

        prompt = self._build_prompt(source, existing_titles, memory_context)

        import time
        last_error = None
        for attempt in range(3):
            try:
                payload = self._request_model(self.primary_model, prompt)
                return self._parse_payload(payload, source, self.primary_model)
            except Exception as e:
                last_error = e
                if "429" in str(e):
                    time.sleep(4 * (attempt + 1))
                else:
                    time.sleep(2)
        
        # Fallback if primary fails 3 times
        try:
            payload = self._request_model(self.fallback_model, prompt)
            return self._parse_payload(payload, source, self.fallback_model)
        except Exception:
            return self._fallback_draft(source, model_name=self.fallback_model)

    def _request_model(self, model_name: str, prompt: str, system_prompt: str = None) -> str:
        if not system_prompt:
            system_prompt = (
                "You are an expert technical editor for a Turkish wiki. "
                "Return only valid JSON object with these fields: "
                "title, category, summary, key_points, links_to_existing, confidence, novelty."
            )
        request_body = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        data = json.dumps(request_body).encode("utf-8")
        request = urllib.request.Request(
            self.base_url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/universir-ai/LeanninAi",
                "X-Title": "AiBeyin",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            raw = response.read().decode("utf-8", errors="ignore")
        parsed = json.loads(raw)
        return parsed["choices"][0]["message"]["content"]

    def _build_prompt(self, source: SourceItem, existing_titles: List[str], memory_context: str) -> str:
        existing_joined = "\n".join(existing_titles[:50])
        memory_section = memory_context.strip() or "No persistent memory context provided."
        return (
            "Task: Create one wiki concept draft in Turkish.\n\n"
            "SCOPE (ONLY these topics are allowed):\n"
            "- Web Frontend: React, Vue, Svelte, Next.js, Nuxt, CSS, TypeScript, JavaScript, Vite, Webpack\n"
            "- Web Backend: Node.js, Express, Fastify, REST API, GraphQL, PostgreSQL, Redis, BullMQ\n"
            "- Web Security: XSS, CSRF, JWT, CORS, CSP, rate limiting, bot detection, OWASP\n"
            "- UI/UX Design: Gestalt, color theory, typography, micro-interactions, responsive design\n"
            "- Web Accessibility (a11y): WCAG, ARIA, keyboard navigation, screen readers\n"
            "- Web Performance: Core Web Vitals, PWA, Service Worker, lazy loading, code splitting\n\n"
            "FORBIDDEN topics (set category='off-topic' and novelty=0 if source is about these):\n"
            "- Blockchain, Solidity, Ethereum, Web3, DeFi, NFT\n"
            "- Flutter, Dart, Swift, Kotlin, Android/iOS native\n"
            "- .NET, C#, Blazor, MAUI, WPF\n"
            "- Go/Golang, Rust (unless web-related tooling)\n"
            "- Unity, Unreal Engine, game development\n"
            "- ML model training, PyTorch, TensorFlow\n"
            "- Career advice, soft skills, burnout, certification exams\n"
            "- Sports, entertainment, non-tech topics\n\n"
            "ANTI-REPEAT LEARNING (CRITICAL):\n"
            "The wiki below already covers many concepts in depth. "
            "You MUST check each existing concept carefully.\n"
            "- If this source just re-explains an ALREADY KNOWN concept "
            "(e.g. another article about React hooks when hooks are already covered), "
            "set novelty=0.\n"
            "- ONLY accept if the source teaches something GENUINELY NEW "
            "that is NOT covered by existing concepts.\n"
            "- A different article about the same topic is NOT new knowledge.\n"
            "- Ask yourself: 'Does this teach me a technique/pattern/concept "
            "I haven't seen in the existing list?' If NO, set novelty=0.\n\n"
            f"Source title: {source.title}\n"
            f"Source category: {source.category}\n"
            f"Source url: {source.url}\n"
            f"Source content:\n{source.content[:3500]}\n\n"
            "Persistent project memory (must be respected):\n"
            f"{memory_section}\n\n"
            "EXISTING CONCEPTS ALREADY IN WIKI (DO NOT REPEAT THESE):\n"
            f"{existing_joined}\n\n"
            "Rules:\n"
            "- If the source is about a FORBIDDEN topic, return category='off-topic' and novelty=0.\n"
            "- If the source covers a topic already in EXISTING CONCEPTS, set novelty below 30.\n"
            "- Only set novelty above 65 if the source teaches a genuinely NEW technique or pattern.\n"
            "- Keep summary practical and action-oriented, in Turkish.\n"
            "- links_to_existing must use [[Page-Name]] format when possible.\n"
            "- Return only valid JSON with fields: title, category, summary, key_points, links_to_existing, confidence, novelty."
        )

    def _parse_payload(self, content: str, source: SourceItem, model_name: str) -> ConceptDraft:
        if content is None:
            return self._fallback_draft(source, model_name=model_name)
            
        text = str(content).strip()
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end >= 0:
            text = text[start : end + 1]

        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return self._fallback_draft(source, model_name=model_name)

        title = str(payload.get("title") or source.title).strip()
        category = str(payload.get("category") or source.category).strip().lower()
        summary = str(payload.get("summary") or source.content[:260]).strip()
        key_points = payload.get("key_points") or []
        links = payload.get("links_to_existing") or []
        confidence = int(payload.get("confidence") or 0)
        novelty = int(payload.get("novelty") or 0)

        return ConceptDraft(
            slug=safe_slug(title),
            title=title,
            category=category,
            summary=summary,
            key_points=[str(x).strip() for x in key_points if str(x).strip()],
            links_to_existing=[str(x).strip() for x in links if str(x).strip()],
            confidence=max(0, min(confidence, 100)),
            novelty=max(0, min(novelty, 100)),
            model_used=model_name,
            source_url=source.url,
        )

    def _fallback_draft(self, source: SourceItem, model_name: str) -> ConceptDraft:
        summary = source.content[:300].strip()
        title = source.title.strip() or "Untitled Concept"
        return ConceptDraft(
            slug=safe_slug(title),
            title=title,
            category=source.category,
            summary=summary,
            key_points=[
                "Kaynak ozetinden cikarilan temel fikirler manuel gozden gecirilmeli.",
                "Bu draft, tekrar ogrenmeme filtresinden gecmistir.",
                "Publish oncesi teknik dogruluk kontrolu onerilir.",
            ],
            links_to_existing=[],
            confidence=75,
            novelty=70,
            model_used=model_name,
            source_url=source.url,
        )
