import axios from 'axios';

// Define the base URL for the FastAPI backend
const API_URL = 'http://localhost:8000/api';

/**
 * Sends a question to the backend AI service.
 * @param {string} question - The student's question.
 * @returns {Promise<Object>} - The response data containing 'answer' and 'category'.
 */
export const askQuestion = async (question) => {
    try {
        // Send a POST request matching the backend AskRequest schema
        const response = await axios.post(`${API_URL}/ask`, { question });
        return response.data;
    } catch (error) {
        console.error("Error communicating with the backend:", error);
        throw error;
    }
};