# Customer Support CRM

A full-stack, web-based customer support management system built for speed and simplicity. 

## Tech Stack
* **Backend:** Python + FastAPI
* **Database:** SQLite (SQLAlchemy ORM)
* **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS
* **Deployment:** Railway.app

## Features Built
1. **Create Tickets:** Auto-generates `TKT-XXX` IDs with timestamps.
2. **List Tickets:** Clean UI displaying ID, Customer, Title, Status, and Date.
3. **Search & Filter:** Real-time quick search across names/emails/IDs, and status filtering.
4. **View & Update:** Detailed modal view to update ticket status and append historical notes.

## How to Run Locally
1. Install requirements: `pip install -r requirements.txt`
2. Start the server: `uvicorn main:app --reload`
3. Visit `http://localhost:8000` in your browser.
