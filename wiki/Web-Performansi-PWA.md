# Web Performansı ve PWA (Service Worker)

## Meta
- category: frontend
- status: published


Kullanıcıyı sistemde tutan en geçerli faktör "Süper Hızlı Çalışan Bir Arayüz" izlenimi vermektir.

## Service Worker (Offline/Proxy Mimarisi)
Service Worker, web sayfanızdan tamamen bağımsız, arka planda çalışan (tarayıcı kapalıyken bile) ve ağ isteklerini kesen (yakalayan) bir Proxy sunucusu gibi çalışır.
- Eğer cihazda internet yoksa, `fetch` isteğini kesip önceden cache'lediği (Catch API ile) dosyaları veya JSON verilerini sunar. 
- Bu sayede web siteniz (Progressive Web App - PWA olarak) tamamen **uygulamaya dönüşür**. İnternetsiz iken Dinozor oyunu çıkmaz, sistem arayüzü çıkar.

## Core Web Vitals Ölçütleri (Google Sıralama Kriterleri)
1. **LCP (Largest Contentful Paint):** Sayfadaki "en büyük görselin/metnin" ne kadar hızlı yüklendiği ölçüsüdür (İdeal < 2.5 saniye). Saniye kurtarmak için ilk görsel Lazy-load (tembel yükleme) yapılmamalı, bilakis `preload` edilmelidir.
2. **CLS (Cumulative Layout Shift):** Sayfa yüklenirken elemanların aşağı yukarı "zıplama" ve "kayma" derecesidir (İdeal "0" olmak zorundadır). Önlemek için Skeleton Loading ([[Tasarim-Psikolojisi-Gestalt-Hick]]) uygulanmalı ve tüm `img` etiketlerine mutlak `width/height` özellikleri önden verilmelidir.
3. **INP (Interaction to Next Paint):** Kullanıcı tıkladığı an (Örn: Sepete ekle) butonun tepki (Görsel state değişimi) vermesi süresidir.

**İlgili Bağlantılar:**
- [[State-Yonetimi-Zustand-TanStack]]
- [[Veritabani-ve-Caching-Stratejileri]]

## 📚 İlgili Draftlar
- [[review/ai-kaynakli-tukenmislik-ve-yazilimci-kaygisi]]
- [[review/boneyard-js-cli-driven-skeleton-ui-olusturma]]
- [[review/gelistirici-deneyimi-ve-arac-secimi-psikolojisi]]
- [[review/tarayicida-calisan-stateless-api-yuk-testi]]
- [[review/unicode-para-birimi-sembolleri-ve-u-20c3-uae-dirham-web-de-ozel-karakter-renderi]]
- [[review/webmcp-devtools-tarayicida-ai-model-baglamini-inceleme-ve-hata-ayiklama]]