import { useState, useEffect } from 'react';
import api from '../services/api';

// Import the custom hook for table features 
import { useTableFeatures } from '../hooks/useTableFeatures';

export default function UsersManager() {
    const [users, setUsers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const [newUsername, setNewUsername] = useState(''); 
    const [newPassword, setNewPassword] = useState('');
    const [newStudentId, setNewStudentId] = useState('');
    const [newIsAdmin, setNewIsAdmin] = useState(false);

    const [editingUserId, setEditingUserId] = useState(null);
    const [editUsername, setEditUsername] = useState(''); 
    const [editPassword, setEditPassword] = useState('');
    const [editStudentId, setEditStudentId] = useState('');
    const [editIsAdmin, setEditIsAdmin] = useState(false);

    // Use the hook! Pass the data and tell it which fields to search in
    const { 
        searchTerm, 
        setSearchTerm, 
        handleSort, 
        renderSortArrow, 
        processedData: sortedUsers 
    } = useTableFeatures(users, ['email', 'student_id']);

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
            setError('Failed to load users.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreateUser = async (e) => {
        e.preventDefault();
        try {
            await api.post('/api/admin/users', { 
                email: newUsername, 
                password: newPassword,
                student_id: newStudentId ? newStudentId : null,
                is_admin: newIsAdmin
            });
            
            setNewUsername('');
            setNewPassword('');
            setNewStudentId('');
            setNewIsAdmin(false);
            fetchUsers();
        } catch (err) {
            alert("Error creating user.");
        }
    };

    const handleDeleteUser = async (userId) => {
        if (!window.confirm("Are you sure?")) return;
        try {
            await api.delete(`/api/admin/users/${userId}`);
            fetchUsers();
        } catch (err) {
            alert("Error deleting user.");
        }
    };

    const startEditing = (user) => {
        setEditingUserId(user.id);
        setEditUsername(user.email); 
        setEditPassword(''); 
        setEditStudentId(user.student_id || '');
        setEditIsAdmin(user.is_admin);
    };

    const cancelEditing = () => {
        setEditingUserId(null);
        setEditUsername('');
        setEditPassword('');
        setEditStudentId('');
        setEditIsAdmin(false);
    };

    const handleSaveEdit = async (userId) => {
        try {
            const payload = {
                email: editUsername, 
                student_id: editStudentId ? editStudentId : null,
                is_admin: editIsAdmin
            };
            if (editPassword.trim() !== '') payload.password = editPassword;

            await api.patch(`/api/admin/users/${userId}`, payload);
            setEditingUserId(null);
            fetchUsers();
        } catch (err) {
            alert("Error updating user.");
        }
    };

    return (
        <div className="manager-container">
            <h2>User Management</h2>
            {error && <div className="error-message">{error}</div>}

            <div className="create-form-card">
                <h3>Add New User</h3>
                <form onSubmit={handleCreateUser} className="inline-form">
                    <input type="text" placeholder="Email / Username" value={newUsername} onChange={(e) => setNewUsername(e.target.value)} required />
                    <input type="password" placeholder="Password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
                    <input type="text" placeholder="Student ID (Optional)" value={newStudentId} onChange={(e) => setNewStudentId(e.target.value)} />
                    <label className="checkbox-label">
                        <input type="checkbox" checked={newIsAdmin} onChange={(e) => setNewIsAdmin(e.target.checked)} /> Admin
                    </label>
                    <button type="submit">Create</button>
                </form>
            </div>

            <div className="table-container">
                <div className="search-bar-container">
                    <input 
                        type="text" 
                        placeholder="Search Email / Username or Student ID..." 
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="search-input"
                    />
                </div>

                {isLoading ? (
                    <p className="loading-text">Loading users...</p>
                ) : (
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th className="sortable-header" onClick={() => handleSort('id')}>ID {renderSortArrow('id')}</th>
                                <th className="sortable-header" onClick={() => handleSort('email')}>Email / Username {renderSortArrow('email')}</th>
                                <th className="sortable-header" onClick={() => handleSort('student_id')}>Student ID {renderSortArrow('student_id')}</th>
                                <th className="sortable-header" onClick={() => handleSort('is_admin')}>Admin {renderSortArrow('is_admin')}</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sortedUsers.length === 0 ? (
                                <tr><td colSpan="5" style={{ textAlign: 'center', padding: '20px' }}>No users found.</td></tr>
                            ) : (
                                sortedUsers.map(user => (
                                    <tr key={user.id}>
                                        <td>{user.id}</td>
                                        {editingUserId === user.id ? ( // If this user is being edited, show input fields instead of text
                                            <>
                                                <td>
                                                    <input type="text" value={editUsername} onChange={(e) => setEditUsername(e.target.value)} className="edit-input" />
                                                    <input type="text" placeholder="New Password" value={editPassword} onChange={(e) => setEditPassword(e.target.value)} className="edit-input mt-1" />
                                                </td>
                                                <td><input type="text" value={editStudentId} onChange={(e) => setEditStudentId(e.target.value)} className="edit-input" /></td>
                                                <td><input type="checkbox" checked={editIsAdmin} onChange={(e) => setEditIsAdmin(e.target.checked)} /></td>
                                                <td>
                                                    <button className="save-btn" onClick={() => handleSaveEdit(user.id)}>Save</button>
                                                    <button className="cancel-btn" onClick={cancelEditing}>Cancel</button>
                                                </td>
                                            </>
                                        ) : ( // If not being edited, show regular text
                                            <>
                                                <td>{user.email}</td>
                                                <td>{user.student_id || '-'}</td>
                                                <td>{user.is_admin ? 'Yes' : 'No'}</td>
                                                <td>
                                                    <button className="edit-btn" onClick={() => startEditing(user)}>Edit</button>
                                                    <button className="delete-btn" onClick={() => handleDeleteUser(user.id)}>Delete</button>
                                                </td>
                                            </>
                                        )}
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
}