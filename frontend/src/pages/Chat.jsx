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

  // Setup refs and context for auto-scroll and logout
  const messagesEndRef = useRef(null);
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  // Auto-scroll function
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Trigger auto-scroll whenever messages or loading state change
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Logout handler
  const handleLogout = () => {
    logout(); // Clears the token from state and localStorage
    navigate('/login'); // Redirects back to the login page
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
      {/* Header with Logout Button */}
      <div className="chat-header">
        <h2>Smart Campus Assistant</h2>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </div>

      <div className="messages-area">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
            {msg.sender === 'bot' && msg.category && (
              <span className="category-tag">{msg.category}</span>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message bot typing">
            <p>AI is typing...</p>
          </div>
        )}
        {/* Invisible div used as an anchor for scrolling */}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="input-area" onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask me anything about the campus..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}