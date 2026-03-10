import React, { createContext, useState, useEffect } from 'react';
import api from '../services/api';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    // Initialize user state from localStorage if it exists
    const [user, setUser] = useState(() => {
        const savedUser = localStorage.getItem('user');
        return savedUser ? JSON.parse(savedUser) : null;
    });
    const [token, setToken] = useState(localStorage.getItem('token') || null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        setIsLoading(false);
    }, [token]);

    const login = async (email, password) => {
        try {
            const formData = new URLSearchParams();
            formData.append('username', email); 
            formData.append('password', password);

            const response = await api.post('/api/admin/login', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
            
            // Destructure both the token AND the user object from the response
            const { access_token, user: userData } = response.data;
            
            // Save token
            setToken(access_token);
            localStorage.setItem('token', access_token);
            
            // Save the real user data from the DB
            setUser(userData);
            localStorage.setItem('user', JSON.stringify(userData));
            
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
        localStorage.removeItem('user');
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};