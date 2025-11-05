## Vehicle Parking App - V2 (Flask + Vue + SQLite + Redis + Celery)

### Prereqs (macOS M2)
- Homebrew: `brew --version`
- Python 3.11 (brew): `brew install python@3.11`
- Redis: `brew install redis && brew services start redis`

### Setup
```bash
cd /Users/aryanpatil/Desktop/vehicle-parking-app-23f1000968
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Environment (optional, sensible defaults already set in code):
- Default admin: email `admin@example.com` / password `admin123`

### Run App
Terminal 1 (Flask API):
```bash
source .venv/bin/activate
export FLASK_APP=backend/app.py
python -m backend.app
```

Terminal 2 (Celery worker):
```bash
source .venv/bin/activate
celery -A backend.tasks.celery worker --loglevel=info
```

Optional scheduler (to trigger daily/monthly tasks manually you can call tasks from a Python shell). A celery beat config can be added later.

Open UI: `http://127.0.0.1:5000`

### Features Implemented
- Admin (pre-created): create/edit/delete parking lots; auto-create spots; view status
- User: register/login, see lots availability, book first free spot, release, history
- Caching with Redis for common list endpoints
- Celery jobs: CSV export (user-triggered), daily reminder (console log), monthly report (console log)

### Project Layout
```
backend/
  app.py, config.py, extensions.py, models.py
  routes/ auth.py admin.py user.py
  tasks.py
frontend/
  index.html
  assets/ api.js app.js
```

### Notes
- CSV exports are written to `frontend/exports/` folder.
- Adjust default admin via env vars if desired.


