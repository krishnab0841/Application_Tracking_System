import React from 'react';
import { CheckCircle, XCircle, AlertTriangle, ArrowRight } from 'lucide-react';

const ResultDisplay = ({ result, type }) => {
    if (!result) return null;

    let data = result;
    if (typeof result === 'string') {
        try {
            data = JSON.parse(result);
        } catch (e) {
            // If it's not JSON, it might be a simple message or error
            return (
                <div className="glass-card animate-fade-in">
                    <h2>Result</h2>
                    <pre className="raw-text">{result}</pre>
                </div>
            );
        }
    }

    // Handle PDF Export Message
    if (data.message) {
        return (
            <div className="glass-card animate-fade-in success-card">
                <CheckCircle size={48} color="#10b981" />
                <h2>{data.message}</h2>
            </div>
        );
    }

    const renderContent = () => {
        switch (type) {
            case 'check_score':
                return (
                    <div className="score-view">
                        <div className="score-circle">
                            <span className="score-value">{data.score}</span>
                            <span className="score-label">Match</span>
                        </div>
                        <div className="score-breakdown">
                            {data.breakdown && Object.entries(data.breakdown).map(([key, value]) => (
                                <div key={key} className="breakdown-item">
                                    <span>{key.replace('_', ' ')}</span>
                                    <div className="progress-bar">
                                        <div className="progress-fill" style={{ width: value }}></div>
                                    </div>
                                    <span>{value}</span>
                                </div>
                            ))}
                        </div>
                        <p className="reasoning">{data.reasoning}</p>
                    </div>
                );

            case 'keyword_match':
                return (
                    <div className="keyword-view">
                        <div className="keyword-section match">
                            <h3><CheckCircle size={18} /> Matching Keywords</h3>
                            <div className="tags">
                                {data.matching_keywords?.map((k, i) => <span key={i} className="tag match">{k}</span>)}
                            </div>
                        </div>
                        <div className="keyword-section missing">
                            <h3><XCircle size={18} /> Missing Keywords</h3>
                            <div className="tags">
                                {data.missing_keywords?.map((k, i) => <span key={i} className="tag missing">{k}</span>)}
                            </div>
                        </div>
                        <p className="analysis-text">{data.keyword_analysis}</p>
                    </div>
                );

            case 'rewrite_bullets':
                return (
                    <div className="rewrite-view">
                        {data.rewrites?.map((item, index) => (
                            <div key={index} className="rewrite-card">
                                <div className="original">
                                    <h4>Original</h4>
                                    <p>{item.original}</p>
                                </div>
                                <div className="arrow"><ArrowRight /></div>
                                <div className="improved">
                                    <h4>Improved</h4>
                                    <p>{item.improved}</p>
                                </div>
                                <p className="reason-text"><strong>Why:</strong> {item.reason}</p>
                            </div>
                        ))}
                    </div>
                );

            case 'grammar_check':
                return (
                    <div className="grammar-view">
                        {data.errors?.length === 0 ? (
                            <div className="success-message">No grammar errors found!</div>
                        ) : (
                            data.errors?.map((err, i) => (
                                <div key={i} className="error-card">
                                    <div className="error-header">
                                        <span className="error-text">"{err.error}"</span>
                                        <ArrowRight size={16} />
                                        <span className="correction-text">"{err.correction}"</span>
                                    </div>
                                    <p className="context">Context: ...{err.context}...</p>
                                </div>
                            ))
                        )}
                    </div>
                );

            default:
                // Generic handler for other types (summarize, format_fix, add_skills)
                return (
                    <div className="generic-view">
                        {Object.entries(data).map(([key, value]) => (
                            <div key={key} className="generic-section">
                                <h3>{key.replace(/_/g, ' ')}</h3>
                                {Array.isArray(value) ? (
                                    <ul>
                                        {value.map((item, i) => <li key={i}>{item}</li>)}
                                    </ul>
                                ) : (
                                    <p>{value}</p>
                                )}
                            </div>
                        ))}
                    </div>
                );
        }
    };

    return (
        <div className="glass-card animate-fade-in result-container">
            <h2>Analysis Result</h2>
            {renderContent()}
        </div>
    );
};

export default ResultDisplay;
