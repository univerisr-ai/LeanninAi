import { startTransition, useDeferredValue, useEffect, useState } from 'react'
import './App.css'

type BrainPage = {
  slug: string
  title: string
  category: string
  status: string
  summary: string
  key_points: string[]
  related_links: string[]
  source_url: string
  generated_at: string
  path: string
  word_count: number
  degree?: number
  is_hot?: boolean
}

type GraphNode = {
  slug: string
  title: string
  category: string
  status: string
  degree: number
}

type GraphEdge = {
  source: string
  target: string
}

type BrainIndex = {
  generated_at: string
  page_count: number
  edge_count: number
  orphan_count: number
  hot_slugs: string[]
  hot_pages?: Array<{
    slug: string
    title: string
    category: string
    summary: string
    degree: number
  }>
  central_pages: Array<{
    slug: string
    title: string
    category: string
    degree: number
  }>
  orphans: string[]
  pages: BrainPage[]
  graph: {
    nodes: GraphNode[]
    edges: GraphEdge[]
  }
}

type RankedPage = {
  page: BrainPage
  score: number
  reasons: string[]
}

const DATA_URL = '/data/query_index.json'
const DEFAULT_RESULT_LIMIT = 14
const CATEGORY_LABELS: Record<string, string> = {
  frontend: 'Frontend',
  'ui-ux': 'UI/UX',
  security: 'Guvenlik',
  backend: 'Backend',
  other: 'Diger',
}

