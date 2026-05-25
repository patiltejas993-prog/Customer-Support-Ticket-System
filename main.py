from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel
from typing import List, Optional
import database
from database import Ticket, get_db

app = FastAPI(title="Ticket CRM API")

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic Schemas
class TicketCreate(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    description: str

class TicketUpdate(BaseModel):
    status: str
    notes: Optional[str] = ""

# --- ENDPOINTS ---

@app.post("/api/tickets")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    count = db.query(Ticket).count()
    new_ticket_id = f"TKT-{count + 1:03d}"
    
    db_ticket = Ticket(
        ticket_id=new_ticket_id,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    return {"ticket_id": db_ticket.ticket_id, "created_at": db_ticket.created_at}

@app.get("/api/tickets")
def list_tickets(status: Optional[str] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    
    if status and status != "All":
        query = query.filter(Ticket.status == status)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Ticket.customer_name.ilike(search_term),
                Ticket.ticket_id.ilike(search_term),
                Ticket.customer_email.ilike(search_term),
                Ticket.subject.ilike(search_term)
            )
        )
        
    tickets = query.order_by(Ticket.created_at.desc()).all()
    return [
        {
            "ticket_id": t.ticket_id,
            "customer_name": t.customer_name,
            "subject": t.subject,
            "status": t.status,
            "created_at": t.created_at
        } for t in tickets
    ]

@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {
        "ticket_id": ticket.ticket_id,
        "customer_name": ticket.customer_name,
        "customer_email": ticket.customer_email,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status,
        "notes": ticket.notes
    }

@app.put("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: str, ticket_update: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket.status = ticket_update.status
    if ticket_update.notes:
        ticket.notes = ticket.notes + f"\n\n--- Note added ---\n{ticket_update.notes}" if ticket.notes else ticket_update.notes
        
    db.commit()
    db.refresh(ticket)
    return {"success": True, "updated_at": ticket.updated_at}

# Serve the frontend
@app.get("/")
def serve_home():
    return FileResponse("static/index.html")
