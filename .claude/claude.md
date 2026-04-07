# LLM Wiki Agent Rules

You are my LLM wiki agent. Implement Andrej Karpathy's LLM wiki idea as my second brain. This project is specifically for **Frontend Mimarisi ve Web Site Güvenliği (Frontend Architecture, UI/UX, and Web Security)**.

## Core Rules & Responsibilities
- **Read & Organize:** Read raw data from `raw/` and extract insights into atomic, cross-linked notes in `wiki/`.
- **Maintain Structure:**
  - `raw/`: Raw data input folder. Never modify original data here.
  - `wiki/`: The synthesized knowledge base.
  - `wiki/index.md`: The main entry point (Map of Content). Keep it well-categorized and updated.
  - `wiki/log.md`: An append-only log of what was ingested and when.
  - `wiki/hot.md`: A ~500-word summary of the most recently ingested concepts. It acts as a "hot cache" for quick context.

## Ingestion Workflow
When instructed to ingest a file from `raw/`:
1. **Analyze:** Read the entire raw document.
2. **Chunk & Extract:** Break the content down into smaller, focused "concept" pages (e.g., `wiki/Concept-Name.md`).
3. **Link (Deep Linking):** Add internal markdown links (`[[Concept-Name]]` or `[Concept](./Concept-Name.md)`) to connect related ideas.
4. **Update Index:** Add the new concept files to `wiki/index.md` under relevant headings.
5. **Update Log:** Append the action to `wiki/log.md` with a timestamp.
6. **Update Hot Cache:** Rewrite `wiki/hot.md` to summarize this new knowledge, ensuring it's around 500 words.

## Querying & Maintenance
- **Queries:** When asked questions, grep or read the related `wiki/` files and synthesize the answer.
- **Linting/Maintenance:** Periodically check for missing links, orphaned pages, or logical inconsistencies.
