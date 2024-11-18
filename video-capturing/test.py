import math

class Camera:
    def __init__(self, x, y, z, azimuth):
        self.x = x
        self.y = y
        self.z = z
        self.azimuth = azimuth

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Matrix:
    def __init__(self, focal_length, sensor_width, sensor_height):
        self.focal_length = focal_length  # мм
        self.sensor_width = sensor_width  # мм
        self.sensor_height = sensor_height  # мм

def project_to_3d(camera, pos, matrix):
    # Размеры сенсора в метрах
    sensor_width = matrix.sensor_width / 1000  # мм -> метры
    sensor_height = matrix.sensor_height / 1000  # мм -> метры

    # Центр изображения (в пикселях)
    center_x = sensor_width / 2
    center_y = sensor_height / 2

    # Разница между центральной точкой и позицией шара на изображении
    dx = (pos.x - center_x) * (sensor_width / matrix.sensor_width)
    dy = (pos.y - center_y) * (sensor_height / matrix.sensor_height)

    # Преобразуем в мировые координаты, используя фокусное расстояние
    fx = matrix.focal_length / 1000  # фокусное расстояние в метрах
    ray_x = dx * fx
    ray_y = dy * fx
    ray_z = fx  # луч всегда будет иметь длину, равную фокусному расстоянию

    # Поворот камеры: азимут (отрицательное значение азимута — поворот по часовой стрелке)
    azimuth_rad = camera.azimuth * math.pi / 180.0

    # Преобразуем координаты луча в мировую систему координат
    rotated_x = ray_x * math.cos(azimuth_rad) - ray_y * math.sin(azimuth_rad)
    rotated_y = ray_x * math.sin(azimuth_rad) + ray_y * math.cos(azimuth_rad)

    # Возвращаем 3D координаты луча (в мировых координатах камеры)
    return rotated_x + camera.x, rotated_y + camera.y, ray_z + camera.z

def calculate_sphere_coordinates(cam1, cam2, cam3, pos1, pos2, pos3, matrix):
    # Преобразуем координаты на изображениях в 3D-лучи для каждой камеры
    ray1 = project_to_3d(cam1, pos1, matrix)
    ray2 = project_to_3d(cam2, pos2, matrix)
    ray3 = project_to_3d(cam3, pos3, matrix)

    # Рассчитываем систему уравнений для t1, t2, t3
    t1 = (ray2[0] - ray1[0]) / (ray3[0] - ray1[0])  # Примерное решение для t1
    t2 = (ray2[1] - ray1[1]) / (ray3[1] - ray1[1])  # Примерное решение для t2
    t3 = (ray2[2] - ray1[2]) / (ray3[2] - ray1[2])  # Примерное решение для t3

    # Рассчитываем точку пересечения лучей
    x = ray1[0] + t1 * (ray2[0] - ray1[0])
    y = ray1[1] + t2 * (ray2[1] - ray1[1])
    z = ray1[2] + t3 * (ray2[2] - ray1[2])

    # Возвращаем координаты шара
    return x, y, z

def main():
    # Примерные параметры камер
    camera1 = Camera(660, 760, 35, -110)
    camera2 = Camera(810, 740, 45, -125)
    camera3 = Camera(900, -400, 80, -225)

    # Параметры матрицы камеры
    matrix = Matrix(35000, 23.76, 13.365)  # мм

    # Примерные координаты шарика на изображениях (предположим, что их можно взять из изображения)
    sphere_pos_on_cam1 = Point2D(1200, 1500)
    sphere_pos_on_cam2 = Point2D(1400, 1600)
    sphere_pos_on_cam3 = Point2D(1100, 1200)

    # Вычисляем координаты шара
    sphere_coordinates = calculate_sphere_coordinates(
        camera1, camera2, camera3,
        sphere_pos_on_cam1, sphere_pos_on_cam2, sphere_pos_on_cam3,
        matrix
    )

    print(f"Sphere coordinates: X={sphere_coordinates[0]}, Y={sphere_coordinates[1]}, Z={sphere_coordinates[2]}")

if __name__ == "__main__":
    main()
