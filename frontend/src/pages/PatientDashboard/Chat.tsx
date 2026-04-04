// Example Patient Simplifier Chat

import React, { useState } from 'react';

export const PatientSimplifierChat = ({ visitId }) => {
    const [message, setMessage] = useState("");
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!message) return;
        
        const userMsg = { role: 'user', content: message };
        setHistory(prev => [...prev, userMsg]);
        setLoading(true);
        
        try {
            const res = await fetch(`/api/patient/visits/${visitId}/explain-chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            });
            const data = await res.json();
            
            const assistMsg = { 
                role: 'assistant', 
                content: data.answer,
                isSupported: data.is_supported
            };
            setHistory(prev => [...prev, assistMsg]);
        } catch (err) {
            console.error("Chat Failed", err);
        } finally {
            setLoading(false);
            setMessage("");
        }
    };

    return (
        <div style={{ maxWidth: '600px', border: '1px solid #ddd', padding: '1rem', marginTop: '2rem' }}>
            <h3>Dr. Orbit Explainer</h3>
            <p><small><i>AI Assistant - Answers strictly limited to your approved visit chart.</i></small></p>
            
            <div style={{ height: '300px', overflowY: 'auto', marginBottom: '1rem', background: '#f9f9f9', padding: '1rem' }}>
                {history.map((msg, idx) => (
                    <div key={idx} style={{ marginBottom: '1rem', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                        <span style={{ 
                            background: msg.role === 'user' ? '#007bff' : (msg.isSupported === false ? '#ffeeba' : '#e2e3e5'), 
                            color: msg.role === 'user' ? 'white' : 'black',
                            padding: '0.5rem 1rem', 
                            borderRadius: '15px', 
                            display: 'inline-block' 
                        }}>
                            {msg.content}
                        </span>
                        {msg.isSupported === false && <div style={{ fontSize: '10px', color: 'red' }}>Out of bounds</div>}
                    </div>
                ))}
            </div>
            
            <div style={{ display: 'flex' }}>
                <input 
                    style={{ flex: 1, padding: '0.5rem' }}
                    value={message} 
                    onChange={e => setMessage(e.target.value)} 
                    placeholder="Ask a question about your report..." 
                />
                <button onClick={handleSend} disabled={loading} style={{ marginLeft: '0.5rem', padding: '0.5rem 1rem' }}>
                    {loading ? '...' : 'Ask'}
                </button>
            </div>
        </div>
    );
};
