// Example Patient Dashboard structure

import React, { useEffect, useState } from 'react';

/**
 * Simple scaffolding demonstrating how the frontend consumes our new Component 8 safe API endpoints.
 */
export const PatientDashboard = () => {
    const [visits, setVisits] = useState([]);
    const [reminders, setReminders] = useState([]);

    useEffect(() => {
        // Fetch securely filtered visits
        fetch('/api/patient/visits')
            .then(res => res.json())
            .then(data => setVisits(data));
            
        // Fetch unified reminders exclusively from APPROVED reports
        fetch('/api/patient/reminders')
            .then(res => res.json())
            .then(data => setReminders(data));
    }, []);

    return (
        <div style={{ padding: '2rem' }}>
            <h1>Patient Dashboard</h1>
            
            <section style={{ marginBottom: '2rem' }}>
                <h2>Your Action Items & Reminders</h2>
                {reminders.length === 0 ? <p>You're all caught up!</p> : (
                    <ul>
                        {reminders.map((r, idx) => (
                            <li key={idx}>✅ {r.task} (Prescribed: {new Date(r.visit_date).toLocaleDateString()})</li>
                        ))}
                    </ul>
                )}
            </section>

            <section>
                <h2>Visit History</h2>
                {visits.map(v => (
                    <div key={v.visit_id} style={{ border: '1px solid #ccc', margin: '1rem 0', padding: '1rem' }}>
                        <h3>{v.title}</h3>
                        {!v.has_approved_report ? (
                            <p><i>Your doctor is still verifying the report for this visit. Check back later!</i></p>
                        ) : (
                            <div>
                                <p><strong>Summary:</strong> {v.simplified_explanation}</p>
                                <p><strong>Discharge Notes:</strong> {v.patient_discharge_draft}</p>
                            </div>
                        )}
                    </div>
                ))}
            </section>
        </div>
    );
};
