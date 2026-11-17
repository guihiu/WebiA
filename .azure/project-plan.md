# Project Plan

## 1. Project Overview
**Status**: Approved
**Created**: 2026-11-17
**Mode**: Standard

A small multilingual Flask informational website for the WebiA project. It explains multilayer perceptrons (MLP) and radial basis function networks (RBF), highlights their differences, and provides dedicated MLP and RBF pages. The interface supports Portuguese, English, and Spanish.

## 2. Requirements Summary
- Build the site with Python and Flask.
- Create a home page with concise explanations of MLP and RBF plus a direct comparison.
- Create separate `/mlp` and `/rbf` pages.
- Provide Portuguese, English, and Spanish language selection that updates the displayed site text.
- Keep the project stateless; no user accounts or persistent datastore are required.
- Reuse a small set of Flask routes and templates to keep the implementation lightweight.

## 3. Architecture & Services
- **Frontend**: Server-rendered HTML, CSS, and a small JavaScript language-switch control.
- **Backend**: One Flask application in Python.
- **Service boundaries**: Public informational routes; no separate API or background worker.
- **Routes**:
  - `/` — home page
  - `/mlp` — MLP information
  - `/rbf` — RBF information
  - language selection via a locale parameter or session

## 4. Data & Storage
**Data Stores**: No datastore required

All page content is stored in Python dictionaries or locale resource files. No database, uploads, object storage, queue, cache, or persistent user data is needed.

## 5. API / Routes
No JSON API is required. Flask routes render server-side Jinja templates:

- `GET /` renders localized home content.
- `GET /mlp` renders the localized MLP page.
- `GET /rbf` renders the localized RBF page.
- `GET /set-language/<locale>` updates the selected language and redirects back to the requested page.

Invalid or unsupported locales fall back to Portuguese.

## 6. Design System & UI
**Component Library**: Pico.css

Use a clean, academic visual style with responsive layouts, accessible navigation, clear headings, and a compact language selector. The home page presents MLP and RBF as paired cards and includes a concise comparison table or list. Dedicated pages use a consistent content layout and provide a link back to the home page.

## 7. Security & Performance
- Enable template escaping and standard Flask configuration.
- Restrict locale values to a fixed allowlist: `pt`, `en`, and `es`.
- Use cacheable static assets and lightweight CSS.
- Add no external identity provider or secret-bearing configuration.
- Return clear 404 handling for unknown routes.

## 8. Implementation Plan
1. Scaffold the Flask application structure and routes.
2. Create localized text resources for Portuguese, English, and Spanish.
3. Build the Jinja templates for the home, MLP, and RBF pages.
4. Implement locale selection and invalid-locale fallback.
5. Add responsive Pico.css-based styling and navigation.
6. Add basic route and translation smoke tests.
7. Run the local Flask server and validate all three pages and language choices.
