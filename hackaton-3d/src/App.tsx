import { useState } from 'react';

function App() {
  const [isPlaying, setIsPlaying] = useState(false);

  return (
    <div className='flex flex-col gap-3 w-full h-full p-6 items-center bg-gray-900'>
      <button 
        onClick={() => setIsPlaying(p => !p)}
        className='p-2 border border-gray-600 rounded-lg'
      >
        {isPlaying ? 'Stop' : 'Play'}
      </button>
      <img src="http://192.168.1.6:8000/stream" alt="Video Stream" />
    </div>
  );
}

export default App;
