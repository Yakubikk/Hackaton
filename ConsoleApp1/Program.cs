using System;

class Program
{
    public struct Camera
    {
        public double X, Y, Z, Azimuth;
        public Camera(double x, double y, double z, double azimuth)
        {
            X = x;
            Y = y;
            Z = z;
            Azimuth = azimuth;
        }
    }

    public struct Point2D
    {
        public double X, Y;
        public Point2D(double x, double y)
        {
            X = x;
            Y = y;
        }
    }

    public struct Matrix
    {
        public double FocalLength; // мм
        public double SensorWidth;  // мм
        public double SensorHeight; // мм
        public Matrix(double focalLength, double sensorWidth, double sensorHeight)
        {
            FocalLength = focalLength;
            SensorWidth = sensorWidth;
            SensorHeight = sensorHeight;
        }
    }

    static void Main(string[] args)
    {
        // Примерные параметры камер
        var camera1 = new Camera(660, 760, 35, -110);
        var camera2 = new Camera(810, 740, 45, -125);
        var camera3 = new Camera(900, -400, 80, -225);

        // Параметры матрицы камеры
        var matrix = new Matrix(35000, 23.76, 13.365); // мм

        // Примерные координаты шарика на изображениях (предположим, что их можно взять из изображения)
        var spherePosOnCam1 = new Point2D(1200, 1500);
        var spherePosOnCam2 = new Point2D(1400, 1600);
        var spherePosOnCam3 = new Point2D(1100, 1200);

        // Вычисляем координаты шара
        var sphereCoordinates = CalculateSphereCoordinates(camera1, camera2, camera3, spherePosOnCam1, spherePosOnCam2, spherePosOnCam3, matrix);

        Console.WriteLine($"Sphere coordinates: X={sphereCoordinates.X}, Y={sphereCoordinates.Y}, Z={sphereCoordinates.Z}");
    }

    // Преобразование координат изображения в 3D-луч
    static (double, double, double) ProjectTo3D(Camera camera, Point2D pos, Matrix matrix)
    {
        // Размеры сенсора в метрах
        double sensorWidth = matrix.SensorWidth / 1000;  // мм -> метры
        double sensorHeight = matrix.SensorHeight / 1000; // мм -> метры

        // Центр изображения (в пикселях)
        double centerX = sensorWidth / 2;
        double centerY = sensorHeight / 2;

        // Разница между центральной точкой и позицией шара на изображении
        double dx = (pos.X - centerX) * (sensorWidth / matrix.SensorWidth);
        double dy = (pos.Y - centerY) * (sensorHeight / matrix.SensorHeight);

        // Преобразуем в мировые координаты, используя фокусное расстояние
        double fx = matrix.FocalLength / 1000; // фокусное расстояние в метрах
        double rayX = dx * fx;
        double rayY = dy * fx;
        double rayZ = fx; // луч всегда будет иметь длину, равную фокусному расстоянию

        // Поворот камеры: азимут (отрицательное значение азимута — поворот по часовой стрелке)
        double azimuthRad = camera.Azimuth * Math.PI / 180.0;

        // Преобразуем координаты луча в мировую систему координат
        double rotatedX = rayX * Math.Cos(azimuthRad) - rayY * Math.Sin(azimuthRad);
        double rotatedY = rayX * Math.Sin(azimuthRad) + rayY * Math.Cos(azimuthRad);

        // Возвращаем 3D координаты луча (в мировых координатах камеры)
        return (rotatedX + camera.X, rotatedY + camera.Y, rayZ + camera.Z);
    }

    // Функция для нахождения координат шара через систему линейных уравнений
    static (double X, double Y, double Z) CalculateSphereCoordinates(
        Camera cam1, Camera cam2, Camera cam3,
        Point2D pos1, Point2D pos2, Point2D pos3,
        Matrix matrix)
    {
        // Преобразуем координаты на изображениях в 3D-лучи для каждой камеры
        var ray1 = ProjectTo3D(cam1, pos1, matrix);
        var ray2 = ProjectTo3D(cam2, pos2, matrix);
        var ray3 = ProjectTo3D(cam3, pos3, matrix);

        // Рассчитываем систему уравнений для пересечения лучей:
        // r1 = C1 + t1 * d1
        // r2 = C2 + t2 * d2
        // r3 = C3 + t3 * d3

        // Создаем систему линейных уравнений для t1, t2, t3
        double t1 = (ray2.Item1 - ray1.Item1) / (ray3.Item1 - ray1.Item1);  // Примерное решение для t1
        double t2 = (ray2.Item2 - ray1.Item2) / (ray3.Item2 - ray1.Item2);  // Примерное решение для t2
        double t3 = (ray2.Item3 - ray1.Item3) / (ray3.Item3 - ray1.Item3);  // Примерное решение для t3

        // Рассчитываем точку пересечения лучей
        double x = ray1.Item1 + t1 * (ray2.Item1 - ray1.Item1);
        double y = ray1.Item2 + t2 * (ray2.Item2 - ray1.Item2);
        double z = ray1.Item3 + t3 * (ray2.Item3 - ray1.Item3);

        // Возвращаем координаты шара
        return (x, y, z);
    }
}
