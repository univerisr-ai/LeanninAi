# AiBeyin

AiBeyin, frontend mimarisi, UI/UX, erisilebilirlik ve web guvenligi odakli bir LLM wiki ve ikinci beyin sistemidir. Ham kaynaklari `raw/` klasorunde korur, bunlardan atomik ve baglantili notlar uretir, tekrar ogrenmeyi en aza indirir ve taze bilgiyi `wiki/` icinde kalici hale getirir.

## Ne Saglar

- `raw/` kaynagini bozmadan `wiki/` icine sentez notlar uretir
- `wiki/index.md`, `wiki/log.md`, `wiki/hot.md` dosyalarini bilgi merkezi olarak korur
- `storage/inventory.json` ile kaynak ve kavram seviyesinde tekrar ogrenmeyi azaltir
- GitHub, RSS, Hacker News ve guvenlik feed'lerinden taze kaynak toplayabilir
- OpenRouter ve Azure OpenAI tabanli model profilleriyle test edilebilir
- `LeanninAi-main` gibi daha guncel bir bilgi deposundan kayipsiz senkron alabilir

## Klasor Yapisi

```text
AiBeyin/
├─ raw/                     # Asil ham kaynaklar, yerinde degistirilmez
├─ wiki/                    # Ana bilgi tabani
│  ├─ review/               # Draft / review notlari
│  ├─ reports/              # Haftalik raporlar
│  ├─ index.md              # Ana icerik haritasi
│  ├─ log.md                # Append-only islem gunlugu
│  └─ hot.md                # En yeni kavramlarin hizli ozeti
├─ storage/                 # Envanter, rapor ve run history
├─ config/                  # Pipeline ve model profilleri
├─ scripts/                 # Calistirma, test ve senkron araclari
└─ src/aibeyin/             # Cekirdek uygulama mantigi
```

## Hizli Baslangic

### 1. Ortam

`.env` dosyasini proje kokune koyun. Scriptler bunu otomatik yukler.

Desteklenen ana anahtarlar:

- `OPENROUTER_API_KEY`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_GPT4O_MINI_DEPLOYMENT`
- `AZURE_KIMI_DEPLOYMENT`
- `GITHUB_TOKEN`

### 2. Model baglantilarini test et

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe scripts\test_models.py
```

Yalnizca tek bir profili denemek icin:

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe scripts\test_models.py --profile azure_gpt4o_mini
```

### 3. Guncel bilgi deposunu senkronla

`LeanninAi-main` gibi daha taze bir bilgi deposu varsa:

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe scripts\sync_learning_repo.py --source LeanninAi-main
```

Bu komut:

- yeni wiki dosyalarini ekler
- daha yeni concept kayitlarini birlestirir
- `run_history` ve `last_run_report` verisini korur
- `wiki/index.md` ve `wiki/review/index.md` dosyalarini yeniler

### 4. Pipeline dry-run

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe scripts\run_pipeline.py --config config/pipeline.json --dry-run
```

### 5. Brain query ve graph index

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe scripts\build_brain_index.py
```

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe scripts\query_brain.py "rate limiting ve bot korumasi"
```

Bu katman, projenin sadece ingest yapan bir wiki kalmamasini saglar:

- `storage/query_index.json`: sorgu icin kullanilabilir sayfa ozeti
- `storage/knowledge_graph.json`: sayfalar arasi graph baglantilari
- `scripts/query_brain.py`: local retrieval CLI

### 6. Testler

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Model Profilleri

`config/model_profiles.json` icinde test ve dogrulama icin hazir profiller bulunur:

- `openrouter_default`
- `azure_gpt4o_mini`
- `azure_kimi_k2_5`

Ana pipeline varsayilan olarak `config/pipeline.json` icindeki `llm` profiline bakar. Bu alan provider-agnostic tasarlanmistir; ister OpenRouter ister Azure OpenAI kullanilabilir.

## Bilgi Kaybi Olmadan Ogrenme

AiBeyin'in ana prensibi, ogrenilen bilgiyi koruyarak ilerlemektir.

- Kaynak hash takibi yapar
- Concept fingerprint ve benzerlik kontrolu uygular
- Sistem hafizasini `wiki/system-memory.md` ve `storage/run_history.jsonl` ile modele tasir
- Harici bir taze repo geldiğinde `sync_learning_repo.py` ile union-merge yapar

## Neden Bu Artik Daha Ciddi Bir Ikinci Beyin Adayi

Bu repo artik sadece "RAG denemesi" degil:

- kalici wiki graph'i uretiyor
- local retrieval ile query sonucunu aciklanabilir sekilde veriyor
- hangi sayfanin neden bulundugunu skor ve baglanti nedeni ile gosterebiliyor
- guncel bilgi deposunu kayipsiz merge edebiliyor

## GitHub Hazirligi

Repo artik acik kaynak kullanima daha uygun bir omurgaya sahiptir:

- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- Issue forms
- Pull request template
- Python CI workflow

## Notlar

- `raw/` klasorundeki orijinal veri dosyalari silinmez veya ustunden yazilmaz.
- `.env` repoya dahil edilmez.
- `storage/` ve `wiki/` altindaki degisiklikler bilincli olarak versiyonlanir; bunlar sistemin hafizasidir.
