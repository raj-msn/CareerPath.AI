import React, { useState, useEffect, useRef } from 'react';
import type { FormEvent } from 'react'; // Import FormEvent as a type
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './ChatInterface.css'; // We will create this file for styling

interface Message {
  sender: 'user' | 'ai';
  text: string;
  isSystem?: boolean; // To hide the initial auto-sent message
}

// Helper to generate a simple UUID for session tracking
const generateSessionId = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

const ChatInterface: React.FC = () => {
  const [sessionId, setSessionId] = useState<string>('');
  const [input, setInput] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const initialMessageSentRef = useRef(false); // To track if initial message was sent
  const messagesEndRef = useRef<null | HTMLDivElement>(null); // For auto-scrolling

  useEffect(() => {
    const newSessionId = generateSessionId();
    setSessionId(newSessionId);
  }, []);

  useEffect(() => {
    // Send initial message once sessionId is set and initial message hasn't been sent
    if (sessionId && !initialMessageSentRef.current) {
      initialMessageSentRef.current = true; // Mark as sent
      setIsLoading(true);

      // This is the automatic initial message to kickstart the AI's greeting
      // It won't be displayed as a user message in the UI
      const initialUserMessage = "Hello"; 

      axios.post('http://localhost:8000/chat', {
        session_id: sessionId,
        message: initialUserMessage, 
      })
      .then(response => {
        const aiMessageText = response.data.reply;
        if (aiMessageText) {
          const aiMessage: Message = { sender: 'ai', text: aiMessageText };
          setMessages(prevMessages => [...prevMessages, aiMessage]);
        }
      })
      .catch(error => {
        console.error('Error sending initial message:', error);
        const errorMessage: Message = { sender: 'ai', text: 'Sorry, I encountered an error starting the chat. Please refresh.' };
        setMessages(prevMessages => [...prevMessages, errorMessage]);
      })
      .finally(() => {
        setIsLoading(false);
      });
    }
  }, [sessionId]); // This effect runs when sessionId changes

  useEffect(() => {
    // Scroll to the bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !sessionId) return;

    const userMessage: Message = { sender: 'user', text: input };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        session_id: sessionId,
        message: input,
      });

      const aiMessageText = response.data.reply;
      if (aiMessageText) {
        const aiMessage: Message = { sender: 'ai', text: aiMessageText };
        setMessages(prevMessages => [...prevMessages, aiMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = { sender: 'ai', text: 'Sorry, I encountered an error. Please try again.' };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="message-area">
        {messages.map((msg, index) => (
          // Do not render system messages if any were accidentally added to visible messages
          !msg.isSystem && (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.sender === 'ai' ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.text}
                </ReactMarkdown>
              ) : (
                <p>{msg.text}</p>
              )}
            </div>
          )
        ))}
        {isLoading && messages.length === 0 && <div className="message ai"><p><i>Connecting to AI advisor...</i></p></div>}
        {isLoading && messages.length > 0 && <div className="message ai"><p><i>AI is thinking...</i></p></div>}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask your career advisor..."
          disabled={isLoading || !sessionId || !initialMessageSentRef.current} // Disable until initial greeting is loaded
        />
        <button type="submit" disabled={isLoading || !sessionId || !initialMessageSentRef.current}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface; 