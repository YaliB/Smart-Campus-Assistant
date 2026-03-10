import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './context/AuthContext';
import Login from './pages/Login';
import Chat from './pages/Chat'; // Import the new Chat component

// ProtectedRoute checks if the user is logged in
const ProtectedRoute = ({ children }) => {
    const { token, isLoading } = useContext(AuthContext);

    if (isLoading) return <div>Loading...</div>;

    if (!token) {
        return <Navigate to="/login" replace />;
    }

    return children;
};

function App() {
    return (
        <Router>
            <Routes>
                {/* Login Route */}
                <Route path="/login" element={<Login />} />

                {/* Protected Chat Route */}
                <Route 
                    path="/chat" 
                    element={
                        <ProtectedRoute>
                            <Chat />
                        </ProtectedRoute>
                    } 
                />

                {/* Default redirect to chat */}
                <Route path="*" element={<Navigate to="/chat" replace />} />
            </Routes>
        </Router>
    );
}

export default App;