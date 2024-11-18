import requests
import time

url = 'http://localhost:5000/process_data'

# Пример данных, замените на реальные данные
sphere_images = [
    [500.0, 300.0],
    [450.0, 320.0],
    [600.0, 400.0]
]

image_diameters = [30.0, 28.0, 32.0]

data = {
    'sphere_images': sphere_images,
    'image_diameters': image_diameters
}

while True:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"Received: X={result['x']}, Y={result['y']}, Z={result['z']}")
    else:
        print(f"Error: {response.status_code}")
    time.sleep(0.5)
