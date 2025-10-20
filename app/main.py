# main.py
# FastAPI application with WebSocket support for a multiplayer dice roller

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import json

# Import custom dice utility functions from utils.py
from app import utils


# -------------------------------
# Connection Manager
# -------------------------------
class ConnectionManager:
    """
    Manages active WebSocket connections.
    Provides methods to connect, disconnect, and broadcast messages
    to all connected clients.
    """

    def __init__(self):
        # Keep track of all active WebSocket connections
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection and add it to the list."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from the list."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Send a message to all connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)


# -------------------------------
# FastAPI App Setup
# -------------------------------
manager = ConnectionManager()
app = FastAPI()

# Serve static files (HTML, CSS, JS) from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------------
# HTTP Routes
# -------------------------------
@app.get("/")
async def get_index():
    """
    Root endpoint.
    Returns the index.html file from the static folder.
    """
    index_path = os.path.join("static", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# -------------------------------
# WebSocket Endpoint
# -------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time dice rolling.
    - Accepts messages in JSON format: {"user": "Bob", "dice": ["2d6","1d8"]}
    - Rolls the dice using utils.py functions
    - Broadcasts results to all connected clients
    """
    await manager.connect(websocket)
    try:
        while True:
            # Receive a message from the client
            data = await websocket.receive_text()
            msg = json.loads(data)

            # Prepare results
            all_results = {}
            grand_total = 0

            # Process each dice notation (e.g., "2d6")
            for notation in msg["dice"]:
                n, sides = utils.parse_dice_notation(notation)
                rolls = utils.roll_multiple(n, sides)
                total = sum(rolls)
                all_results[notation] = rolls
                grand_total += total

            # Build the payload to send back
            payload = {
                "user": msg["user"],
                "results": all_results,
                "grand_total": grand_total,
            }

            # Broadcast results to all connected clients
            await manager.broadcast(json.dumps(payload))

    except Exception:
        # On error or disconnect, remove the client
        manager.disconnect(websocket)
