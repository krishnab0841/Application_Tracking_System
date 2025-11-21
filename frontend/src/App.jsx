import React, { useState } from 'react';
import axios from 'axios';
import {
  CheckCircle, Search, Edit3, FileText,
  SpellCheck, Layout, PlusCircle, Download,
  Upload, AlertTriangle
} from 'lucide-react';
import ResultDisplay from './components/ResultDisplay';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeAction, setActiveAction] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async (actionType) => {
    if (!file && actionType !== 'export_pdf') {
      setError('Please upload a resume first.');
      return;
    }

    if (!jd && actionType !== 'grammar_check') {
      setError('Please provide a job description.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);
    setActiveAction(actionType);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('jd', jd);
    formData.append('action', actionType);

    try {
      const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: actionType === 'export_pdf' ? 'blob' : 'json',
      });

      if (actionType === 'export_pdf') {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'improved_resume.pdf');
        document.body.appendChild(link);
        link.click();
        setResult({ message: "PDF Exported Successfully!" });
      } else {
        setResult(response.data.response);
      }
    } catch (err) {
      console.error(err);
      setError('An error occurred during analysis. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const toolButtons = [
    { id: 'keyword_match', label: 'Keyword Match', icon: <Search size={24} />, color: '#8b5cf6' },
    { id: 'rewrite_bullets', label: 'Rewrite Bullets', icon: <Edit3 size={24} />, color: '#ec4899' },
    { id: 'summarize', label: 'Summarize', icon: <FileText size={24} />, color: '#f43f5e' },
    { id: 'grammar_check', label: 'Grammar Check', icon: <SpellCheck size={24} />, color: '#f59e0b' },
    { id: 'format_fix', label: 'Format Fix', icon: <Layout size={24} />, color: '#06b6d4' },
    { id: 'add_skills', label: 'Add Skills', icon: <PlusCircle size={24} />, color: '#10b981' },
    { id: 'export_pdf', label: 'Export PDF', icon: <Download size={24} />, color: '#3b82f6' },
  ];

  return (
    <div className="app-wrapper">
      <div className="two-column-layout">
        {/* Left Panel */}
        <div className="left-panel">
          <div className="jd-section glass-card">
            <h2>Job Description</h2>
            <textarea
              className="jd-textarea"
              value={jd}
              onChange={(e) => setJd(e.target.value)}
              placeholder="Paste the job description here..."
              rows={12}
            />
          </div>

          <div className="upload-section glass-card">
            <h3>Upload Resume</h3>
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              id="resume-upload"
              className="file-input-hidden"
            />
            <label htmlFor="resume-upload" className="upload-resume-btn">
              <Upload size={20} />
              {file ? 'Change Resume' : 'Select PDF'}
            </label>
            {file && <p className="selected-file">{file.name}</p>}
          </div>

          <button
            className="check-score-btn"
            onClick={() => handleAnalyze('check_score')}
            disabled={loading && activeAction === 'check_score'}
          >
            <CheckCircle size={24} />
            {loading && activeAction === 'check_score' ? 'Analyzing...' : 'Check ATS Score'}
          </button>
        </div>

        {/* Right Panel */}
        <div className="right-panel">
          <div className="display-area glass-card">
            {result ? (
              <ResultDisplay result={result} type={activeAction} />
            ) : (
              <div className="placeholder-content">
                <p>Results will appear here after analysis</p>
              </div>
            )}
          </div>

          <div className="tools-grid">
            {/* Tool Buttons */}
            {toolButtons.map((tool) => (
              <button
                key={tool.id}
                className="tool-btn glass-card"
                onClick={() => handleAnalyze(tool.id)}
                disabled={loading}
                style={{ '--tool-color': tool.color }}
              >
                <div className="tool-icon">{tool.icon}</div>
                <span>{tool.label}</span>
                {loading && activeAction === tool.id && <div className="spinner-mini"></div>}
              </button>
            ))}
          </div>

          {error && <div className="error-banner"><AlertTriangle size={16} /> {error}</div>}
        </div>
      </div>
    </div>
  );
}

export default App;
