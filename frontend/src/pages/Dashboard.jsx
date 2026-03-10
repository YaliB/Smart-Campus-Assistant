import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import UsersManager from '../components/UsersManager';
import './Dashboard.css';

export default function Dashboard() {
    // State to manage which admin tab is currently active
    const [activeTab, setActiveTab] = useState('users');
    const navigate = useNavigate();

    return (
        <div className="dashboard-layout">
            {/* Sidebar Navigation */}
            <aside className="sidebar">
                <h2>Admin Panel</h2>
                <nav>
                    <ul>
                        <li 
                            className={activeTab === 'users' ? 'active' : ''} 
                            onClick={() => setActiveTab('users')}
                        >
                            Users
                        </li>
                        <li 
                            className={activeTab === 'rooms' ? 'active' : ''} 
                            onClick={() => setActiveTab('rooms')}
                        >
                            Rooms
                        </li>
                        <li 
                            className={activeTab === 'faqs' ? 'active' : ''} 
                            onClick={() => setActiveTab('faqs')}
                        >
                            FAQs
                        </li>
                    </ul>
                </nav>
                <button className="back-button" onClick={() => navigate('/chat')}>
                    &larr; Back to Chat
                </button>
            </aside>

            {/* Main Content Area */}
            <main className="dashboard-content">
                {activeTab === 'users' && <UsersManager />}
                {activeTab === 'rooms' && <div><h2>Rooms Management</h2><p>Coming soon...</p></div>}
                {activeTab === 'faqs' && <div><h2>FAQs Management</h2><p>Coming soon...</p></div>}
            </main>
        </div>
    );
}