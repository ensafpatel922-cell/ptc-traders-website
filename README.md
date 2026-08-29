# PTC Traders — Complete Website

## Features
- Buyer-focused potato procurement website
- Bulk potato supply
- Contract farming section
- Buyer inquiry form
- Flask backend
- SQLite database
- Admin inquiry dashboard at `/admin`
- WhatsApp and phone buttons
- Responsive mobile design

## Run locally (Windows / VS Code)

1. Install Python 3.11+.
2. Open this folder in VS Code terminal.
3. Create a virtual environment:
   `python -m venv venv`
4. Activate it:
   Windows PowerShell:
   `venv\Scripts\Activate.ps1`
   Windows CMD:
   `venv\Scripts\activate`
5. Install:
   `pip install -r requirements.txt`
6. Run:
   `python app.py`
7. Open:
   `http://127.0.0.1:5000`
8. Admin:
   `http://127.0.0.1:5000/admin`

## Before public launch
- Change SECRET_KEY in app.py.
- Add proper admin login/authentication before exposing `/admin` publicly.
- Add your actual business photos, potato specifications, packing, capacity, service areas and verified claims.
- Use McCain name/logo and relationship wording only as permitted by your agreement/authorization.
- For production, use a proper WSGI server and HTTPS.

## What happens to buyer inquiries?
The form is submitted to Flask -> stored in `ptc_traders.db` -> visible in the admin dashboard.


## Admin Login

Admin URL:
`http://127.0.0.1:5000/admin`

Default credentials in this demo:
- Username: `admin`
- Password: `PTC@2026ChangeMe`

IMPORTANT: Change `ADMIN_PASSWORD` and `SECRET_KEY` in `app.py` before putting the website online.
For production, use environment variables and HTTPS.
