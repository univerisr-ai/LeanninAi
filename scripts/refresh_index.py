"""Index.md dosyasini yeniden olustur."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.aibeyin.wiki_writer import WikiWriter

project_root = Path(__file__).resolve().parent.parent
writer = WikiWriter(project_root)
writer._refresh_wiki_index()
print("index.md yeniden olusturuldu.")
