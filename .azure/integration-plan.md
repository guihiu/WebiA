# Integration Plan

## Backend
- Project folder: workspace root
- Entry point: `app.py`
- Run command: `python app.py`
- Port: `5000`
- Build command: none
- Health route: `GET /`

## Frontend
- Project folder: `templates/` and `static/`
- Build command: none
- Dev command: `python app.py`
- API seam: none; the Flask/Jinja application is server-rendered
- Mock files: none

## API Routes
- `GET /` — localized overview and MLP/RBF comparison
- `GET /mlp` — localized MLP page
- `GET /rbf` — localized RBF page
- `GET /set-language/<locale>?next=<path>` — switch locale and redirect

## Database
- No database.
- No migrations.
- No seed data.

## Shared Types
- Localized content dictionary: `locales.py`

## Services
- Essential: Flask web application
- Enhancement: none
