import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Send, Loader2, User, Bot } from 'lucide-react';

const ChatInterface = ({ onSendMessage, isLoading, messages = [] }) => {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const message = inputMessage.trim();
    setInputMessage('');
    
    try {
      await onSendMessage(message);
    } catch (error) {
      console.error('Error sending message:', error);
    }
    
    // Focus back on input
    inputRef.current?.focus();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const renderMessage = (message, index) => {
    const isUser = message.type === 'user';
    const isAI = message.type === 'ai';

    return (
      <div key={index} className={`flex mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
        <div className={`message-bubble ${isUser ? 'user' : 'ai'}`}>
          {/* Follow-up indicator for AI messages */}
          {isAI && index > 0 && (
            <div className="text-xs text-gray-500 mb-2 flex items-center">
              <div className="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
              Continuing our conversation...
            </div>
          )}
          
          {isAI ? (
            <div className="markdown-content">
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  // Custom styling for markdown elements
                  h1: ({children}) => <h1 className="text-xl font-bold mb-2 text-gray-800">{children}</h1>,
                  h2: ({children}) => <h2 className="text-lg font-semibold mb-2 text-gray-700">{children}</h2>,
                  h3: ({children}) => <h3 className="text-md font-medium mb-1 text-gray-600">{children}</h3>,
                  p: ({children}) => <p className="mb-2 leading-relaxed">{children}</p>,
                  strong: ({children}) => <strong className="font-semibold text-gray-800">{children}</strong>,
                  em: ({children}) => <em className="italic text-gray-700">{children}</em>,
                  ul: ({children}) => <ul className="list-disc pl-4 mb-2 space-y-1">{children}</ul>,
                  ol: ({children}) => <ol className="list-decimal pl-4 mb-2 space-y-1">{children}</ol>,
                  li: ({children}) => <li className="text-gray-700">{children}</li>,
                  code: ({children}) => (
                    <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono text-gray-800">
                      {children}
                    </code>
                  ),
                  pre: ({children}) => (
                    <pre className="bg-gray-100 p-3 rounded-lg overflow-x-auto mb-2">
                      {children}
                    </pre>
                  ),
                  blockquote: ({children}) => (
                    <blockquote className="border-l-4 border-primary-300 pl-4 italic text-gray-600 mb-2">
                      {children}
                    </blockquote>
                  ),
                  a: ({href, children}) => (
                    <a 
                      href={href} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:text-primary-700 underline"
                    >
                      {children}
                    </a>
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          ) : (
            message.content
          )}
        </div>
      </div>
    );
  };

  const renderTypingIndicator = () => (
    <div className="flex justify-start mb-4">
      <div className="message-bubble ai">
        <div className="flex items-center space-x-2">
          <div className="loading-dots">
            <div style={{'--i': 0}}></div>
            <div style={{'--i': 1}}></div>
            <div style={{'--i': 2}}></div>
          </div>
          <span className="text-sm text-gray-600">AI agents are analyzing your career path...</span>
        </div>
      </div>
    </div>
  );

  const hasMessages = messages.length > 0;

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="flex-shrink-0 bg-gradient-to-r from-primary-500 to-primary-600 text-white p-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-semibold">CareerPath.AI</h2>
            <p className="text-sm text-primary-100">Multi-Agent Career Planning Assistant</p>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        {!hasMessages && (
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Bot className="w-8 h-8 text-primary-500" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Welcome to CareerPath.AI! 🚀
            </h3>
            <p className="text-gray-600 mb-4">
              I'm your AI-powered career planning assistant with specialized agents to help you:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-md mx-auto text-sm">
              <div className="bg-blue-50 p-3 rounded-lg">
                <strong>🎯 Skills Analysis</strong><br />
                Identify your strengths and skill gaps
              </div>
              <div className="bg-green-50 p-3 rounded-lg">
                <strong>📊 Industry Research</strong><br />
                Get market insights and trends
              </div>
              <div className="bg-purple-50 p-3 rounded-lg">
                <strong>🛤️ Learning Paths</strong><br />
                Create personalized roadmaps
              </div>
              <div className="bg-orange-50 p-3 rounded-lg">
                <strong>📚 Resources</strong><br />
                Find courses and certifications
              </div>
            </div>
            <p className="text-gray-500 mt-4 text-sm">
              Try: "I want to transition from software engineer to senior software engineer"
            </p>
          </div>
        )}

        {messages.map(renderMessage)}
        {isLoading && renderTypingIndicator()}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="flex-shrink-0 border-t border-gray-200 p-4">
        <form onSubmit={handleSubmit} className="flex space-x-3">
          <div className="flex-1">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Describe your career goals or ask about your next steps..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows="2"
              disabled={isLoading}
            />
          </div>
          <button
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            className="flex-shrink-0 bg-primary-500 text-white px-6 py-3 rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </form>
        
        <div className="mt-2 text-xs text-gray-500 text-center">
          Press Enter to send • Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 