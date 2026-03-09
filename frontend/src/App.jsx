import { useState } from 'react';
import { askQuestion } from './services/api';

function App() {
  // State to store the chat history
  const [messages, setMessages] = useState([
    { text: "Hello! I am the Smart Campus Assistant. How can I help you today?", sender: "bot" }
  ]);
  
  // State to store the current input value
  const [inputValue, setInputValue] = useState('');
  
  // State to manage the loading status while waiting for the AI
  const [isLoading, setIsLoading] = useState(false);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add the user's message to the chat
    const userMessage = { text: inputValue, sender: "user" };
    setMessages((prev) => [...prev, userMessage]); // [...] is the spread operator to create a new array with the existing messages and the new one
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the FastAPI backend
      const response = await askQuestion(userMessage.text);
      
      // Add the bot's response to the chat
      setMessages((prev) => [
        ...prev, 
        { 
          text: response.answer, 
          sender: "bot", 
          category: response.category 
        }
      ]);
    } catch (error) {
      // Handle connection errors
      setMessages((prev) => [
        ...prev, 
        { text: "Sorry, I couldn't connect to the server. Please try again later.", sender: "bot" }
      ]);
    } finally {
      setIsLoading(false); // Reset loading state regardless of success or failure
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-area">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
            {/* Display category if it's a bot message and has a category */}
            {msg.sender === 'bot' && msg.category && (
              <span className="category-tag">Category: {msg.category}</span>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <p>Thinking...</p>
          </div>
        )}
      </div>
      
      <form className="input-area" onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask about schedules, rooms, etc..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}

export default App;