function App() {
  const [brain, setBrain] = useState<BrainIndex | null>(null)
  const [queryInput, setQueryInput] = useState('')
  const [activeCategory, setActiveCategory] = useState('all')
  const [selectedSlug, setSelectedSlug] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const deferredQuery = useDeferredValue(queryInput)

  useEffect(() => {
    const controller = new AbortController()

    async function loadBrain() {
      try {
        setLoading(true)
        const response = await fetch(DATA_URL, { signal: controller.signal })
        if (!response.ok) {
          throw new Error(`Index yuklenemedi (${response.status})`)
        }
        const payload = (await response.json()) as BrainIndex
        setBrain(payload)
      } catch (loadError) {
        if (controller.signal.aborted) {
          return
        }
        setError(
          loadError instanceof Error
            ? loadError.message
            : 'Bilinmeyen bir yukleme hatasi olustu.',
        )
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false)
        }
      }
    }

    void loadBrain()
    return () => controller.abort()
  }, [])

  const pages = brain?.pages ?? []
  const graphNodes = brain?.graph.nodes ?? []
  const graphEdges = brain?.graph.edges ?? []
  const hotSlugs = new Set(brain?.hot_slugs ?? [])
  const degreeBySlug: Record<string, number> = {}
  const slugLookup: Record<string, string> = {}
  const pagesBySlug: Record<string, BrainPage> = {}
  const categoryCounts: Record<string, number> = {}

  for (const node of graphNodes) {
    degreeBySlug[node.slug] = node.degree
  }

  for (const page of pages) {
    pagesBySlug[page.slug] = page
    categoryCounts[page.category] = (categoryCounts[page.category] ?? 0) + 1
    slugLookup[normalizeKey(page.slug)] = page.slug
    const stem = page.slug.split('/').at(-1) ?? page.slug
    slugLookup[normalizeKey(stem)] = page.slug
  }

  const normalizedQuery = normalizeKey(deferredQuery)
  const filteredPages =
    activeCategory === 'all'
      ? pages
      : pages.filter((page) => page.category === activeCategory)
  const rankedPages: RankedPage[] = filteredPages
    .map((page) => {
      const degree = degreeBySlug[page.slug] ?? page.degree ?? 0
      if (!normalizedQuery) {
        return {
          page,
          score: defaultPageScore(page, degree),
          reasons: defaultReasons(page, degree),
        }
      }

      return rankPage(page, normalizedQuery, degree, hotSlugs)
    })
    .filter((item) => (!normalizedQuery ? true : item.score > 0))
    .sort((left, right) => {
      if (right.score !== left.score) {
        return right.score - left.score
      }
      return left.page.title.localeCompare(right.page.title, 'tr')
    })

  const visibleResults = rankedPages.slice(0, DEFAULT_RESULT_LIMIT)
  const defaultSelection =
    visibleResults[0]?.page.slug ??
    brain?.hot_pages?.[0]?.slug ??
    brain?.central_pages[0]?.slug ??
    pages[0]?.slug ??
    ''

  const selectedPage =
    pagesBySlug[selectedSlug] ?? pagesBySlug[defaultSelection] ?? null
  const selectedDegree = selectedPage
    ? degreeBySlug[selectedPage.slug] ?? selectedPage.degree ?? 0
    : 0
  const selectedRelated =
    selectedPage?.related_links
      .map((slug) => slugLookup[normalizeKey(slug)] ?? slug)
      .map((slug) => pagesBySlug[slug])
      .filter((page): page is BrainPage => Boolean(page)) ?? []

  const backlinkSlugs = new Set<string>()
  if (selectedPage) {
    for (const edge of graphEdges) {
      if (edge.source === selectedPage.slug) {
        backlinkSlugs.add(edge.target)
      } else if (edge.target === selectedPage.slug) {
        backlinkSlugs.add(edge.source)
      }
    }
  }

  const backlinks = Array.from(backlinkSlugs)
    .map((slug) => pagesBySlug[slug])
    .filter((page): page is BrainPage => Boolean(page))
    .sort((left, right) => {
      const rightDegree = degreeBySlug[right.slug] ?? right.degree ?? 0
      const leftDegree = degreeBySlug[left.slug] ?? left.degree ?? 0
      if (rightDegree !== leftDegree) {
        return rightDegree - leftDegree
      }
      return left.title.localeCompare(right.title, 'tr')
    })
    .slice(0, 8)

  const categorySummary = Object.entries(categoryCounts).sort((left, right) => {
    if (right[1] !== left[1]) {
      return right[1] - left[1]
    }
    return labelForCategory(left[0]).localeCompare(labelForCategory(right[0]), 'tr')
  })

  return (
    <div className="app-shell">
      <header className="hero-panel">
        <div className="hero-copy">
          <p className="eyebrow">AiBeyin / Brain Navigator</p>
          <h1>Frontend mimarisi, UI/UX ve web guvenligi icin yasayan ikinci beyin.</h1>
          <p className="hero-text">
            Her ingest sonrasi yenilenen bu yuzey; merkez kavramlari, sicak
            konulari ve sayfa baglantilarini tek bakista okunur hale getirir.
          </p>
          <div className="hero-stats" role="list" aria-label="Knowledge metrics">
            <div role="listitem">
              <span>Sayfa</span>
              <strong>{brain?.page_count ?? 0}</strong>
            </div>
            <div role="listitem">
              <span>Bag</span>
              <strong>{brain?.edge_count ?? 0}</strong>
            </div>
            <div role="listitem">
              <span>Yetim</span>
              <strong>{brain?.orphan_count ?? 0}</strong>
            </div>
          </div>
        </div>

        <div className="hero-orbit" aria-hidden="true">
          {(brain?.hot_pages ?? []).slice(0, 5).map((item, index) => (
            <div
              key={item.slug}
              className={`orbit-chip orbit-chip-${index + 1}`}
            >
              <span>{labelForCategory(item.category)}</span>
              <strong>{item.title}</strong>
            </div>
          ))}
        </div>
      </header>

      {loading ? (
        <section className="state-panel">
          <p>Knowledge graph yukleniyor...</p>
        </section>
      ) : error ? (
        <section className="state-panel error-panel">
          <p>{error}</p>
          <p>
            `python scripts/build_brain_index.py` komutu ile statik veriyi tekrar
            uretip sayfayi yenileyebilirsin.
          </p>
        </section>
      ) : (
        <section className="workspace">
          <aside className="signal-rail">
            <div className="rail-section">
              <div className="section-heading">
                <p className="section-kicker">Taze akil</p>
                <h2>Hot cache</h2>
              </div>
              <ul className="plain-list compact-list">
                {(brain?.hot_pages ?? []).slice(0, 5).map((item) => (
                  <li key={item.slug}>
                    <button
                      type="button"
                      className="list-button"
                      onClick={() => setSelectedSlug(item.slug)}
                    >
                      <span>{item.title}</span>
                      <small>{item.degree} bag</small>
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rail-section">
              <div className="section-heading">
                <p className="section-kicker">Dagilim</p>
                <h2>Kategori yogunlugu</h2>
              </div>
              <div className="category-stack">
                {categorySummary.map(([category, count]) => (
                  <button
                    key={category}
                    type="button"
                    className={`category-bar ${
                      activeCategory === category ? 'active' : ''
                    }`}
                    onClick={() =>
                      startTransition(() => {
                        setActiveCategory(category)
                        setSelectedSlug('')
                      })
                    }
                  >
                    <span>{labelForCategory(category)}</span>
                    <strong>{count}</strong>
                  </button>
                ))}
              </div>
            </div>

            <div className="rail-section">
              <div className="section-heading">
                <p className="section-kicker">Bakim riski</p>
                <h2>Yetim sayfalar</h2>
              </div>
              <ul className="plain-list compact-list orphan-list">
                {(brain?.orphans ?? []).slice(0, 6).map((slug) => {
                  const page = pagesBySlug[slug]
                  if (!page) {
                    return null
                  }
                  return (
                    <li key={slug}>
                      <button
                        type="button"
                        className="list-button"
                        onClick={() => setSelectedSlug(page.slug)}
                      >
                        <span>{page.title}</span>
                        <small>{labelForCategory(page.category)}</small>
                      </button>
                    </li>
                  )
                })}
              </ul>
            </div>
          </aside>

          <main className="results-pane">
            <div className="search-strip">
              <label className="search-field" htmlFor="brain-search">
                <span className="search-label">Sorgu</span>
                <input
                  id="brain-search"
                  type="search"
                  placeholder="Ornek: rate limiting, CSP, react forms, PWA..."
                  value={queryInput}
                  onChange={(event) => {
                    const nextValue = event.target.value
                    startTransition(() => {
                      setQueryInput(nextValue)
                      setSelectedSlug('')
                    })
                  }}
                />
              </label>

              <div className="filter-row" role="tablist" aria-label="Categories">
                <button
                  type="button"
                  className={`filter-chip ${
                    activeCategory === 'all' ? 'active' : ''
                  }`}
                  onClick={() =>
                    startTransition(() => {
                      setActiveCategory('all')
                      setSelectedSlug('')
                    })
                  }
                >
                  Tum alanlar
                </button>
                {categorySummary.slice(0, 4).map(([category]) => (
                  <button
                    key={category}
                    type="button"
                    className={`filter-chip ${
                      activeCategory === category ? 'active' : ''
                    }`}
                    onClick={() =>
                      startTransition(() => {
                        setActiveCategory(category)
                        setSelectedSlug('')
                      })
                    }
                  >
                    {labelForCategory(category)}
                  </button>
                ))}
              </div>
            </div>

            <div className="results-header">
              <div>
                <p className="section-kicker">Calisma yuzeyi</p>
                <h2>
                  {normalizedQuery
                    ? `"${deferredQuery}" icin eslesen kavramlar`
                    : 'Merkez kavramlar ve yuksek sinyal notlar'}
                </h2>
              </div>
              <p className="freshness">
                Son index: {formatDateTime(brain?.generated_at ?? '')}
              </p>
            </div>

            <div className="result-list">
              {visibleResults.map(({ page, reasons, score }) => (
                <button
                  key={page.slug}
                  type="button"
                  className={`result-row ${
                    selectedPage?.slug === page.slug ? 'active' : ''
                  }`}
                  onClick={() => setSelectedSlug(page.slug)}
                >
                  <div className="result-topline">
                    <span className="result-category">
                      {labelForCategory(page.category)}
                    </span>
                    <span className="result-score">
                      {normalizedQuery
                        ? `${Math.round(score)} puan`
                        : `${degreeBySlug[page.slug] ?? page.degree ?? 0} bag`}
                    </span>
                  </div>
                  <h3>{page.title}</h3>
                  <p>{page.summary || 'Bu sayfa icin henuz ozet bulunmuyor.'}</p>
                  <div className="reason-row">
                    {reasons.slice(0, 4).map((reason) => (
                      <span key={`${page.slug}-${reason}`} className="reason-pill">
                        {reason}
                      </span>
                    ))}
                  </div>
                </button>
              ))}

              {!visibleResults.length ? (
                <div className="empty-state">
                  <p>Bu filtrede sonuc bulunamadi.</p>
                  <button
                    type="button"
                    className="ghost-action"
                    onClick={() => {
                      startTransition(() => setQueryInput(''))
                      startTransition(() => setActiveCategory('all'))
                    }}
                  >
                    Filtreleri temizle
                  </button>
                </div>
              ) : null}
            </div>
          </main>

          <aside className="detail-pane">
            {selectedPage ? (
              <>
                <div className="detail-head">
                  <p className="section-kicker">Secili not</p>
                  <h2>{selectedPage.title}</h2>
                  <div className="detail-meta">
                    <span>{labelForCategory(selectedPage.category)}</span>
                    <span>{selectedDegree} bag</span>
                    <span>{selectedPage.word_count} kelime</span>
                  </div>
                  <p className="detail-summary">
                    {selectedPage.summary || 'Bu not icin ozet alani bos.'}
                  </p>
                </div>

                <div className="detail-block">
                  <h3>Ana noktalar</h3>
                  <ul className="plain-list detail-list">
                    {selectedPage.key_points.length ? (
                      selectedPage.key_points.slice(0, 5).map((point) => (
                        <li key={point}>{point}</li>
                      ))
                    ) : (
                      <li>Bu sayfada henuz maddelendirilmis ana nokta yok.</li>
                    )}
                  </ul>
                </div>

                <div className="detail-block">
                  <h3>Baglanan sayfalar</h3>
                  <div className="link-grid">
                    {selectedRelated.length ? (
                      selectedRelated.map((page) => (
                        <button
                          key={page.slug}
                          type="button"
                          className="link-tile"
                          onClick={() => setSelectedSlug(page.slug)}
                        >
                          <span>{labelForCategory(page.category)}</span>
                          <strong>{page.title}</strong>
                        </button>
                      ))
                    ) : (
                      <p className="helper-copy">Bu nottan cikan canonical link yok.</p>
                    )}
                  </div>
                </div>

                <div className="detail-block">
                  <h3>Backlink sinyali</h3>
                  <div className="link-grid">
                    {backlinks.length ? (
                      backlinks.map((page) => (
                        <button
                          key={page.slug}
                          type="button"
                          className="link-tile subdued"
                          onClick={() => setSelectedSlug(page.slug)}
                        >
                          <span>{degreeBySlug[page.slug] ?? page.degree ?? 0} bag</span>
                          <strong>{page.title}</strong>
                        </button>
                      ))
                    ) : (
                      <p className="helper-copy">Bu nota henuz baska sayfalar baglanmiyor.</p>
                    )}
                  </div>
                </div>

                <div className="detail-foot">
                  {selectedPage.source_url ? (
                    <a
                      href={selectedPage.source_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Kaynagi ac
                    </a>
                  ) : null}
                  <span>{formatDateTime(selectedPage.generated_at)}</span>
                </div>
              </>
            ) : (
              <div className="empty-state detail-empty">
                <p>Bir not secildiginde detaylar burada acilacak.</p>
              </div>
            )}
          </aside>
        </section>
      )}
    </div>
  )
}

export default App

function normalizeKey(value: string): string {
  return value
    .toLocaleLowerCase('tr')
    .trim()
    .replaceAll('\\', '/')
    .normalize('NFKD')
    .replaceAll(/[\u0300-\u036f]/g, '')
}

function tokenize(value: string): string[] {
  return normalizeKey(value)
    .split(/[^a-z0-9]+/i)
    .map((token) => token.trim())
    .filter(Boolean)
}

function labelForCategory(category: string): string {
  return CATEGORY_LABELS[category] ?? category
}

function defaultPageScore(page: BrainPage, degree: number): number {
  const generatedAt = Date.parse(page.generated_at)
  const now = Date.now()
  const ageInDays = Number.isNaN(generatedAt)
    ? 365
    : Math.max(0, (now - generatedAt) / 86_400_000)
  const freshness = Math.max(0, 30 - ageInDays)
  return degree * 6 + (page.is_hot ? 30 : 0) + freshness
}

function defaultReasons(page: BrainPage, degree: number): string[] {
  const reasons: string[] = []
  if (page.is_hot) {
    reasons.push('Hot cache')
  }
  if (degree >= 5) {
    reasons.push('Merkez dugum')
  }
  if (!reasons.length) {
    reasons.push('Taze not')
  }
  reasons.push(labelForCategory(page.category))
  return reasons
}

function rankPage(
  page: BrainPage,
  normalizedQuery: string,
  degree: number,
  hotSlugs: Set<string>,
): RankedPage {
  const reasons: string[] = []
  const title = normalizeKey(page.title)
  const summary = normalizeKey(page.summary)
  const points = normalizeKey(page.key_points.join(' '))
  const links = normalizeKey(page.related_links.join(' '))
  const category = normalizeKey(page.category)
  const haystack = `${title} ${summary} ${points} ${links} ${category}`.trim()
  const tokens = tokenize(normalizedQuery)

  let score = 0

  if (title.includes(normalizedQuery)) {
    score += 34
    reasons.push('Baslik eslesmesi')
  }
  if (summary.includes(normalizedQuery)) {
    score += 18
    reasons.push('Ozet eslesmesi')
  }
  if (points.includes(normalizedQuery)) {
    score += 14
    reasons.push('Ana noktalar')
  }
  if (category.includes(normalizedQuery)) {
    score += 8
    reasons.push('Kategori')
  }

  const overlapCount = tokens.filter((token) => haystack.includes(token)).length
  score += overlapCount * 5
  if (overlapCount > 0) {
    reasons.push(`${overlapCount} ortak terim`)
  }

  if (degree > 0) {
    score += Math.min(degree, 10) * 0.8
    if (degree >= 4) {
      reasons.push('Baglanti yogun')
    }
  }

  if (hotSlugs.has(page.slug)) {
    score += 5
    reasons.push('Hot cache')
  }

  return {
    page,
    score,
    reasons: Array.from(new Set(reasons)),
  }
}

function formatDateTime(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return 'Tarih bilgisi yok'
  }

  return new Intl.DateTimeFormat('tr-TR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}
