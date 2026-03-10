import { useState, useEffect } from 'react';
import api from '../services/api';
import { useTableFeatures } from '../hooks/useTableFeatures';

export default function ExamSchedulesManager() {
    const [exams, setExams] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const [newCourse, setNewCourse] = useState('');
    const [newDate, setNewDate] = useState('');
    const [newLocation, setNewLocation] = useState('');

    const [editingId, setEditingId] = useState(null);
    const [editCourse, setEditCourse] = useState('');
    const [editDate, setEditDate] = useState('');
    const [editLocation, setEditLocation] = useState('');

    const { searchTerm, setSearchTerm, handleSort, renderSortArrow, processedData: sortedExams } = useTableFeatures(exams, ['course_name']);

    useEffect(() => { fetchExams(); }, []);

    const fetchExams = async () => {
        try {
            setIsLoading(true);
            const response = await api.get('/api/admin/exams');
            setExams(response.data);
            setError('');
        } catch (err) { setError('Failed to load exams.'); } 
        finally { setIsLoading(false); }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            // Convert to ISO string if needed by backend, or send as is if FastAPI parses it correctly
            await api.post('/api/admin/exams', { course_name: newCourse, exam_date: newDate, location: newLocation });
            setNewCourse(''); setNewDate(''); setNewLocation('');
            fetchExams();
        } catch (err) { alert("Error creating exam."); }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure?")) return;
        try { await api.delete(`/api/admin/exams/${id}`); fetchExams(); } 
        catch (err) { alert("Error deleting exam."); }
    };

    const startEditing = (item) => {
        setEditingId(item.id); setEditCourse(item.course_name); 
        // HTML datetime-local requires format YYYY-MM-DDThh:mm
        const dateString = item.exam_date ? new Date(item.exam_date).toISOString().slice(0, 16) : '';
        setEditDate(dateString); 
        setEditLocation(item.location);
    };

    const handleSaveEdit = async (id) => {
        try {
            await api.patch(`/api/admin/exams/${id}`, { course_name: editCourse, exam_date: editDate, location: editLocation });
            setEditingId(null); fetchExams();
        } catch (err) { alert("Error updating exam."); }
    };

    return (
        <div className="manager-container">
            <h2>Exam Schedules Management</h2>
            {error && <div className="error-message">{error}</div>}

            <div className="create-form-card">
                <h3>Add New Exam</h3>
                <form onSubmit={handleCreate} className="inline-form">
                    <input type="text" placeholder="Course Name" value={newCourse} onChange={(e) => setNewCourse(e.target.value)} required />
                    <input type="datetime-local" value={newDate} onChange={(e) => setNewDate(e.target.value)} required />
                    <input type="text" placeholder="Location" value={newLocation} onChange={(e) => setNewLocation(e.target.value)} required />
                    <button type="submit">Create</button>
                </form>
            </div>

            <div className="table-container">
                <div className="search-bar-container">
                    <input type="text" placeholder="Search by course name..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="search-input" />
                </div>
                {isLoading ? <p className="loading-text">Loading...</p> : (
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th onClick={() => handleSort('id')} className="sortable-header">ID {renderSortArrow('id')}</th>
                                <th onClick={() => handleSort('course_name')} className="sortable-header">Course Name {renderSortArrow('course_name')}</th>
                                <th onClick={() => handleSort('exam_date')} className="sortable-header">Date & Time {renderSortArrow('exam_date')}</th>
                                <th>Location</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sortedExams.map(item => (
                                <tr key={item.id}>
                                    <td>{item.id}</td>
                                    {editingId === item.id ? (
                                        <>
                                            <td><input type="text" value={editCourse} onChange={(e) => setEditCourse(e.target.value)} className="edit-input" /></td>
                                            <td><input type="datetime-local" value={editDate} onChange={(e) => setEditDate(e.target.value)} className="edit-input" /></td>
                                            <td><input type="text" value={editLocation} onChange={(e) => setEditLocation(e.target.value)} className="edit-input" /></td>
                                            <td>
                                                <button className="save-btn" onClick={() => handleSaveEdit(item.id)}>Save</button>
                                                <button className="cancel-btn" onClick={() => setEditingId(null)}>Cancel</button>
                                            </td>
                                        </>
                                    ) : (
                                        <>
                                            <td>{item.course_name}</td>
                                            <td>{new Date(item.exam_date).toLocaleString()}</td>
                                            <td>{item.location}</td>
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