# Contributing to AiBeyin

Tesekkurler. AiBeyin, frontend mimarisi, UI/UX, erisilebilirlik ve web guvenligi ekseninde taze bilgiyi kalici bir ikinci beyne donusturmek icin kurulmus bir bilgi tabanidir.

## Katki Ilkeleri

- `raw/` klasorundeki kaynak dosyalari silmeyin veya yerinde degistirmeyin.
- Yeni ogrenim ciktilarini `wiki/` altina atomik, baglantili notlar olarak ekleyin.
- `wiki/index.md`, `wiki/log.md` ve `wiki/hot.md` dosyalarini guncel tutun.
- Bilginin tekrar yazilmasi yerine mevcut kavramlarla bag kurulmasini tercih edin.
- Gizli anahtar, token veya kisisel veri iceren icerigi commitlemeyin.

## Gelistirme Akisi

1. `.env` dosyasini proje kokune yerlestirin.
2. Model baglantilarini dogrulayin:

```powershell
.venv\Scripts\python.exe scripts\test_models.py
```

3. Taze bilgi senkronizasyonu gerekiyorsa harici bilgi deposunu birlestirin:

```powershell
.venv\Scripts\python.exe scripts\sync_learning_repo.py --source LeanninAi-main
```

4. Testleri calistirin:

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

5. Pipeline dry-run ile kaliteyi kontrol edin:

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe scripts\run_pipeline.py --config config/pipeline.json --dry-run
```

## Iyi Pull Request Ozellikleri

- Degisiklik tek bir amaca hizmet etsin.
- Wiki veya storage uzerindeki buyuk guncellemelerde kaynagi ve nedeni acikca yazin.
- Yeni kaynak toplama mantigi ekliyorsaniz rate limit ve duplicate korumasi dusunun.
- Yeni model veya provider ekliyorsaniz `config/model_profiles.json` ve test senaryosunu birlikte guncelleyin.

## Kapsam Disi

- Alakasiz teknoloji kategorileri
- Lisanssiz veri dump'lari
- Kaynak gostermeyen, dogrulanamayan guvenlik iddialari
