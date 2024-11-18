import { useState } from 'react';

const App = () => {
  const [isPlaying, setIsPlaying] = useState(false);  // Начальное состояние - "остановлено"
  const [streamUrl, setStreamUrl] = useState('');  // Состояние для хранения URL потока

  const toggleStream = async () => {
    const action = isPlaying ? 'stop' : 'start';

    try {
      console.log(action);
      const response = await fetch('http://192.168.126.209:8000/control', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action }),
      });

      const result = await response.json();
      if (result.status) {
        setIsPlaying(prevState => !prevState);  // Переключаем состояние воспроизведения

        // Если поток запускается, обновляем URL (для перезагрузки потока)
        if (!isPlaying) {
          setStreamUrl(`http://192.168.126.209:8000/stream?time=${Date.now()}`);  // Добавляем уникальный параметр времени
        }
      }
    } catch (error) {
      console.error('Error toggling stream:', error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center w-full h-screen bg-gray-800 text-white">
      <button
        onClick={toggleStream}
        className="px-4 py-2 bg-blue-500 rounded-md hover:bg-blue-700"
      >
        {isPlaying ? 'Stop' : 'Start'}
      </button>
      
      {isPlaying && (
        <img src={streamUrl} alt="Video Stream" />
      )}
    </div>
  );
};

export default App;