'use client';

import { occurEarthQuake } from '@/api/occurEarthQuake';
import { useState } from 'react';

type Location = 'niigata' | 'tokyo';

export default function EarthquakePage() {
  const [isShaking, setIsShaking] = useState(false);
  const [intensity, setIntensity] = useState(0);
  const [location, setLocation] = useState<Location>('tokyo');

  const triggerEarthquake = (level: number) => {
    setIntensity(level);
    setIsShaking(true);
    setTimeout(() => {
      setIsShaking(false);
    }, 1000);
  };

  const getLocationName = (loc: Location) => {
    return loc === 'niigata' ? '新潟' : '東京';
  };

  const handleOccurEarthQuake = async () => {
    const response = await occurEarthQuake();
    console.log(response);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className={`space-y-4 ${isShaking ? 'animate-shake' : ''}`}>
        <h1 className="text-3xl font-bold text-center mb-8">地震シミュレーター</h1>

        <div className="flex space-x-4 mb-6">
          <button
            onClick={() => setLocation('tokyo')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              location === 'tokyo'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            東京
          </button>
          <button
            onClick={() => setLocation('niigata')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              location === 'niigata'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            新潟
          </button>
        </div>

        <div className="space-y-4">
          <button
            onClick={handleOccurEarthQuake}
            className="px-6 py-3 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors w-full"
          >
            {getLocationName(location)}で震度3の地震を起こす
          </button>
          <button
            onClick={handleOccurEarthQuake}
            className="px-6 py-3 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors w-full"
          >
            {getLocationName(location)}で震度7の地震を起こす
          </button>
        </div>
      </div>
    </div>
  );
}
