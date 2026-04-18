# Security Policy

AiBeyin, web guvenligi ve agentik otomasyonla ilgili bilgiler tuttugu icin gizli bilgi yonetimi ve sorumlu aciklama bizim icin kritik.

## Desteklenen Guvenlik Kapsami

- `.env` veya CI secret yonetimi
- Kaynak toplama ve pipeline icinde token sizintisi riski
- Wiki icine hassas veri yazilmasi
- Otomatik GitHub aksiyonlarinda yetki ve commit guvenligi
- Agent veya model entegrasyonlarinda istemsiz veri disari cikisi

## Guvenlik Acigi Bildirimi

Bir zafiyet veya secret sizintisi bulursan:

1. Public issue acmayin.
2. Etkilenen dosya veya akis yolunu net yazin.
3. Yeniden uretim adimlarini ve beklenen riski ekleyin.
4. Mümkünse etkisini azaltan gecici bir oneri iletin.

Bu repo icin varsayilan kanal GitHub uzerinden private security report veya depo sahibine dogrudan bildirimdir.

## Sorumlu Davranis

- Gercek API key, token veya cookie paylasmayin.
- Sadece gerekli minimum kaniti iletin.
- Zafiyet cozumu yayinlanmadan exploit detaylarini yaymayin.
