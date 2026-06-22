# WebM Stream Recorder
**WebM Stream Recorder** is a lightweight web application that receives video data in real time through a WebSocket connection, saves the stream as a WebM recording, and converts it into MP4 video and WAV audio formats. The project is designed to demonstrate real-time media streaming, backend processing, and simple playback through a FastAPI-powered server.

## Description

This project solves the problem of capturing streamed video chunks from a client and processing them into usable media files. A Python WebSocket client sends a `.webm` file in chunks to the server, where the backend stores the recording, converts it, and exposes endpoints for health checks, file listing, and video playback.

It is a strong foundation for applications such as browser-based recording tools, video submission platforms, remote interview systems, and real-time media processing workflows.

## Features

* Real-time WebSocket endpoint for receiving streamed video chunks
* WebM file reconstruction from binary data
* Automatic conversion to MP4 video and WAV audio
* REST endpoint for server health checks
* Endpoint to list saved recordings
* Browser-based playback page for the latest recording
* Test client for sending a sample WebM file
* Clean FastAPI project structure with asynchronous processing

## Tech Stack

* **Backend:** Python, FastAPI
* **Server:** Uvicorn
* **Real-Time Communication:** WebSockets
* **Media Processing:** MoviePy, FFmpeg
* **File Handling:** pathlib
* **Environment Management:** python-dotenv

## Installation

### Prerequisites

Ensure you have the following installed:

* Python 3.10+
* pip
* FFmpeg

### Setup

```bash
git clone https://github.com/username/saroshkhan111-websocketproject.git
cd saroshkhan111-websocketproject
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
mkdir recordings
```

## Usage

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Check server status:

```bash
http://127.0.0.1:8000/health
```

Send a test WebM file using the client:

```bash
python client_test.py
```

Make sure a `sample.webm` file exists in the project root before running the client.

View saved recordings:

```bash
http://127.0.0.1:8000/recordings
```

Watch the latest converted video:

```bash
http://127.0.0.1:8000/watch``

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes with clear messages.
4. Push the branch to your fork.
5. Open a pull request with a short description of your changes.

Please follow clean coding practices and test your changes before submitting.

## Contact

**SaroshKhan**
Email: khansarosh902@gmail.com
LinkedIn: https://www.linkedin.com/in/sarosh-khan-0186a636a/
