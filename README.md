# Kissan Konnect — Full-stack starter

Government-style subsidy portal for farmers (India-inspired).

## Stack
- **Backend**: FastAPI, SQLAlchemy, JWT, SQLite
- **Frontend**: React (Vite), axios, React Router

## Quick start

### 1) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Optional: cp .env.sample .env  (edit secrets)
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend
```bash
cd frontend
npm install
# set API base if needed:
echo "VITE_API_URL=http://localhost:8000" > .env.local
npm run dev
```

### 3) Login
- Register a farmer account on `/register`
- Admin account: `admin@kissan.local` / `Admin@12345`

## Notes
- Uploads saved to `backend/uploads/`
- Seed data includes crops and 3 demo programs.
- Tokens: access (30m), refresh (7d) with rotation.

## Next steps
- Program details page: replace numeric IDs with names (UI mapping call)
- Add status history timeline & document viewer
- Migrate to Postgres for prod, add backups
- Add consent and privacy pages (NZ Privacy Act 2020 compliance)
# kissan-konnect
