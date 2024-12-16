from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import calendar_routes

app = FastAPI(
    title="AI Calendar API",
    description="Backend to fetch and manage calendar events.",
    version="1.0.0",
)

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(calendar_routes.router, prefix="/calendar", tags=["Calendar"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI Calendar Backend!"}

