import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import UsersManager from '../components/UsersManager';
import RoomsManager from '../components/RoomsManager';
import FaqsManager from '../components/FaqsManager';
import ReceptionHoursManager from '../components/ReceptionHoursManager';
import ExamSchedulesManager from '../components/ExamSchedulesManager';
import './Dashboard.css';

export default function Dashboard() {
    const [activeTab, setActiveTab] = useState('users');
    const navigate = useNavigate();

    return (
        <div className="dashboard-layout">
            {/* Sidebar Navigation */}
            <aside className="sidebar">
                <h2>Admin Panel</h2>
                <nav>
                    <ul>
                        <li className={activeTab === 'users' ? 'active' : ''} onClick={() => setActiveTab('users')}>
                            Users
                        </li>
                        <li className={activeTab === 'rooms' ? 'active' : ''} onClick={() => setActiveTab('rooms')}>
                            Rooms
                        </li>
                        <li className={activeTab === 'faqs' ? 'active' : ''} onClick={() => setActiveTab('faqs')}>
                            FAQs
                        </li>
                        <li className={activeTab === 'reception' ? 'active' : ''} onClick={() => setActiveTab('reception')}>
                            Reception Hours
                        </li>
                        <li className={activeTab === 'exams' ? 'active' : ''} onClick={() => setActiveTab('exams')}>
                            Exam Schedules
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
                {activeTab === 'rooms' && <RoomsManager />}
                {activeTab === 'faqs' && <FaqsManager />}
                {activeTab === 'reception' && <ReceptionHoursManager />}
                {activeTab === 'exams' && <ExamSchedulesManager />}
            </main>
        </div>
    );
}