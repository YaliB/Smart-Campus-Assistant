import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Login.css';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    
    // Get the login function from our context
    const { login } = useContext(AuthContext);
    
    // Hook for redirecting the user after a successful login
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        // Prevent the default form submission (page reload)
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            // Attempt to log in
            await login(email, password);
            
            // If successful, redirect to the chat/dashboard page
            // Adjust the route based on your App.jsx setup TODO make a decision on the route structure
            navigate('/chat'); 
        } catch (err) {
            // Display error to the user
            setError('Login failed. Please check your credentials.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleSubmit}>
                <h2>Login</h2>
                
                {/* Conditionally render the error message */}
                {error && <div className="error-message">{error}</div>}
                
                <div className="input-group">
                    <label>Email / Username</label>
                    <input 
                        type="text" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                        disabled={isLoading}
                    />
                </div>
                
                <div className="input-group">
                    <label>Password</label>
                    <input 
                        type="password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                        disabled={isLoading}
                    />
                </div>
                
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Logging in...' : 'Login'}
                </button>
            </form>
        </div>
    );
}