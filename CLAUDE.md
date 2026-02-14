# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal finance tracker ("Planilha Financeira") — a single-page web app for monthly income/expense management. All code lives in one self-contained `index.html` file (HTML + CSS + JS inline). No build system, no package manager, no external dependencies (except Google Fonts).

## Development

**Run the app:** Open `index.html` directly in a browser, or serve locally:
```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

**Test (Playwright):** `test_app.py` contains E2E tests that expect the app running on `localhost:8000`:
```bash
python3 -m http.server 8000 &
python3 test_app.py
```

**No lint/build/typecheck** — pure vanilla HTML/CSS/JS with no tooling.

## Architecture

Everything is in `index.html` (~1000 lines):
- **CSS** (lines 12-576): Glassmorphism dark-mode design system using CSS custom properties (`--glass-*`, `--text-*`, color tokens). Responsive at 1200px breakpoint.
- **HTML** (lines 579-693): 3-column layout — header with month/year selector, KPI cards (income/expenses/balance), then main grid (income list, expense list, chart + notes).
- **JS** (lines 696-1011): All app logic in a single `<script>` block.

### Data Model

```js
dados = { mes, ano, saidas: [{descricao, valor, categoria}], entradas: [{descricao, valor}], notas }
```

localStorage key pattern: `planilha-financeira-{month}-{year}` (one entry per month/year).

### Key Functions
- `salvarDados()` / `carregarDados()` — localStorage persistence
- `renderRows(tipo, containerId)` — renders income or expense list
- `renderizar()` — full UI refresh
- `calcularTotais(animate)` — updates KPIs, delta comparison with previous month, triggers chart
- `desenharGrafico(items, total, progress)` — Canvas API donut chart by category
- `copiarMesAnterior()` — imports previous month's data

### Categories (expenses only)
Defined in `CATEGORIAS` object: casa, cartao, educacao, saude, transporte, lazer, investimento, outros. Each has label, color, and icon.

## Conventions

- All UI text and variable names are in **Portuguese (pt-BR)**
- Currency format: `R$ 1.234,56` (Brazilian Real)
- Values stored as floats, formatted via `toLocaleString('pt-BR', {style:'currency', currency:'BRL'})`
- When modifying the app, all changes must stay within the single `index.html` file
