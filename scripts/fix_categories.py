"""Eski wiki dosyalarina eksik kategori meta verisi ekle."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.aibeyin.utils import read_text, write_text

wiki_root = Path(__file__).resolve().parent.parent / "wiki"

# Bilinen eski dosyalar ve kategorileri
CATEGORY_MAP = {
    "Bot-Tespiti-ve-Honeypot.md": "security",
    "Clean-Architecture.md": "backend",
    "CORS-ve-Guvenlik-Headerlari.md": "security",
    "Erisilebilirlik-WCAG-ve-ARIA.md": "a11y",
    "JWT-ve-Kimlik-Dogrulama.md": "security",
    "Klavye-Navigasyon-Focus.md": "a11y",
    "Modern-React-Desenleri.md": "frontend",
    "Rate-Limiting-Token-Bucket.md": "security",
    "Renk-Teorisi-ve-Tipografi.md": "ui-ux",
    "State-Yonetimi-Zustand-TanStack.md": "frontend",
    "Tasarim-Psikolojisi-Gestalt-Hick.md": "ui-ux",
    "Veritabani-ve-Caching-Stratejileri.md": "backend",
    "Web-Performansi-PWA.md": "frontend",
    "XSS-ve-CSRF-Açiklari.md": "security",
}

fixed = 0
for filename, category in CATEGORY_MAP.items():
    path = wiki_root / filename
    if not path.exists():
        continue
    text = read_text(path)
    if "- category:" in text:
        continue
    # Birinci '# ' başlığından sonra meta bloğu ekle
    lines = text.splitlines()
    insert_idx = None
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_idx = i + 1
            break
    if insert_idx is None:
        insert_idx = 0
    
    meta_block = [
        "",
        "## Meta",
        f"- category: {category}",
        f"- status: published",
        "",
    ]
    new_lines = lines[:insert_idx] + meta_block + lines[insert_idx:]
    write_text(path, "\n".join(new_lines))
    fixed += 1
    print(f"[OK] {filename} -> category: {category}")

print(f"\nToplam {fixed} dosya guncellendi.")
