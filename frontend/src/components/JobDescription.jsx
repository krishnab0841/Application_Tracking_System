import React from 'react';

const JobDescription = ({ value, onChange }) => {
    return (
        <div className="glass-card animate-fade-in" style={{ marginBottom: '2rem', animationDelay: '0.1s' }}>
            <h2>Job Description</h2>
            <textarea
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder="Paste the job description here..."
                rows={8}
            />
        </div>
    );
};

export default JobDescription;
