import React, { createContext, useState, useEffect } from 'react';
import api from '../services/api';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('token') || null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (token) {
            setUser({ isAuthenticated: true });
        } else {
            setUser(null);
        }
        setIsLoading(false);
    }, [token]);

    const login = async (email, password) => {
        try {
            // Create URLSearchParams to send data as application/x-www-form-urlencoded
            const formData = new URLSearchParams();
            // FastAPI's OAuth2PasswordRequestForm specifically looks for 'username'
            formData.append('username', email); 
            formData.append('password', password);

            // Note: route is based on main.py routers setup
            const response = await api.post('/api/admin/login', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
            
            const { access_token } = response.data;
            
            setToken(access_token);
            localStorage.setItem('token', access_token);
            setUser({ email }); 
            
            return true;
        } catch (error) {
            console.error("Login failed:", error);
            throw error;
        }
    };

    const logout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('token');
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};