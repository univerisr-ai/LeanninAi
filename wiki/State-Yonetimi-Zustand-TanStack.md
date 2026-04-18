# State Yönetimi: Zustand ve TanStack Query

## Meta
- category: frontend
- status: published


Redux'ın karmaşıklığı yerine, modern state yönetiminde state iki farklı sorumluluğa bölünür: Sunucu State'i ve İstemci (UI) State'i.

## Sunucu (Server) State: TanStack Query
Veritabanında yaşayan veridir. Biz sadece ekranımızdaki kopyayı görürüz.
- **Sorumlulukları:** Veri çekme (fetch), önbellekleme (caching), arka planda senkronize etme, iyimser güncellemeler (Optimistic UI), pagination ve re-fetching (Odaklanınca veriyi tazele).
- **Avantajı:** `useEffect` spagetti kodundan kurtarır, loading/error statelerini otomatik verir. Asla `loading` isimli useState oluşturmak zorunda kalmazsınız.

## İstemci (UI) State: Zustand
Sadece tarayıcıda yaşayan (sekme kapanınca ölecek olan) geçici arayüz verisidir.
- **Örnekler:** Modal'ın açık olup olmaması, dark/light mode sekme tercihi, form'un adım sayısı.
- **Neden Zustand?** Redux gibi boilerplate (tekrar eden kod yığını) taşımaz. Provider sarmalaması (`<Provider>`) istemez (Context API re-render sorunu yaşatmaz). Sadece hook olarak kullanılır ve atomiktir.

**İlgili Bağlantılar:**
- [[Modern-React-Desenleri]]
- [[Clean-Architecture]]

## 📚 İlgili Draftlar
- [[ai-kaynakli-tukenmislik-ve-yazilimci-kaygisi]]
- [[ai-saas-baslangic-kiti-mimarisi-tekrarlanan-kurulum-sureclerini-otomatiklestirme]]
- [[review/api-response-yapilari-flat-vs-nested-duzlestirilmis-vs-ic-ice]]
- [[review/react-projelerinde-biraktigim-aliskanliklar-ve-kod-kalitem-neden-daha-iyi-oldu]]
- [[webmcp-devtools-tarayicida-ai-model-baglamini-inceleme-ve-hata-ayiklama]]