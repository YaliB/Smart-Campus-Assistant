import axios from 'axios';

// Create an Axios instance with the base URL of your FastAPI backend
const api = axios.create({
    //TODO add env variable for this
    baseURL: 'http://localhost:8000', // Base URL for all requests
});

// Interceptor to inject the JWT token into requests automatically
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Intercept responses to catch 401 Unauthorized errors globally
api.interceptors.response.use(
    (response) => {
        // If the request succeeds, just return the response
        return response;
    },
    (error) => {
        // If the server returns a 401 Unauthorized (e.g., token expired or invalid)
        if (error.response && error.response.status === 401) {
            console.warn("Token expired or invalid. Redirecting to login...");
            // 1. Clear the invalid credentials from storage
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            // 2. Force a redirect to the login page
            // Note: window.location.href is used here because we are outside a React component 
            window.location.href = '/login';
        }
        // Reject the promise so the component's catch block can still run if needed
        return Promise.reject(error);
    }
);

/**
 * Sends a question to the backend AI service.
 * @param {string} question - The student's question.
 * @returns {Promise<Object>} - The response data containing 'answer' and 'category'.
 */
export const askQuestion = async (question) => {
    try {
        // We use api.post, and since baseURL is already set, we just add the relative route
        const response = await api.post('/api/ask', { question });
        return response.data;
    } catch (error) {
        console.error("Error communicating with the backend:", error);
        throw error;
    }
};

// Export the instance as default for AuthContext and other services
export default api;