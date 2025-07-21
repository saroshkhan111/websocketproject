# main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.converter import save_chunks_to_webm, convert_to_mp4_and_wav

app = FastAPI(title="WebM Stream Recorder")

# ─── 1) Serve the recordings directory under /recordings ────────────────
app.mount("/recordings", StaticFiles(directory="recordings"), name="recordings")

# ─── 2) HTTP endpoints for quick browser checks ─────────────────────────

@app.get("/health", summary="Heartbeat")
async def health():
    """Check that the server is alive."""
    return {"status": "ok"}

@app.get("/recordings", summary="List all recordings")
async def list_recordings():
    """Return a JSON list of every file in recordings/."""
    folder = Path("recordings")
    files = sorted(p.name for p in folder.iterdir() if p.is_file())
    return {"recordings": files}

@app.get("/watch", response_class=HTMLResponse, summary="Watch latest recording")
async def watch():
    """
    Render an HTML page with the latest .mp4 embedded.
    Falls back to a “no recordings” message if empty.
    """
    folder = Path("recordings")
    mp4s = sorted(p.name for p in folder.iterdir() if p.suffix == ".mp4")
    if not mp4s:
        return "<h1>No recordings yet</h1>"
    latest = mp4s[-1]
    return f"""
    <html>
      <body>
        <h1>Watching: {latest}</h1>
        <video controls width="640" src="/recordings/{latest}">
          Your browser does not support video playback.
        </video>
      </body>
    </html>
    """

# ─── 3) WebSocket endpoint for streaming WebM chunks ────────────────────

active_recordings: dict[str, list[bytes]] = {}

@app.websocket("/ws/record")
async def record_stream(ws: WebSocket):
    await ws.accept()
    client_key = str(ws.client)
    active_recordings[client_key] = []

    try:
        while True:
            msg = await ws.receive()

            # Client signals end of stream
            if msg.get("text") == "FIN":
                # 1️⃣ Write raw WebM
                webm_path = save_chunks_to_webm(
                    active_recordings.pop(client_key),
                    Path("recordings")
                )

                # 2️⃣ Convert to MP4 + WAV
                mp4_path, wav_path = convert_to_mp4_and_wav(
                    webm_path,
                    Path("recordings")
                )

                # 3️⃣ Send back filenames
                await ws.send_json({
                    "status": "saved",
                    "video": mp4_path.name,
                    "audio": wav_path.name
                })

                # 4️⃣ Close the socket cleanly
                await ws.close(code=1000)
                return

            # Otherwise, collect binary chunks
            if "bytes" in msg:
                active_recordings[client_key].append(msg["bytes"])

    except WebSocketDisconnect:
        # Cleanup on early disconnect
        active_recordings.pop(client_key, None)
        print(f"Client {client_key} disconnected early.")
