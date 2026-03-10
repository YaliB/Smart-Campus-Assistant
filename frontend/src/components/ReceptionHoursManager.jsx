import { useState, useEffect } from 'react';
import api from '../services/api';
import { useTableFeatures } from '../hooks/useTableFeatures';

export default function ReceptionHoursManager() {
    const [hours, setHours] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const [newDept, setNewDept] = useState('');
    const [newHours, setNewHours] = useState('');
    const [newContact, setNewContact] = useState('');

    const [editingId, setEditingId] = useState(null);
    const [editDept, setEditDept] = useState('');
    const [editHours, setEditHours] = useState('');
    const [editContact, setEditContact] = useState('');

    const { searchTerm, setSearchTerm, handleSort, renderSortArrow, processedData: sortedHours } = useTableFeatures(hours, ['department']);

    useEffect(() => { fetchHours(); }, []);

    const fetchHours = async () => {
        try {
            setIsLoading(true);
            const response = await api.get('/api/admin/reception');
            setHours(response.data);
            setError('');
        } catch (err) { setError('Failed to load reception hours.'); } 
        finally { setIsLoading(false); }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            await api.post('/api/admin/reception', { department: newDept, hours: newHours, contact_info: newContact || null });
            setNewDept(''); setNewHours(''); setNewContact('');
            fetchHours();
        } catch (err) { alert("Error creating record."); }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure?")) return;
        try { await api.delete(`/api/admin/reception/${id}`); fetchHours(); } 
        catch (err) { alert("Error deleting record."); }
    };

    const startEditing = (item) => {
        setEditingId(item.id); setEditDept(item.department); setEditHours(item.hours); setEditContact(item.contact_info || '');
    };

    const handleSaveEdit = async (id) => {
        try {
            await api.patch(`/api/admin/reception/${id}`, { department: editDept, hours: editHours, contact_info: editContact || null });
            setEditingId(null); fetchHours();
        } catch (err) { alert("Error updating record."); }
    };

    return (
        <div className="manager-container">
            <h2>Reception Hours Management</h2>
            {error && <div className="error-message">{error}</div>}

            <div className="create-form-card">
                <h3>Add New Reception Hour</h3>
                <form onSubmit={handleCreate} className="inline-form">
                    <input type="text" placeholder="Department" value={newDept} onChange={(e) => setNewDept(e.target.value)} required />
                    <input type="text" placeholder="Hours (e.g., Sun-Thu 09:00-15:00)" value={newHours} onChange={(e) => setNewHours(e.target.value)} required />
                    <input type="text" placeholder="Contact Info (Optional)" value={newContact} onChange={(e) => setNewContact(e.target.value)} />
                    <button type="submit">Create</button>
                </form>
            </div>

            <div className="table-container">
                <div className="search-bar-container">
                    <input type="text" placeholder="Search by department..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="search-input" />
                </div>
                {isLoading ? <p className="loading-text">Loading...</p> : (
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th onClick={() => handleSort('id')} className="sortable-header">ID {renderSortArrow('id')}</th>
                                <th onClick={() => handleSort('department')} className="sortable-header">Department {renderSortArrow('department')}</th>
                                <th>Hours</th>
                                <th>Contact Info</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sortedHours.map(item => (
                                <tr key={item.id}>
                                    <td>{item.id}</td>
                                    {editingId === item.id ? (
                                        <>
                                            <td><input type="text" value={editDept} onChange={(e) => setEditDept(e.target.value)} className="edit-input" /></td>
                                            <td><input type="text" value={editHours} onChange={(e) => setEditHours(e.target.value)} className="edit-input" /></td>
                                            <td><input type="text" value={editContact} onChange={(e) => setEditContact(e.target.value)} className="edit-input" /></td>
                                            <td>
                                                <button className="save-btn" onClick={() => handleSaveEdit(item.id)}>Save</button>
                                                <button className="cancel-btn" onClick={() => setEditingId(null)}>Cancel</button>
                                            </td>
                                        </>
                                    ) : (
                                        <>
                                            <td>{item.department}</td><td>{item.hours}</td><td>{item.contact_info || '-'}</td>
                                            <td>
                                                <button className="edit-btn" onClick={() => startEditing(item)}>Edit</button>
                                                <button className="delete-btn" onClick={() => handleDelete(item.id)}>Delete</button>
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