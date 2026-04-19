# AiBeyin Brain Navigator

Static React frontend for exploring the AiBeyin second-brain index.

## What it does

- Loads `frontend/public/data/query_index.json`
- Surfaces hot cache items, central pages, orphan risk, and linked notes
- Lets you search the knowledge base without a backend

## Data flow

The frontend is powered by the Python query index generator in the repo root.

```bash
py -3 scripts/build_brain_index.py
```

That command refreshes both:

- `storage/query_index.json`
- `frontend/public/data/query_index.json`

## Development

```bash
npm install
npm run lint
npm run build
```

To run locally:

```bash
npm run dev
```

If the knowledge graph changes, rebuild the index before refreshing the UI.
