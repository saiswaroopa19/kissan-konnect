from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .database import Base, engine
from .routers import auth, programs, applications
from .seed import seed
from .routers import auth, programs, applications, upload

# Run seed to create tables and demo data if not already present
seed()

app = FastAPI(title="Kissan Konnect API", version="1.0.0")

# Allow frontend (default: localhost:5173) to talk to backend
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(programs.router)
app.include_router(applications.router)
app.include_router(upload.router)


# Health check endpoint
@app.get("/health")
def health():
    return {"ok": True}
