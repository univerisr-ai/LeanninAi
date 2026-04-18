import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

from .models import ConceptDraft, SourceItem
from .utils import safe_slug


class LLMClient:
    DEFAULT_AZURE_API_VERSIONS = [
        "2024-10-21",
        "2024-07-18",
        "2024-02-15-preview",
    ]

    def __init__(self, config: Dict) -> None:
        self.config = dict(config or {})
        self.provider = str(self.config.get("provider") or "openrouter").strip().lower()

        self.max_tokens = int(self.config.get("max_tokens", 1200))
        self.temperature = float(self.config.get("temperature", 0.2))
        self.timeout_seconds = int(self.config.get("request_timeout_seconds", 45))

        self.primary_model = self._resolve_config_value(
            field_name="primary_model",
            env_name=self.config.get("primary_model_env"),
        )
        self.fallback_model = self._resolve_config_value(
            field_name="fallback_model",
            env_name=self.config.get("fallback_model_env"),
        )

        default_api_key_env = "AZURE_OPENAI_API_KEY" if self.provider == "azure_openai" else "OPENROUTER_API_KEY"
        self.api_key_env = str(self.config.get("api_key_env") or default_api_key_env)
        self.api_key = os.getenv(self.api_key_env, "").strip()

        default_base_url = "https://openrouter.ai/api/v1/chat/completions"
        if self.provider == "azure_openai":
            default_base_url = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()

        self.base_url = self._resolve_config_value(
            field_name="base_url",
            env_name=self.config.get("base_url_env"),
            default=default_base_url,
        )
        self.azure_api_versions = self._normalize_api_versions(
            self.config.get("api_versions") or self.config.get("azure_api_versions")
        )

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
            raise RuntimeError(f"{self.api_key_env} is required for non-dry-run execution")
        if not self.primary_model:
            raise RuntimeError("primary_model is missing in LLM configuration")

        prompt = self._build_prompt(source, existing_titles, memory_context)

        last_error: Optional[Exception] = None
        models_to_try = [self.primary_model]
        if self.fallback_model and self.fallback_model != self.primary_model:
            models_to_try.append(self.fallback_model)

        for index, model_name in enumerate(models_to_try):
            retries = 3 if index == 0 else 1
            for attempt in range(retries):
                try:
                    payload = self._request_model(model_name, prompt)
                    return self._parse_payload(payload, source, model_name)
                except Exception as exc:  # noqa: PERF203 - explicit retry loop
                    last_error = exc
                    wait_seconds = 4 * (attempt + 1) if "429" in str(exc) else 2
                    time.sleep(wait_seconds)

        if last_error is not None and len(models_to_try) == 1:
            return self._fallback_draft(source, model_name=models_to_try[0])
        if self.fallback_model:
            return self._fallback_draft(source, model_name=self.fallback_model)
        raise last_error or RuntimeError("LLM request failed")

    def test_text(self, prompt: str, system_prompt: Optional[str] = None, model_name: Optional[str] = None) -> Dict[str, str]:
        chosen_model = model_name or self.primary_model
        if not chosen_model:
            raise RuntimeError("No model configured for test")
        if not self.api_key:
            raise RuntimeError(f"{self.api_key_env} is missing")

        started = time.perf_counter()
        content = self._request_model(chosen_model, prompt, system_prompt=system_prompt)
        latency_ms = int((time.perf_counter() - started) * 1000)
        return {
            "provider": self.provider,
            "model": chosen_model,
            "latency_ms": str(latency_ms),
            "content": content.strip(),
        }

    def _request_model(self, model_name: str, prompt: str, system_prompt: str = None) -> str:
        if self.provider == "azure_openai":
            return self._request_azure_openai(model_name, prompt, system_prompt)
        return self._request_openrouter(model_name, prompt, system_prompt)

    def _request_openrouter(self, model_name: str, prompt: str, system_prompt: Optional[str]) -> str:
        system_text = system_prompt or (
            "You are an expert technical editor for a Turkish wiki. "
            "Return only valid JSON object with these fields: "
            "title, category, summary, key_points, links_to_existing, confidence, novelty."
        )

        request_body = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": system_text,
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

    def _request_azure_openai(self, model_name: str, prompt: str, system_prompt: Optional[str]) -> str:
        if not self.base_url:
            raise RuntimeError("Azure base_url is missing")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        request_body = {
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        data = json.dumps(request_body).encode("utf-8")

        last_error: Optional[Exception] = None
        resource_root = self._azure_resource_root(self.base_url)
        quoted_model = urllib.parse.quote(model_name, safe="")

        for api_version in self.azure_api_versions:
            url = (
                f"{resource_root}/openai/deployments/{quoted_model}/chat/completions"
                f"?api-version={urllib.parse.quote(api_version, safe='')}"
            )
            request = urllib.request.Request(
                url,
                data=data,
                headers={
                    "api-key": self.api_key,
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    raw = response.read().decode("utf-8", errors="ignore")
                parsed = json.loads(raw)
                return parsed["choices"][0]["message"]["content"]
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="ignore")
                last_error = RuntimeError(f"Azure OpenAI request failed ({exc.code}, api-version={api_version}): {body}")
                if exc.code in {400, 404}:
                    continue
                raise last_error

        raise last_error or RuntimeError("Azure OpenAI request failed")

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
            model_used=f"{self.provider}:{model_name}",
            source_url=source.url,
        )

    def _fallback_draft(self, source: SourceItem, model_name: str) -> ConceptDraft:
        summary = source.content[:300].strip()
        title = source.title.strip() or "Untitled Concept"
        category = self._guess_category(title, summary)
        return ConceptDraft(
            slug=safe_slug(title),
            title=title,
            category=category,
            summary=summary,
            key_points=[
                "Bu draft LLM ciktisi alinamadigi icin fallback olarak uretilmistir.",
                "Icerigi manuel gozden gecirin veya yeniden isleyin.",
            ],
            links_to_existing=[],
            confidence=40,
            novelty=30,
            model_used=f"fallback:{self.provider}:{model_name}",
            source_url=source.url,
        )

    @staticmethod
    def _guess_category(title: str, content: str) -> str:
        text = f"{title} {content}".lower()
        security_kw = [
            "security", "vulnerability", "cve", "hack", "auth", "xss",
            "csrf", "jwt", "pentest", "exploit", "zero-trust", "sandbox",
            "malicious", "injection", "cryptomin", "bounty", "credential",
            "ssl", "tls", "rate limit", "bot detect", "güvenlik", "zafiyet",
        ]
        a11y_kw = [
            "accessibility", "a11y", "wcag", "aria", "screen reader",
            "keyboard", "erişilebilirlik", "rgaa",
        ]
        uiux_kw = [
            "ui", "ux", "design", "animation", "css", "tailwind", "figma",
            "color", "typography", "layout", "skeleton", "responsive",
        ]
        backend_kw = [
            "backend", "api", "database", "redis", "postgresql", "node",
            "express", "fastify", "graphql", "prisma", "docker", "deploy",
            "server", "queue", "ci/cd", "kubernetes",
        ]
        frontend_kw = [
            "react", "vue", "svelte", "next", "nuxt", "frontend",
            "browser", "component", "hook", "typescript", "javascript",
            "vite", "webpack", "pwa", "service worker",
        ]

        scores = {
            "security": sum(1 for kw in security_kw if kw in text),
            "a11y": sum(1 for kw in a11y_kw if kw in text),
            "ui-ux": sum(1 for kw in uiux_kw if kw in text),
            "backend": sum(1 for kw in backend_kw if kw in text),
            "frontend": sum(1 for kw in frontend_kw if kw in text),
        }
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "frontend"

    def _resolve_config_value(self, field_name: str, env_name: Optional[str] = None, default: str = "") -> str:
        if env_name:
            env_value = os.getenv(str(env_name), "").strip()
            if env_value:
                return env_value
        return str(self.config.get(field_name) or default).strip()

    @classmethod
    def _normalize_api_versions(cls, raw_versions) -> List[str]:
        if isinstance(raw_versions, list):
            cleaned = [str(item).strip() for item in raw_versions if str(item).strip()]
            if cleaned:
                return cleaned
        return list(cls.DEFAULT_AZURE_API_VERSIONS)

    @staticmethod
    def _azure_resource_root(base_url: str) -> str:
        cleaned = base_url.strip().rstrip("/")
        if cleaned.endswith("/openai/v1"):
            return cleaned[: -len("/openai/v1")]
        return cleaned
