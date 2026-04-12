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
- [[review/a-practical-javascript-roadmap-for-2026-what-actually-matters]]
- [[review/announcing-fuik-a-webhook-engine-for-rails]]
- [[review/cert-gating-every-tool-call-zero-trust-for-ai-agents]]
- [[review/cve-2026-23869-the-precompute-pattern-boneyard-use-cache-migration-rsc-boundary]]
- [[review/from-idea-to-paid-saas-in-24-hours-the-claude-code-blueprint-is-live]]
- [[review/front-end-struggles]]
- [[review/how-ai-voice-agents-enhance-customer-support-and-sales]]
- [[review/how-i-automated-62-of-europe-s-rgaa-accessibility-criteria]]
- [[review/how-i-built-a-tinder-style-group-decision-app-with-react-native-and-firebase]]
- [[review/how-i-built-a-web-interface-for-1-4-million-government-documents-with-fastapi-htmx-and-sqlite]]
- [[review/how-i-fixed-transparent-video-alpha-in-playwright-using-1970s-film-math]]
- [[review/how-to-add-human-approval-to-mcp-tool-calls-no-code-changes]]
- [[review/how-to-improve-ux-in-legacy-systems]]
- [[review/how-to-prove-compliance-in-ai-generated-code]]
- [[review/i-built-a-captcha-replacement-after-ai-hit-91-bypass-rate]]
- [[review/i-built-a-free-hydration-tracker-with-no-signup-here-s-what-i-learned]]
- [[review/i-built-an-ai-workflow-for-bug-bounty-automation-here-is-what-worked]]
- [[review/i-built-an-email-verification-api-from-scratch]]
- [[review/i-got-cryptomined-5-times-in-10-days-here-s-my-story]]
- [[review/i-keep-telling-claude-the-same-things-so-he-started-writing-them-down-himself]]
- [[review/i-wrote-a-novel-about-personal-ai-in-2017-in-2026-i-built-it]]
- [[review/lost-your-private-key-for-your-ssl-certificate-here-is-how-to-fix-it-in-10-minutes]]
- [[review/nomshub-how-to-check-if-your-mac-was-affected-by-the-cursor-sandbox-escape]]
- [[review/not-yet-falco-ai-agent-part-1-real-time-kubernetes-security-analysis-with-claude]]
- [[review/react-flexi-window-v2-0-i-added-a-wasm-powered-liquid-glass-engine-to-my-react-window-component]]
- [[review/sdk-v0-2-9-output-verification-attestations-preflight-and-budgets]]
- [[review/secure-truenas-plex-setup-for-your-homelab]]
- [[review/soft-deleting-postgres-rows-without-losing-the-url-slug]]
- [[review/the-ethical-grey-coding-for-results-when-the-best-practices-manual-is-burning]]
- [[review/the-formula-was-exact-the-assumption-was-wrong-that-s-not-an-ai-problem]]
- [[review/the-most-valuable-signal-on-my-network-was-silence]]
- [[review/this-week-in-react-276-boneyard-ink-mui-react-router-next-js-rn-0-85-viewtransition-skia-windows-jsir-security-esbuild-ky-intl]]
- [[review/typescript-tip-cikarma-motoru-yazmak]]
- [[review/ucp-april-2026-cart-catalog-and-signals-change-everything]]
- [[review/we-built-an-open-source-coding-exam-platform-because-every-vendor-let-us-down]]
- [[review/what-if-you-could-reverse-a-template-engine]]
- [[review/why-math-random-will-fail-your-next-security-audit]]
- [[review/wordpress-7-0-the-good-the-ai-and-the-still-missing]]