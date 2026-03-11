import { useState, useRef, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { askQuestion } from '../services/api';
import { AuthContext } from '../context/AuthContext';
import './Chat.css';

export default function Chat() {
  const [messages, setMessages] = useState([
    { text: "Hello! I am the Smart Campus Assistant. How can I help you today?", sender: "bot" }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const MAX_CHARS = 500;

  const messagesEndRef = useRef(null);
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = { text: inputValue, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await askQuestion(userMessage.text);
      
      setMessages((prev) => [
        ...prev, 
        { 
          text: response.answer, 
          sender: "bot", 
          category: response.category 
        }
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev, 
        { text: "Sorry, I couldn't connect to the server. Please try again later.", sender: "bot" }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="header-title">
            <span className="header-icon emoji-symbol">🎓</span>
            <h2>Smart Campus Assistant</h2>
        </div>
        <div className="header-actions">
          {user && user.is_admin && (
              <button onClick={() => navigate('/dashboard')} className="dashboard-button">
                Dashboard
              </button>
          )}
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </div>

      {/* Messages Area */}
      <div className="messages-area">
        {messages.map((msg, index) => (
          <div key={index} className={`message-wrapper ${msg.sender}`}>
            <div className="message-avatar emoji-symbol">
                {msg.sender === 'bot' ? '🤖' : '👤'}
            </div>
            <div className={`message-content ${msg.sender}`}>
                <span className="sender-name">
                    {msg.sender === 'bot' ? 'Campus AI' : 'You'}
                </span>
                <div className="message-bubble">
                    <p dir="auto">{msg.text}</p>
                    {msg.sender === 'bot' && msg.category && (
                    <span className="category-tag">{msg.category}</span>
                    )}
                </div>
            </div>
          </div>
        ))}
        
        {/* Typing Indicator */}
        {isLoading && (
          <div className="message-wrapper bot">
             <div className="message-avatar emoji-symbol">🤖</div>
             <div className="message-content bot">
                 <span className="sender-name">Campus AI</span>
                 <div className="message-bubble typing-indicator">
                    <span></span><span></span><span></span>
                 </div>
             </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Area */}
      <div className="input-section">
          <form className="input-area" onSubmit={handleSubmit}>
            <input 
              type="text" 
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask me anything about the campus..."
              disabled={isLoading}
              maxLength={MAX_CHARS}
              dir="auto" 
            />
            <button type="submit" disabled={isLoading || !inputValue.trim()} aria-label="send">
              <svg viewBox="0 0 24 24" fill="currentColor" className="send-icon"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path></svg>
            </button>
          </form>
          <div className={`char-counter ${inputValue.length >= MAX_CHARS ? 'limit-reached' : ''}`}>
              {inputValue.length}/{MAX_CHARS}
          </div>
      </div>
    </div>
  );
}