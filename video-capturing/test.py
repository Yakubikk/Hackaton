import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def locate_sphere(cameras, sphere_images, image_diameters):
    num_cameras = cameras.shape[0]

    # Преобразование углов азимута в радианы
    azimuths = np.radians(cameras[:, 3])

    # Переменные для системы уравнений
    A = np.zeros((num_cameras, 3))
    B = np.zeros(num_cameras)

    # Заполнение системы уравнений
    for i in range(num_cameras):
        x_cam = cameras[i, 0]
        y_cam = cameras[i, 1]
        z_cam = cameras[i, 2]
        x_img = sphere_images[i, 0]
        y_img = sphere_images[i, 1]
        img_diameter = image_diameters[i]

        # Рассчитать направление луча из камеры на изображение шара
        direction = np.array([np.cos(azimuths[i]), np.sin(azimuths[i]), (x_img - y_img) / img_diameter])

        A[i, :] = direction
        B[i] = np.dot(direction, np.array([x_cam, y_cam, z_cam]))

    # Решение системы уравнений
    result = np.linalg.lstsq(A, B, rcond=None)[0]
    return result

# Параметры камер: [x, y, z, угол азимута (в градусах)]
cameras = np.array([
    [660.0, 760.0, 35.0, -110.0],
    [810.0, 740.0, 45.0, -125.0],
    [900.0, -400.0, 80.0, -225.0]
])

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json
    sphere_images = np.array(data['sphere_images'])
    image_diameters = np.array(data['image_diameters'])

    sphere_coords = locate_sphere(cameras, sphere_images, image_diameters)
    return jsonify({
        'x': sphere_coords[0],
        'y': sphere_coords[1],
        'z': sphere_coords[2]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
