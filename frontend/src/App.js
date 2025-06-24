import React, { useState, useEffect } from 'react';
import { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';
import ChatInterface from './components/ChatInterface';
import CareerRoadmapFlow from './components/CareerRoadmapFlow';
import { careerAPI } from './services/api';
import { AlertCircle, CheckCircle, Wifi, WifiOff } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentLearningPath, setCurrentLearningPath] = useState(null);
  const [currentResources, setCurrentResources] = useState(null);
  const [backendStatus, setBackendStatus] = useState('unknown');
  const [error, setError] = useState(null);

  // Check backend connection on component mount
  useEffect(() => {
    checkBackendHealth();
  }, []);

  // Debug: Monitor learning path state changes
  useEffect(() => {
    console.log('🗺️ FRONTEND: Learning path state changed to:', currentLearningPath ? 'has data' : 'empty');
  }, [currentLearningPath]);

  const checkBackendHealth = async () => {
    try {
      await careerAPI.testConnection();
      setBackendStatus('connected');
    } catch (error) {
      setBackendStatus('disconnected');
      console.error('Backend connection failed:', error);
    }
  };

  const handleSendMessage = async (message) => {
    if (isLoading) return;

    // Add user message to chat
    const userMessage = { type: 'user', content: message, timestamp: Date.now() };
    setMessages(prev => [...prev, userMessage]);
    
    setIsLoading(true);
    setError(null);

    try {
      console.log('🚀 FRONTEND: Sending message to API:', message);
      
      // Prepare conversation context (last 6 messages for context)
      const conversationHistory = messages.slice(-6).map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }));
      
      // Include current learning path as part of context
      const contextData = {
        conversation_history: conversationHistory,
        current_learning_path: currentLearningPath,
        is_follow_up: messages.length > 0 // True if this isn't the first message
      };
      
      console.log('🧠 FRONTEND: Sending context:', {
        history_length: conversationHistory.length,
        has_existing_path: !!currentLearningPath,
        is_follow_up: contextData.is_follow_up
      });
      
      // Call the career planning API with context
      const response = await careerAPI.chat(message, contextData);
      
      console.log('📦 FRONTEND: Received API response:', response);
      console.log('🗺️ FRONTEND: Learning path in response:', response.data?.learning_path);
      
      // Add AI response to chat
      const aiMessage = { 
        type: 'ai', 
        content: response.response || 'I received your message and am processing it.',
        timestamp: Date.now() 
      };
      setMessages(prev => [...prev, aiMessage]);

      // Update learning path if available
      if (response.data?.learning_path) {
        console.log('🎯 FRONTEND: Updating learning path with new data:', response.data.learning_path);
        setCurrentLearningPath(response.data.learning_path);
      } else {
        console.log('⚠️ FRONTEND: No learning path in response - keeping existing path');
      }

      // Update resources if available
      if (response.data?.resources) {
        console.log('📚 FRONTEND: Updating resources with new data:', response.data.resources);
        setCurrentResources(response.data.resources);
      }

      // Update backend status to connected if successful
      setBackendStatus('connected');

    } catch (error) {
      console.error('❌ FRONTEND: Error sending message:', error);
      setError(error.message);
      
      // Add error message to chat
      const errorMessage = { 
        type: 'ai', 
        content: `Sorry, I encountered an error: ${error.message}. Please make sure the backend is running and try again.`,
        timestamp: Date.now() 
      };
      setMessages(prev => [...prev, errorMessage]);

      // Update backend status
      setBackendStatus('disconnected');
    } finally {
      setIsLoading(false);
    }
  };

  const renderStatusBar = () => {
    const statusConfig = {
      connected: {
        icon: <Wifi className="w-4 h-4" />,
        text: 'Connected',
        bgColor: 'bg-green-100',
        textColor: 'text-green-800',
        borderColor: 'border-green-200'
      },
      disconnected: {
        icon: <WifiOff className="w-4 h-4" />,
        text: 'Backend Disconnected',
        bgColor: 'bg-red-100',
        textColor: 'text-red-800',
        borderColor: 'border-red-200'
      },
      unknown: {
        icon: <AlertCircle className="w-4 h-4" />,
        text: 'Checking Connection...',
        bgColor: 'bg-yellow-100',
        textColor: 'text-yellow-800',
        borderColor: 'border-yellow-200'
      }
    };

    const config = statusConfig[backendStatus];

    return (
      <div className={`flex items-center justify-between px-4 py-2 border-b ${config.borderColor} ${config.bgColor}`}>
        <div className={`flex items-center space-x-2 ${config.textColor}`}>
          {config.icon}
          <span className="text-sm font-medium">{config.text}</span>
        </div>
        
        {backendStatus === 'disconnected' && (
          <button
            onClick={checkBackendHealth}
            className="text-sm px-3 py-1 bg-red-200 hover:bg-red-300 rounded-md transition-colors"
          >
            Retry
          </button>
        )}
        
        {backendStatus === 'connected' && (
          <div className="flex items-center space-x-1 text-green-700">
            <CheckCircle className="w-4 h-4" />
            <span className="text-sm">Multi-Agent System Ready</span>
          </div>
        )}
      </div>
    );
  };

  return (
    <ReactFlowProvider>
      <div className="h-screen bg-gray-50 flex flex-col">
        {/* Status Bar */}
        {renderStatusBar()}

        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Chat Interface */}
          <div className="w-1/2 border-r border-gray-300 flex flex-col">
            <ChatInterface
              messages={messages}
              isLoading={isLoading}
              onSendMessage={handleSendMessage}
            />
          </div>

          {/* Visualization Panel */}
          <div className="w-1/2 flex flex-col bg-gray-50">
            {/* Header */}
            <div className="flex-shrink-0 bg-white border-b border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-gray-800">Career Roadmap</h2>
                  <p className="text-sm text-gray-600">Visual representation of your career path</p>
                </div>
                <div className="text-2xl">🗺️</div>
              </div>
            </div>

            {/* Diagram Area */}
            <div className="flex-1 p-4 overflow-auto">
              <CareerRoadmapFlow 
                learningPath={currentLearningPath}
                resources={currentResources}
                className="w-full h-full rounded-lg border border-gray-200"
              />
            </div>

            {/* Footer Info */}
            <div className="flex-shrink-0 bg-white border-t border-gray-200 p-3">
              <div className="text-xs text-gray-500 text-center">
                {currentLearningPath ? (
                  <span className="flex items-center justify-center space-x-1">
                    <CheckCircle className="w-3 h-3 text-green-500" />
                    <span>Interactive roadmap loaded</span>
                  </span>
                ) : (
                  <span className="text-gray-400">Send a message to generate your career roadmap</span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Error Toast */}
        {error && (
          <div className="fixed bottom-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-5 h-5" />
              <span>{error}</span>
              <button 
                onClick={() => setError(null)}
                className="ml-2 text-red-200 hover:text-white"
              >
                ×
              </button>
            </div>
          </div>
        )}
      </div>
    </ReactFlowProvider>
  );
}

export default App; 