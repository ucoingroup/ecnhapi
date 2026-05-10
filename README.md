# eCNH API Ecosystem Guide

A lightweight, dependency-free Wisdom Atlas web app for comparing social and AI APIs that can support the eCNH community, AI mentor, developer, and growth workflows.

## What is included

- **Top 10 Social APIs** with free-tier notes, pricing, platform fit, and eCNH use cases.
- **Top 10 AI APIs** covering LLMs, RAG, vector search, web research, voice, and creative AI services.
- **Interactive dashboard** with search, category filters, eCNH fit filters, responsive cards, and comparison tables.
- **Recommended eCNH stack** for community operations, AI mentor knowledge base, and growth/developer loops.
- **English / Chinese toggle** for core interface text.

## Run locally

Because the browser blocks `fetch()` for local `file://` JSON in many environments, run the site through any static server from the repository root:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Validate data

```bash
node test/validate-data.mjs
```

The validation script checks that the guide contains 10 social APIs, 10 AI APIs, enough free-tier options, enough best-fit eCNH options, unique API names, and complete card metadata.

## Maintenance notes

API pricing, quotas, and partner program requirements change frequently. Treat the included 2025-2026 pricing notes as guide content, and verify against official provider documentation before production use or budget planning.
