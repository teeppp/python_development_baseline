'use client';

import { useState, useEffect } from 'react';
import { api, Endpoint } from '@/lib/api';

interface SidebarProps {
  onEndpointChange: (invokeEndpoint: Endpoint, streamEndpoint: Endpoint) => void;
  isStreamMode: boolean;
}

export function Sidebar({ onEndpointChange, isStreamMode }: SidebarProps) {
  const [endpoints, setEndpoints] = useState<{
    invoke: Endpoint[];
    stream: Endpoint[];
  }>({ invoke: [], stream: [] });
  const [selectedInvoke, setSelectedInvoke] = useState<string>('');
  const [selectedStream, setSelectedStream] = useState<string>('');

  useEffect(() => {
    const initializeEndpoints = async () => {
      await api.initialize();
      const availableEndpoints = api.getEndpoints();
      setEndpoints(availableEndpoints);
      
      if (availableEndpoints.invoke.length > 0) {
        setSelectedInvoke(availableEndpoints.invoke[0].path);
      }
      if (availableEndpoints.stream.length > 0) {
        setSelectedStream(availableEndpoints.stream[0].path);
      }
    };

    initializeEndpoints();
  }, []);

  useEffect(() => {
    const invokeEndpoint = endpoints.invoke.find(e => e.path === selectedInvoke);
    const streamEndpoint = endpoints.stream.find(e => e.path === selectedStream);
    
    if (invokeEndpoint && streamEndpoint) {
      onEndpointChange(invokeEndpoint, streamEndpoint);
    }
  }, [selectedInvoke, selectedStream, onEndpointChange]);

  return (
    <div className="w-64 bg-gray-50 border-r p-4 flex flex-col h-screen">
      <h2 className="text-lg font-semibold mb-4">エンドポイント設定</h2>
      
      <div className="mb-6">
        <h3 className="text-sm font-medium text-gray-700 mb-2">Invoke エンドポイント</h3>
        <div className="space-y-2">
          {endpoints.invoke.map((endpoint) => (
            <label
              key={endpoint.path}
              className={`flex items-center p-2 rounded cursor-pointer hover:bg-gray-100 ${
                selectedInvoke === endpoint.path ? 'bg-blue-50 border border-blue-200' : ''
              }`}
            >
              <input
                type="radio"
                name="invoke"
                value={endpoint.path}
                checked={selectedInvoke === endpoint.path}
                onChange={(e) => setSelectedInvoke(e.target.value)}
                className="mr-2"
              />
              <div>
                <div className="text-sm font-medium">{endpoint.name}</div>
                {endpoint.description && (
                  <div className="text-xs text-gray-500">{endpoint.description}</div>
                )}
              </div>
            </label>
          ))}
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-medium text-gray-700 mb-2">Stream エンドポイント</h3>
        <div className="space-y-2">
          {endpoints.stream.map((endpoint) => (
            <label
              key={endpoint.path}
              className={`flex items-center p-2 rounded cursor-pointer hover:bg-gray-100 ${
                selectedStream === endpoint.path ? 'bg-blue-50 border border-blue-200' : ''
              }`}
            >
              <input
                type="radio"
                name="stream"
                value={endpoint.path}
                checked={selectedStream === endpoint.path}
                onChange={(e) => setSelectedStream(e.target.value)}
                className="mr-2"
              />
              <div>
                <div className="text-sm font-medium">{endpoint.name}</div>
                {endpoint.description && (
                  <div className="text-xs text-gray-500">{endpoint.description}</div>
                )}
              </div>
            </label>
          ))}
        </div>
      </div>

      <div className="mt-auto text-xs text-gray-500">
        現在のモード: {isStreamMode ? 'ストリーミング' : '通常'}
      </div>
    </div>
  );
}