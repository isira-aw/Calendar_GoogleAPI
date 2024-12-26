import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = FastAPI()

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

# Simulate login with email
@app.get("/login/{email}")
def login(email: str):
    if "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    return {"status": "OK", "message": "Code sent to your email", "code": "123456"}

# Simulate verification of the code
@app.get("/verify/{code}")
def verify_code(code: str):
    if code == "123456":
        return {"status": "OK", "message": "Code verified"}
    else:
        raise HTTPException(status_code=400, detail="Invalid code")

# Return sample calendar data
@app.get("/calendar-data")
def get_calendar_data():
    return {"calendar": [{"day": i, "eventCount": 0} for i in range(1, 31)]}
