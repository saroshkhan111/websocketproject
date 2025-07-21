import asyncio  # ==> This is for running tasks at the same time (without waiting).
import websockets  # ==> This helps us talk to the server in real-time using WebSockets.
from websockets.exceptions import ConnectionClosedOK  # ==> This catches the case when the WebSocket connection closes normally.
from pathlib import Path  # ==> This helps us manage and work with file paths (like finding and reading files).
import sys  # ==> This helps us control the program, like stopping it when there's an error.

# Set the path to the video file we want to send
VIDEO_FILE = Path("sample.webm")  
"""
VIDEO_FILE = Path("sample.webm"):
This line sets the path to a video file called 'sample.webm'. We will use this file later in the program.
"""

async def main():  # ==> Main function where we will write the steps for sending the file.
    # 0️⃣ Verify the test file exists
    if not VIDEO_FILE.exists():  # Check if the video file really exists.
        print(f"Error: {VIDEO_FILE!r} not found. Generate it with ffmpeg first.")  # Tell the user if the file is missing.
        sys.exit(1)  # Exit the program with an error (1 means something went wrong).

    """
    async def main():
    This function does the main work, like checking if the file exists and sending the data.
    
    VIDEO_FILE.exists():   

  #my first project
  print("Hello Ramla")



        
    sys.exit(1):  
    If the file is not found, it stops the program and gives an error message.
    """

    uri = "ws://127.0.0.1:8000/ws/record"  # ==> This is the address of the server we will connect to using WebSockets.
    async with websockets.connect(uri, max_size=None) as ws:  # ==> Open a connection to the server.
        data = VIDEO_FILE.read_bytes()  # ==> Read the content of the video file.

        # 1️⃣ Send the file in 64 KB parts
        for i in range(0, len(data), 64_000):  # Loop through the file and send it in small pieces of 64 KB.
            await ws.send(data[i : i + 64_000])  # Send the piece of data to the server.

        # 2️⃣ Tell the server we’re done
        await ws.send("FIN")  # ==> Send a "FIN" message to let the server know we're done sending the file.

        # 3️⃣ Wait for the server’s response and handle closing
        try:
            response = await ws.recv()  # ==> Wait and receive the server’s response.
            print("Server said:", response)  # ==> Print the server's reply.
        except ConnectionClosedOK:  # ==> If the connection closes normally, do nothing.
            pass  # ==> "pass" means we don't need to do anything if the server closes the connection normally.

if __name__ == "__main__":  # ==> If this is the main program being run, not imported as a module.
    asyncio.run(main())  # ==> Run the main function using asyncio, so it runs the tasks in the right order.
