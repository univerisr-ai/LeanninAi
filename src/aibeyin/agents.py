import logging
from pathlib import Path
from typing import Dict, Optional

from .openrouter import OpenRouterClient
from .utils import now_utc_iso, write_text

logger = logging.getLogger(__name__)

class MultiAgentSystem:
    def __init__(self, openrouter_config: Dict, multi_agent_config: Dict):
        # Temporarily adapt OpenRouterClient max_tokens for coding tasks
        # Coding tasks might require more than the standard wiki summarization tokens.
        or_config = dict(openrouter_config)
        or_config["max_tokens"] = max(int(or_config.get("max_tokens", 4000)), 4000)
        
        self.client = OpenRouterClient(or_config)
        self.config = multi_agent_config
        
        self.maker_model = self.config.get("maker_model", "qwen/qwen3-coder-480b-a35b:free")
        self.reviewer_model = self.config.get("reviewer_model", "meta-llama/llama-3.3-70b-instruct:free")
        self.fixer_model = self.config.get("fixer_model", "qwen/qwen3-coder-480b-a35b:free")
        self.auditor_model = self.config.get("auditor_model", "nousresearch/hermes-3-llama-3.1-405b:free")
        self.architect_model = self.config.get("architect_model", "methexis-inc/trinity-large")
        self.logic_model = self.config.get("logic_model", "liquid/lfm-40b:free")
        
        self.max_retries = int(self.config.get("max_retries", 3))

    def run_coding_task(self, task_description: str, project_root: Path) -> str:
        staging_dir = project_root / "staging"
        logs_dir = project_root / "logs" / "reviews"
        output_dir = project_root / "src" / "output"
        
        for d in [staging_dir, logs_dir, output_dir]:
            d.mkdir(parents=True, exist_ok=True)
            
        timestamp = now_utc_iso().replace(":", "-").replace(".", "-")

        print(f"🚀 [Maker] ({self.maker_model}) ilk yazimi hazirliyor...")
        current_code = self._maker_step(task_description)
        write_text(staging_dir / f"draft_{timestamp}.py", current_code)

        for attempt in range(1, self.max_retries + 1):
            print(f"🔍 [Reviewer] ({self.reviewer_model}) kodu denetliyor... (Deneme {attempt}/{self.max_retries})")
            review_report = self._reviewer_step(task_description, current_code)
            write_text(logs_dir / f"review_{timestamp}_try{attempt}.md", review_report)
            
            # If the reviewer finds no distinct errors or says LGTM (Looks Good To Me)
            if "NO_ERRORS_FOUND" in review_report or "LGTM" in review_report.upper() or len(review_report.split()) < 10:
                 print("✅ [Reviewer] kodda sorun bulamadi, onaylandi!")
                 break
                 
            print(f"🔧 [Fixer] ({self.fixer_model}) rapor isiginda hatalari duzeltiyor...")
            current_code = self._fixer_step(task_description, current_code, review_report)
            write_text(staging_dir / f"draft_{timestamp}_fixed{attempt}.py", current_code)
        else:
            # Reached max retries, invoke High Council (Auditor)
            print(f"⚡ [Auditor/High Council] ({self.auditor_model}) kod cozulemedi, bas mufettis devrede!")
            final_report = self._auditor_step(task_description, current_code, review_report)
            write_text(logs_dir / f"audit_{timestamp}.md", final_report)
            
            print(f"🛡️ [Trinity/Architect] Son duzeltmeyi uyguluyor...")
            current_code = self._fixer_step(task_description, current_code, final_report, model=self.fixer_model)

        final_path = output_dir / f"final_{timestamp}.py"
        write_text(final_path, current_code)
        print(f"🎉 Islem Tamamlandi. Nihai kod: {final_path}")
        return str(final_path)

    def _maker_step(self, task: str) -> str:
        sys_prompt = "Sen uzman bir bas yazilimcisin. Istenilen gorevi eksiksiz kodla."
        prompt = f"Task: {task}\nSadece raw (saf) kodu yaz. Markdown formatlama (```python ... ```) KULLANMA. Aciklama yazma, sadece koda odaklan."
        return self._clean_code(self.client._request_model(self.maker_model, prompt, sys_prompt))

    def _reviewer_step(self, task: str, code: str) -> str:
        sys_prompt = (
            "Sen bir kod denetçisisin. Sana verilen kodu doğrudan çalıştırma, "
            "sadece mantık hatalarını, güvenlik açıklarını ve verimlilik sorunlarını bul. "
            "Cevabını sadece düzeltme listesi olarak ver. Eğer her şey mükemmelse sadece 'NO_ERRORS_FOUND' yaz."
        )
        prompt = f"Orijinal Gorev: {task}\n\nİncelenecek Kod:\n```\n{code}\n```\n\nHataları raporla."
        return self.client._request_model(self.reviewer_model, prompt, sys_prompt)

    def _fixer_step(self, task: str, code: str, report: str, model: Optional[str] = None) -> str:
        model_to_use = model or self.fixer_model
        sys_prompt = "Sen bir kod duzeltme uzmanisin. Log raporundaki hatalari oku ve kodu mukemmel hale getir."
        prompt = (
            f"Orijinal Gorev: {task}\n\nMevcut Kod:\n```\n{code}\n```\n\nMufettis Raporu:\n{report}\n\n"
            "Rapordaki tum sayilan hatalari coz ve sadece nihai kodu ver. Markdown isaretleri kullanma."
        )
        return self._clean_code(self.client._request_model(model_to_use, prompt, sys_prompt))

    def _auditor_step(self, task: str, code: str, prev_report: str) -> str:
        sys_prompt = "Sen 'Bas Mufettis' Hermes'sin. Cok karmasik mimari sorunlari tek bakista anlarsin."
        prompt = (
            f"Gorev: {task}\n\nKod:\n```\n{code}\n```\n\nCozulemeyen Sorunlar Raporu:\n{prev_report}\n\n"
            "Bu koddaki ana sorunu teshis et ve mimari cozum adimlarini kisaca dikte et."
        )
        return self.client._request_model(self.auditor_model, prompt, sys_prompt)
        
    def _clean_code(self, raw_response: str) -> str:
        # LLMs often format code with ```python ... ``` even when instructed not to.
        text = raw_response.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        return text
