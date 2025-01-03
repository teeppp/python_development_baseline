'use client';

import { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '@/components/ChatMessage';
import { ChatInput } from '@/components/ChatInput';
import { Sidebar } from '@/components/Sidebar';
import { Message } from '@/types/chat';
import { api, Endpoint } from '@/lib/api';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreamMode, setIsStreamMode] = useState(true);
  const [currentInvokeEndpoint, setCurrentInvokeEndpoint] = useState<Endpoint>();
  const [currentStreamEndpoint, setCurrentStreamEndpoint] = useState<Endpoint>();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleEndpointChange = (invokeEndpoint: Endpoint, streamEndpoint: Endpoint) => {
    setCurrentInvokeEndpoint(invokeEndpoint);
    setCurrentStreamEndpoint(streamEndpoint);
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const assistantMessage: Message = {
        id: `${Date.now()}-assistant`,
        content: '',
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      if (isStreamMode) {
        await api.streamMessage(content, (chunk) => {
          setMessages((prev) => {
            const lastMessage = prev[prev.length - 1];
            if (lastMessage.role === 'assistant') {
              return [
                ...prev.slice(0, -1),
                {
                  ...lastMessage,
                  content: lastMessage.content + chunk,
                },
              ];
            }
            return prev;
          });
        }, currentStreamEndpoint);
      } else {
        const response = await api.sendMessage(content, currentInvokeEndpoint);
        setMessages((prev) => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage.role === 'assistant') {
            return [
              ...prev.slice(0, -1),
              {
                ...lastMessage,
                content: response.response,
              },
            ];
          }
          return prev;
        });
      }
    } catch (error) {
      console.error('Error in chat:', error);
      setMessages((prev) => [
        ...prev,
        {
          id: `${Date.now()}-error`,
          content: 'メッセージの送信中にエラーが発生しました。もう一度お試しください。',
          role: 'assistant',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen">
      <Sidebar onEndpointChange={handleEndpointChange} isStreamMode={isStreamMode} />
      
      <main className="flex-1 flex flex-col bg-gray-50">
        <div className="border-b bg-white p-4">
          <div className="max-w-3xl mx-auto flex items-center justify-between">
            <h1 className="text-xl font-semibold">チャット</h1>
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">ストリーミングモード</span>
              <button
                onClick={() => setIsStreamMode(!isStreamMode)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                  isStreamMode ? 'bg-blue-500' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    isStreamMode ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          <div className="max-w-3xl mx-auto space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 mt-8">
                メッセージを入力してチャットを開始してください
              </div>
            )}
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>

        <div className="border-t bg-white">
          <div className="max-w-3xl mx-auto p-4">
            <ChatInput onSend={handleSendMessage} disabled={isLoading} />
          </div>
        </div>
      </main>
    </div>
  );
}
