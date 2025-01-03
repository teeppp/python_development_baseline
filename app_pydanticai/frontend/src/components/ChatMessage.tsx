import { Message } from '@/types/chat';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`relative max-w-[80%] rounded-lg px-4 py-2 ${
          isUser
            ? 'bg-blue-500 text-white'
            : 'bg-white text-gray-900 border border-gray-200'
        }`}
      >
        {!isUser && (
          <div className="absolute -left-2 top-2 w-4 h-4 transform rotate-45 bg-white border-l border-t border-gray-200" />
        )}
        {isUser && (
          <div className="absolute -right-2 top-2 w-4 h-4 transform rotate-45 bg-blue-500" />
        )}
        <div className="relative">
          <p className="text-sm whitespace-pre-wrap break-words">{message.content}</p>
          <p className="text-xs mt-1 opacity-70">
            {message.timestamp.toLocaleTimeString()}
          </p>
        </div>
      </div>
    </div>
  );
}