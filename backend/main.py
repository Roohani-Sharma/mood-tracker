from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

app = FastAPI()

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Mount static and template directories
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Mood tracking dictionary
mood_counts = {"happy": 0, "meh": 0, "sad": 0}
moods_data = []

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/mood/{mood_type}")
async def update_mood(mood_type: str):
    if mood_type in mood_counts:
        mood_counts[mood_type] += 1
        return {"message": "Mood updated", "mood": mood_counts}
    return {"error": "Invalid mood type"}

@app.get("/summary")
async def get_summary():
    return JSONResponse(content=mood_counts)
from fastapi import WebSocket, WebSocketDisconnect

connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            mood = data.get("mood")
            # Send all moods back to everyone (basic tracking)
            mood_data = {"moods": [mood for _ in connected_clients]}
            for client in connected_clients:
                await client.send_json(mood_data)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static" , "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Mood tracking dictionary with reasons
mood_counts = {"happy": 0, "meh": 0, "sad": 0}
mood_reasons = {"happy": [], "meh": [], "sad": []}
connected_clients = []

def generate_affirmation(mood: str) -> str:
    affirmations = {
        "happy": ["Great job!", "You're doing amazing!", "Keep it up!"],
        "meh": ["You're doing alright, keep going!", "Stay positive, it gets better!"],
        "sad": ["It's okay to feel down sometimes. You'll get through it."]
    }
    return random.choice(affirmations.get(mood, ["You're valid no matter what you're feeling."]))

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/mood/{mood_type}")
async def update_mood(mood_type: str, reason: str = None):
    if mood_type in mood_counts:
        mood_counts[mood_type] += 1
        if reason:
            mood_reasons[mood_type].append(reason)
        affirmation = generate_affirmation(mood_type)
        return {"message": "Mood updated", "mood": mood_counts, "affirmation": affirmation}
    return {"error": "Invalid mood type"}

@app.get("/summary")
async def get_summary():
    return JSONResponse(content=mood_counts)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()  # Receive JSON data from client
            mood = data.get("mood")  # Extract mood type
            reason = data.get("reason")  # Get the reason if provided
            
            # Update the mood count
            if mood in mood_counts:
                mood_counts[mood] += 1
                if reason:
                    mood_reasons[mood].append(reason)
            
            # Generate an affirmation for the mood
            affirmation = generate_affirmation(mood)

            # Send updated data (including affirmation) to all connected clients
            mood_data = {
                "moods": mood_counts,
                "affirmation": affirmation
            }
            for client in connected_clients:
                await client.send_json(mood_data)

    except WebSocketDisconnect:
        connected_clients.remove(websocket)

