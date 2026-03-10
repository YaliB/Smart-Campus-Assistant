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