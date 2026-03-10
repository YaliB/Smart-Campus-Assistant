import { useState } from 'react';
import { askQuestion } from '../services/api';
import './Chat.css'; // We will create this file next

export default function Chat() {
  // State for chat history
  const [messages, setMessages] = useState([
    { text: "Hello! I am the Smart Campus Assistant. How can I help you today?", sender: "bot" }
  ]);
  
  // State for input field
  const [inputValue, setInputValue] = useState('');
  
  // State for loading indicator
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = { text: inputValue, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Calling the unified api service
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