import cv2 as cv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open camera")

async def video_streaming():
    while True:
        _, frame = cap.read()
        _, buffer = cv.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/stream")
async def main():
    return StreamingResponse(video_streaming(), 
                             media_type="multipart/x-mixed-replace; boundary=frame")
