# Brandon Adam's Security Services

This repo now supports static hosting on GitHub Pages.

## GitHub Pages deployment

1. Push this repository to GitHub.
2. Ensure your default branch is `main`.
3. In GitHub, open **Settings -> Pages**.
4. Under **Build and deployment**, choose **Source: GitHub Actions**.
5. Push any new commit to `main` and the workflow will deploy automatically.

Your site URL will be:

- `https://<your-username>.github.io/<repo-name>/`

## Contact form email on GitHub Pages

GitHub Pages only hosts static files. It cannot run `main.py` or `/api/contact` by itself.

This project now supports two contact form modes via [static/site-config.js](static/site-config.js):

- `window.CONTACT_FORM_ENDPOINT` for static email sending (recommended for GitHub Pages)
- `window.CONTACT_API_URL` for your own hosted backend API

### Quick setup (no backend) with FormSubmit

1. Open [static/site-config.js](static/site-config.js).
2. Set:

```js
window.CONTACT_FORM_ENDPOINT = "https://formsubmit.co/YOUR_EMAIL@example.com";
```

3. Leave `window.CONTACT_API_URL = "";`
4. Commit and push.
5. Submit the contact form once and confirm your email address in FormSubmit's verification email.

After verification, submissions from your GitHub Pages site will be delivered to your inbox.

### Using your own API instead

Set:

```js
window.CONTACT_API_URL = "https://your-api-domain/api/contact";
```

If both are set, the form uses `CONTACT_API_URL` first.

## Optional local API (FastAPI)

If you still want to run the backend locally or on another host:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set SMTP values.

3. Run:

```bash
uvicorn main:app --reload
```
