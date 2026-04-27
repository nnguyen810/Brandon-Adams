# Brandon Adam's Security Services - FastAPI Setup

## 1) Install dependencies

```bash
pip install -r requirements.txt
```

## 2) Configure email settings

Copy `.env.example` to `.env` and fill in your SMTP values.

Required values:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM_EMAIL`
- `SMTP_TO_EMAIL`
- `SMTP_USE_TLS`

## 3) Run the server

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## Endpoints

- `GET /` serves the splash page
- `POST /api/contact` sends contact form email
- `GET /health` basic health check
