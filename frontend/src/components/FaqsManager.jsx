import { useState, useEffect } from 'react';
import api from '../services/api';
import { useTableFeatures } from '../hooks/useTableFeatures';

export default function FaqsManager() {
    const [faqs, setFaqs] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const [newQuestion, setNewQuestion] = useState('');
    const [newAnswer, setNewAnswer] = useState('');
    const [newTags, setNewTags] = useState('');

    const [editingFaqId, setEditingFaqId] = useState(null);
    const [editQuestion, setEditQuestion] = useState('');
    const [editAnswer, setEditAnswer] = useState('');
    const [editTags, setEditTags] = useState('');

    const { searchTerm, setSearchTerm, handleSort, renderSortArrow, processedData: sortedFaqs } = useTableFeatures(faqs, ['question', 'tags']);

    useEffect(() => { fetchFaqs(); }, []);

    const fetchFaqs = async () => {
        try {
            setIsLoading(true);
            const response = await api.get('/api/admin/faq');
            setFaqs(response.data);
            setError('');
        } catch (err) {
            setError('Failed to load FAQs.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreateFaq = async (e) => {
        e.preventDefault();
        try {
            await api.post('/api/admin/faq', { question: newQuestion, answer: newAnswer, tags: newTags || null });
            setNewQuestion(''); setNewAnswer(''); setNewTags('');
            fetchFaqs();
        } catch (err) { alert("Error creating FAQ."); }
    };

    const handleDeleteFaq = async (faqId) => {
        if (!window.confirm("Are you sure?")) return;
        try { await api.delete(`/api/admin/faq/${faqId}`); fetchFaqs(); } 
        catch (err) { alert("Error deleting FAQ."); }
    };

    const startEditing = (faq) => {
        setEditingFaqId(faq.id);
        setEditQuestion(faq.question);
        setEditAnswer(faq.answer);
        setEditTags(faq.tags || '');
    };

    const cancelEditing = () => { setEditingFaqId(null); };

    const handleSaveEdit = async (faqId) => {
        try {
            await api.patch(`/api/admin/faq/${faqId}`, { question: editQuestion, answer: editAnswer, tags: editTags || null });
            setEditingFaqId(null);
            fetchFaqs();
        } catch (err) { alert("Error updating FAQ."); }
    };

    return (
        <div className="manager-container">
            <h2>FAQs Management</h2>
            {error && <div className="error-message">{error}</div>}

            <div className="create-form-card">
                <h3>Add New FAQ</h3>
                <form onSubmit={handleCreateFaq} className="inline-form">
                    <input type="text" placeholder="Question" value={newQuestion} onChange={(e) => setNewQuestion(e.target.value)} required />
                    <input type="text" placeholder="Answer" value={newAnswer} onChange={(e) => setNewAnswer(e.target.value)} required />
                    <input type="text" placeholder="Tags (e.g., library, wifi)" value={newTags} onChange={(e) => setNewTags(e.target.value)} />
                    <button type="submit">Create</button>
                </form>
            </div>

            <div className="table-container">
                <div className="search-bar-container">
                    <input type="text" placeholder="Search FAQs by question or tags..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="search-input" />
                </div>
                {isLoading ? <p className="loading-text">Loading...</p> : (
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th className="sortable-header" onClick={() => handleSort('id')}>ID {renderSortArrow('id')}</th>
                                <th className="sortable-header" onClick={() => handleSort('question')}>Question {renderSortArrow('question')}</th>
                                <th>Answer</th>
                                <th className="sortable-header" onClick={() => handleSort('tags')}>Tags {renderSortArrow('tags')}</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sortedFaqs.map(faq => (
                                <tr key={faq.id}>
                                    <td>{faq.id}</td>
                                    {editingFaqId === faq.id ? (
                                        <>
                                            <td><input type="text" value={editQuestion} onChange={(e) => setEditQuestion(e.target.value)} className="edit-input" /></td>
                                            <td><input type="text" value={editAnswer} onChange={(e) => setEditAnswer(e.target.value)} className="edit-input" /></td>
                                            <td><input type="text" value={editTags} onChange={(e) => setEditTags(e.target.value)} className="edit-input" /></td>
                                            <td>
                                                <button className="save-btn" onClick={() => handleSaveEdit(faq.id)}>Save</button>
                                                <button className="cancel-btn" onClick={cancelEditing}>Cancel</button>
                                            </td>
                                        </>
                                    ) : (
                                        <>
                                            <td>{faq.question}</td><td>{faq.answer}</td><td>{faq.tags || '-'}</td>
                                            <td>
                                                <button className="edit-btn" onClick={() => startEditing(faq)}>Edit</button>
                                                <button className="delete-btn" onClick={() => handleDeleteFaq(faq.id)}>Delete</button>
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