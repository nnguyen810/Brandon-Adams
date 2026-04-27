import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Brandon Adam's Security Services API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/CSS", StaticFiles(directory=str(BASE_DIR / "CSS")), name="css")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


class ContactRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = Field(default="", max_length=40)
    message: str = Field(min_length=10, max_length=2000)


@app.get("/")
def home() -> FileResponse:
    return FileResponse(BASE_DIR / "home.html")


@app.get("/about")
def about() -> FileResponse:
    return FileResponse(BASE_DIR / "about.html")


@app.get("/services")
def services() -> FileResponse:
    return FileResponse(BASE_DIR / "services.html")


@app.get("/contact")
def contact() -> FileResponse:
    return FileResponse(BASE_DIR / "contact.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/contact")
def submit_contact(payload: ContactRequest) -> dict[str, str]:
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL", "")
    smtp_to_email = os.getenv("SMTP_TO_EMAIL", "")
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    missing = [
        key
        for key, value in {
            "SMTP_HOST": smtp_host,
            "SMTP_USERNAME": smtp_username,
            "SMTP_PASSWORD": smtp_password,
            "SMTP_FROM_EMAIL": smtp_from_email,
            "SMTP_TO_EMAIL": smtp_to_email,
        }.items()
        if not value
    ]

    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Server email is not configured. Missing: {', '.join(missing)}",
        )

    subject = f"New Security Inquiry - {payload.name}"

    text_body = (
        "New contact request submitted\n\n"
        f"Name: {payload.name}\n"
        f"Email: {payload.email}\n"
        f"Phone: {payload.phone or 'Not provided'}\n\n"
        "Message:\n"
        f"{payload.message}\n"
    )

    html_body = f"""
    <h2>New Security Inquiry</h2>
    <p><strong>Name:</strong> {payload.name}</p>
    <p><strong>Email:</strong> {payload.email}</p>
    <p><strong>Phone:</strong> {payload.phone or 'Not provided'}</p>
    <p><strong>Message:</strong></p>
    <p>{payload.message.replace(chr(10), '<br>')}</p>
    """

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = smtp_from_email
    message["To"] = smtp_to_email
    message["Reply-To"] = str(payload.email)
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            if smtp_use_tls:
                server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Failed to send email.") from exc

    return {"message": "Thanks. Your request has been sent."}
