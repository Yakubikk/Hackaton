from flask import Flask, Response, jsonify, request
import cv2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

is_streaming = False  # Флаг состояния потока
camera = None  # Глобальная переменная для камеры

def start_camera():
    """Инициализирует камеру."""
    global camera
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0)

def release_camera():
    """Освобождает камеру."""
    global camera
    if camera is not None:
        camera.release()
        
        camera = None

def generate_frames():
    """Генерирует кадры из камеры."""
    global camera
    start_camera()  # Убедиться, что камера инициализирована

    while is_streaming:  # Проверяем флаг состояния
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/stream')
def video_feed():
    """Отправляет поток в браузер."""
    if not is_streaming:
        return "Stream is not active", 403
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control_stream():
    """Управляет состоянием потока."""
    global is_streaming

    action = request.json.get('action')
    if action == 'start':
        if not is_streaming:
            is_streaming = True
        return jsonify({'status': 'started'})
    elif action == 'stop':
        if is_streaming:
            is_streaming = False
            release_camera()  # Освобождаем ресурсы камеры
        return jsonify({'status': 'stopped'})
    return jsonify({'error': 'Invalid action'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
