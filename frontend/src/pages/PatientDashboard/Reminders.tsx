import React, { useState, useEffect } from 'react';

export const PatientRemindersSection = () => {
    const [reminders, setReminders] = useState([]);

    useEffect(() => {
        fetch('/api/patient/reminders')
            .then(res => res.json())
            .then(data => setReminders(data));
    }, []);

    const markComplete = async (id) => {
        try {
            await fetch(`/api/patient/reminders/${id}/status`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ status: "COMPLETED" })
            });
            // Optmistic UI Update
            setReminders(prev => prev.map(r => r.id === id ? { ...r, status: "COMPLETED" } : r));
        } catch (e) {
            console.error("Failed to update status", e);
        }
    };

    return (
        <section style={{ margin: '2rem 0', border: '1px solid #ccc', padding: '1rem' }}>
            <h2>Your Care Tasks</h2>
            {reminders.length === 0 ? <p>You have no current tasks.</p> : (
                <ul style={{ listStyleType: 'none', padding: 0 }}>
                    {reminders.map(r => (
                        <li key={r.id} style={{ 
                            marginBottom: '1rem', 
                            padding: '1rem', 
                            background: r.status === 'COMPLETED' ? '#e2f0cb' : '#ffebcc',
                            display: 'flex',
                            justifyContent: 'space-between',
                            borderRadius: '8px'
                        }}>
                            <div>
                                <strong>{r.title}</strong>
                                <p style={{ margin: '0.2rem 0', fontSize: '0.9rem' }}>
                                    Due: {new Date(r.due_at).toLocaleDateString()}
                                </p>
                            </div>
                            {r.status === 'PENDING' ? (
                                <button onClick={() => markComplete(r.id)}>Complete</button>
                            ) : (
                                <span style={{ color: 'green' }}>✓ Done</span>
                            )}
                        </li>
                    ))}
                </ul>
            )}
        </section>
    );
};
