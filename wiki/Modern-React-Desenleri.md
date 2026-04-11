# Modern React Desenleri

## Meta
- category: frontend
- status: published


UI geliştirmesinde bileşen (component) bağımlılığını azaltmak ve tekrar kullanılabilirliği (reusability) artırmak için kullanılan mimari tekniklerdir.

## 1. Compound Components (Bileşik Bileşenler)
İç içe geçmiş ancak aynı state'i (React Context üzerinden) paylaşan elementlerdir. En klasik örneği `<select>` ve `<option>` etiketleridir. Biz bunu Tab, Accordion veya Modal yaparken kullanırız.
Props drilling (veriyi 5 kat alta tek tek taşıma) sorununu çözer. Kullanıcıya API olarak esneklik sunar (Sıralamayı komponenti kullanan belirler).

## 2. Polymorphic Components
HTML etiketini prop olarak dışarıdan alabildiğin (örn. `<Text as="h1">...</Text>`) ve TypeScript ile tamamen tip güvenli (O as="a" ise "href" zorunlu olsun) olan bileşenlerdir. Tasarım sistemlerinin temelini oluşturur.

## 3. Optimistic Updates (İyimser Güncellemeler)
Frontend'in sunucu cevabını beklemeden, veritabanına yazılmış *varsayarak* UI'ı anında güncellemesidir. Hız hissi verir. Hata olursa (Error) önceki duruma (rollback) geri döner. En iyi TanStack Query (veya SWR) ile yönetilir.

**İlgili Bağlantılar:**
- [[State-Yonetimi-Zustand-TanStack]]

## 📚 İlgili Draftlar
- [[review/api-response-yapilari-flat-vs-nested-duzlestirilmis-vs-ic-ice]]
- [[review/boneyard-js-cli-driven-skeleton-ui-olusturma]]
- [[review/gunluk-kullandigim-typescript-ipuclari-ve-puf-noktalari]]
- [[review/react-projelerinde-biraktigim-aliskanliklar-ve-kod-kalitem-neden-daha-iyi-oldu]]
- [[review/unicode-para-birimi-sembolleri-ve-u-20c3-uae-dirham-web-de-ozel-karakter-renderi]]