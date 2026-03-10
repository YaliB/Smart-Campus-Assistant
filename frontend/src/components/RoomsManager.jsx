import { useState, useEffect } from 'react';
import api from '../services/api';
// Using custom hook for search and sort!
import { useTableFeatures } from '../hooks/useTableFeatures';

export default function RoomsManager() {
    const [rooms, setRooms] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    // State for creating a new room
    const [newRoomName, setNewRoomName] = useState('');
    const [newBuilding, setNewBuilding] = useState('');
    const [newDescription, setNewDescription] = useState('');

    // State for editing an existing room
    const [editingRoomId, setEditingRoomId] = useState(null);
    const [editRoomName, setEditRoomName] = useState('');
    const [editBuilding, setEditBuilding] = useState('');
    const [editDescription, setEditDescription] = useState('');

    // Initialize the custom hook - searching by room name and building
    const { 
        searchTerm, 
        setSearchTerm, 
        handleSort, 
        renderSortArrow, 
        processedData: sortedRooms 
    } = useTableFeatures(rooms, ['room_name', 'building']);

    useEffect(() => {
        fetchRooms();
    }, []);

    const fetchRooms = async () => {
        try {
            setIsLoading(true);
            const response = await api.get('/api/admin/rooms');
            setRooms(response.data);
            setError('');
        } catch (err) {
            console.error("Failed to fetch rooms", err);
            setError('Failed to load rooms.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreateRoom = async (e) => {
        e.preventDefault();
        try {
            await api.post('/api/admin/rooms', { 
                room_name: newRoomName, 
                building: newBuilding,
                description: newDescription ? newDescription : null
            });
            
            // Clear form and refresh
            setNewRoomName('');
            setNewBuilding('');
            setNewDescription('');
            fetchRooms();
        } catch (err) {
            console.error("Failed to create room", err);
            alert("Error creating room. Check if the name already exists.");
        }
    };

    const handleDeleteRoom = async (roomId) => {
        if (!window.confirm("Are you sure you want to delete this room?")) return;
        try {
            await api.delete(`/api/admin/rooms/${roomId}`);
            fetchRooms();
        } catch (err) {
            console.error("Failed to delete room", err);
            alert("Error deleting room.");
        }
    };

    const startEditing = (room) => {
        setEditingRoomId(room.id);
        setEditRoomName(room.room_name);
        setEditBuilding(room.building);
        setEditDescription(room.description || '');
    };

    const cancelEditing = () => {
        setEditingRoomId(null);
        setEditRoomName('');
        setEditBuilding('');
        setEditDescription('');
    };

    const handleSaveEdit = async (roomId) => {
        try {
            const payload = {
                room_name: editRoomName,
                building: editBuilding,
                description: editDescription ? editDescription : null
            };

            // Using PATCH just like we discussed
            await api.patch(`/api/admin/rooms/${roomId}`, payload);
            setEditingRoomId(null);
            fetchRooms();
        } catch (err) {
            console.error("Failed to update room", err);
            alert("Error updating room.");
        }
    };

    return (
        <div className="manager-container">
            <h2>Rooms Management</h2>
            {error && <div className="error-message">{error}</div>}

            {/* Create Room Form */}
            <div className="create-form-card">
                <h3>Add New Room</h3>
                <form onSubmit={handleCreateRoom} className="inline-form">
                    <input 
                        type="text" 
                        placeholder="Room Name (e.g., F101)" 
                        value={newRoomName} 
                        onChange={(e) => setNewRoomName(e.target.value)} 
                        required 
                    />
                    <input 
                        type="text" 
                        placeholder="Building (e.g., Main)" 
                        value={newBuilding} 
                        onChange={(e) => setNewBuilding(e.target.value)} 
                        required 
                    />
                    <input 
                        type="text" 
                        placeholder="Description (Optional)" 
                        value={newDescription} 
                        onChange={(e) => setNewDescription(e.target.value)} 
                    />
                    <button type="submit">Create</button>
                </form>
            </div>

            {/* Rooms Table & Search Bar */}
            <div className="table-container">
                <div className="search-bar-container">
                    <input 
                        type="text" 
                        placeholder="Search rooms by name or building..." 
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="search-input"
                    />
                </div>

                {isLoading ? (
                    <p className="loading-text">Loading rooms...</p>
                ) : (
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th className="sortable-header" onClick={() => handleSort('id')}>
                                    ID {renderSortArrow('id')}
                                </th>
                                <th className="sortable-header" onClick={() => handleSort('room_name')}>
                                    Room Name {renderSortArrow('room_name')}
                                </th>
                                <th className="sortable-header" onClick={() => handleSort('building')}>
                                    Building {renderSortArrow('building')}
                                </th>
                                <th className="sortable-header" onClick={() => handleSort('description')}>
                                    Description {renderSortArrow('description')}
                                </th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sortedRooms.length === 0 ? (
                                <tr>
                                    <td colSpan="5" style={{ textAlign: 'center', padding: '20px' }}>
                                        No rooms found.
                                    </td>
                                </tr>
                            ) : (
                                sortedRooms.map(room => (
                                    <tr key={room.id}>
                                        <td>{room.id}</td>
                                        
                                        {editingRoomId === room.id ? (
                                            <>
                                                <td>
                                                    <input 
                                                        type="text" 
                                                        value={editRoomName} 
                                                        onChange={(e) => setEditRoomName(e.target.value)} 
                                                        className="edit-input"
                                                    />
                                                </td>
                                                <td>
                                                    <input 
                                                        type="text" 
                                                        value={editBuilding} 
                                                        onChange={(e) => setEditBuilding(e.target.value)} 
                                                        className="edit-input"
                                                    />
                                                </td>
                                                <td>
                                                    <input 
                                                        type="text" 
                                                        value={editDescription} 
                                                        onChange={(e) => setEditDescription(e.target.value)} 
                                                        className="edit-input"
                                                    />
                                                </td>
                                                <td>
                                                    <button className="save-btn" onClick={() => handleSaveEdit(room.id)}>Save</button>
                                                    <button className="cancel-btn" onClick={cancelEditing}>Cancel</button>
                                                </td>
                                            </>
                                        ) : (
                                            <>
                                                <td>{room.room_name}</td>
                                                <td>{room.building}</td>
                                                <td>{room.description || '-'}</td>
                                                <td>
                                                    <button className="edit-btn" onClick={() => startEditing(room)}>Edit</button>
                                                    <button className="delete-btn" onClick={() => handleDeleteRoom(room.id)}>Delete</button>
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