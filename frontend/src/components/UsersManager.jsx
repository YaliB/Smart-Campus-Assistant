import { useState, useEffect } from 'react';
import api from '../services/api';

export default function UsersManager() {
    const [users, setUsers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    // State for creating a new user
    const [newEmail, setNewEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [newStudentId, setNewStudentId] = useState('');

    // State for editing an existing user
    const [editingUserId, setEditingUserId] = useState(null);
    const [editEmail, setEditEmail] = useState('');
    const [editStudentId, setEditStudentId] = useState('');

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            setIsLoading(true);
            const response = await api.get('/api/admin/users');
            setUsers(response.data);
            setError('');
        } catch (err) {
            console.error("Failed to fetch users", err);
            setError('Failed to load users. Please check your connection.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreateUser = async (e) => {
        e.preventDefault();
        try {
            await api.post('/api/admin/users', { 
                email: newEmail, 
                password: newPassword,
                student_id: newStudentId ? newStudentId : null
            });
            
            // Clear form and refresh
            setNewEmail('');
            setNewPassword('');
            setNewStudentId('');
            fetchUsers();
        } catch (err) {
            console.error("Failed to create user", err);
            alert("Error creating user. Check if email already exists.");
        }
    };

    const handleDeleteUser = async (userId) => {
        if (!window.confirm("Are you sure you want to delete this user?")) return;
        try {
            await api.delete(`/api/admin/users/${userId}`);
            fetchUsers();
        } catch (err) {
            console.error("Failed to delete user", err);
            alert("Error deleting user.");
        }
    };

    // --- Editing Logic ---
    const startEditing = (user) => {
        setEditingUserId(user.id);
        setEditEmail(user.email);
        setEditStudentId(user.student_id || '');
    };

    const cancelEditing = () => {
        setEditingUserId(null);
        setEditEmail('');
        setEditStudentId('');
    };

    const handleSaveEdit = async (userId) => {
        try {
            await api.put(`/api/admin/users/${userId}`, {
                email: editEmail,
                student_id: editStudentId ? editStudentId : null
            });
            setEditingUserId(null);
            fetchUsers();
        } catch (err) {
            console.error("Failed to update user", err);
            alert("Error updating user.");
        }
    };

    return (
        <div className="manager-container">
            <h2>User Management</h2>
            {error && <div className="error-message">{error}</div>}

            {/* Create User Form */}
            <div className="create-form-card">
                <h3>Add New User</h3>
                <form onSubmit={handleCreateUser} className="inline-form">
                    <input 
                        type="email" 
                        placeholder="Email" 
                        value={newEmail} 
                        onChange={(e) => setNewEmail(e.target.value)} 
                        required 
                    />
                    <input 
                        type="password" 
                        placeholder="Password" 
                        value={newPassword} 
                        onChange={(e) => setNewPassword(e.target.value)} 
                        required 
                    />
                    <input 
                        type="text" 
                        placeholder="Student ID (Optional)" 
                        value={newStudentId} 
                        onChange={(e) => setNewStudentId(e.target.value)} 
                    />
                    <button type="submit">Create</button>
                </form>
            </div>

            {/* Users Table */}
            <div className="table-container">
                {isLoading ? (
                    <p>Loading users...</p>
                ) : (
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Email</th>
                                <th>Student ID</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map(user => (
                                <tr key={user.id}>
                                    <td>{user.id}</td>
                                    
                                    {/* Conditional Rendering: Edit Mode vs View Mode */}
                                    {editingUserId === user.id ? (
                                        <>
                                            <td>
                                                <input 
                                                    type="email" 
                                                    value={editEmail} 
                                                    onChange={(e) => setEditEmail(e.target.value)} 
                                                    className="edit-input"
                                                />
                                            </td>
                                            <td>
                                                <input 
                                                    type="text" 
                                                    value={editStudentId} 
                                                    onChange={(e) => setEditStudentId(e.target.value)} 
                                                    className="edit-input"
                                                />
                                            </td>
                                            <td>
                                                <button className="save-btn" onClick={() => handleSaveEdit(user.id)}>Save</button>
                                                <button className="cancel-btn" onClick={cancelEditing}>Cancel</button>
                                            </td>
                                        </>
                                    ) : (
                                        <>
                                            <td>{user.email}</td>
                                            <td>{user.student_id || '-'}</td>
                                            <td>
                                                <button className="edit-btn" onClick={() => startEditing(user)}>Edit</button>
                                                <button className="delete-btn" onClick={() => handleDeleteUser(user.id)}>Delete</button>
                                            </td>
                                        </>
                                    )}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
}