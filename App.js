import React, { useState, useCallback } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && (droppedFile.name.endsWith('.pdf') || droppedFile.name.endsWith('.docx'))) {
      setFile(droppedFile);
      setError('');
    } else {
      setError('Please upload a PDF or DOCX file');
    }
  }, []);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError('');
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload your resume');
      return;
    }
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResults(data);
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure the backend is running.');
    }

    setLoading(false);
  };

  const getScoreColor = (score) => {
    if (score >= 75) return '#00d4aa';
    if (score >= 50) return '#fbbf24';
    return '#ff4757';
  };

  const getScoreLabel = (score) => {
    if (score >= 75) return 'Excellent';
    if (score >= 50) return 'Good';
    return 'Needs Work';
  };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <header className="header">
          <h1>🎯 AI Resume Analyzer</h1>
          <p>Upload your resume, paste a job description, and get AI-powered insights</p>
        </header>

        {/* Main Content */}
        <div className="main-grid">
          {/* Left Panel - Input */}
          <div className="panel">
            <h2 className="panel-title">📄 Upload Resume</h2>
            
            <div
              className={`upload-zone ${dragOver ? 'dragover' : ''} ${file ? 'has-file' : ''}`}
              onDrop={handleDrop}
              onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onClick={() => document.getElementById('file-input').click()}
            >
              <input
                id="file-input"
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              {file ? (
                <>
                  <div className="file-icon">📎</div>
                  <div className="file-name">{file.name}</div>
                  <div className="file-size">{(file.size / 1024).toFixed(1)} KB</div>
                </>
              ) : (
                <>
                  <div className="upload-icon">📤</div>
                  <div className="upload-text">Drop your resume here or click to browse</div>
                  <div className="upload-hint">Supports PDF and DOCX</div>
                </>
              )}
            </div>

            <h2 className="panel-title" style={{ marginTop: '24px' }}>💼 Job Description</h2>
            <textarea
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={8}
            />

            {error && <div className="error-message">{error}</div>}

            <button
              className="analyze-btn"
              onClick={handleAnalyze}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                <>🔍 Analyze Resume</>
              )}
            </button>
          </div>

          {/* Right Panel - Results */}
          <div className="panel results-panel">
            {!results && !loading && (
              <div className="empty-state">
                <div className="empty-icon">📊</div>
                <h3>Your Analysis Results</h3>
                <p>Upload your resume and enter a job description to see how well you match</p>
              </div>
            )}

            {loading && (
              <div className="loading-state">
                <div className="loading-spinner"></div>
                <h3>Analyzing your resume...</h3>
                <p>Our AI is comparing your skills and experience</p>
              </div>
            )}

            {results && (
              <div className="results">
                {/* Score Cards */}
                <div className="score-grid">
                  <div className="score-card">
                    <div className="score-circle" style={{ '--score-color': getScoreColor(results.match_score) }}>
                      <svg viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" className="score-bg" />
                        <circle
                          cx="50" cy="50" r="45"
                          className="score-fill"
                          style={{
                            strokeDasharray: `${results.match_score * 2.83} 283`,
                            stroke: getScoreColor(results.match_score)
                          }}
                        />
                      </svg>
                      <div className="score-value">{results.match_score}%</div>
                    </div>
                    <div className="score-label">Match Score</div>
                    <div className="score-sublabel" style={{ color: getScoreColor(results.match_score) }}>
                      {getScoreLabel(results.match_score)}
                    </div>
                  </div>

                  <div className="score-card">
                    <div className="score-circle" style={{ '--score-color': getScoreColor(results.ats_score.total) }}>
                      <svg viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" className="score-bg" />
                        <circle
                          cx="50" cy="50" r="45"
                          className="score-fill"
                          style={{
                            strokeDasharray: `${results.ats_score.total * 2.83} 283`,
                            stroke: getScoreColor(results.ats_score.total)
                          }}
                        />
                      </svg>
                      <div className="score-value">{results.ats_score.total}%</div>
                    </div>
                    <div className="score-label">ATS Score</div>
                    <div className="score-sublabel" style={{ color: getScoreColor(results.ats_score.total) }}>
                      {getScoreLabel(results.ats_score.total)}
                    </div>
                  </div>
                </div>

                {/* Stats Row */}
                <div className="stats-row">
                  <div className="stat">
                    <span className="stat-value">{results.stats.word_count}</span>
                    <span className="stat-label">Words</span>
                  </div>
                  <div className="stat">
                    <span className="stat-value">{results.stats.skills_count}</span>
                    <span className="stat-label">Skills Found</span>
                  </div>
                  <div className="stat">
                    <span className="stat-value">{results.stats.strong_verbs}</span>
                    <span className="stat-label">Action Verbs</span>
                  </div>
                </div>

                {/* ATS Breakdown */}
                <div className="section">
                  <h3 className="section-title">📊 ATS Score Breakdown</h3>
                  <div className="ats-breakdown">
                    {Object.entries(results.ats_score.breakdown).map(([key, value]) => (
                      <div className="ats-item" key={key}>
                        <div className="ats-label">{key}</div>
                        <div className="ats-bar">
                          <div
                            className="ats-fill"
                            style={{
                              width: `${(value / (key === 'Skills Match' ? 35 : key === 'Keywords' ? 25 : key === 'Contact Info' || key === 'Formatting' ? 15 : 10)) * 100}%`
                            }}
                          />
                        </div>
                        <div className="ats-value">{value}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Skills */}
                {results.missing_skills.length > 0 && (
                  <div className="section">
                    <h3 className="section-title">🔧 Missing Skills</h3>
                    <div className="skills-list">
                      {results.missing_skills.slice(0, 8).map((skill, i) => (
                        <span className="skill-tag missing" key={i}>{skill}</span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Your Skills */}
                {Object.keys(results.resume_skills).length > 0 && (
                  <div className="section">
                    <h3 className="section-title">✅ Your Skills</h3>
                    <div className="skills-list">
                      {Object.values(results.resume_skills).flat().slice(0, 12).map((skill, i) => (
                        <span className="skill-tag found" key={i}>{skill}</span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Recommendations */}
                <div className="section">
                  <h3 className="section-title">💡 Recommendations</h3>
                  <div className="recommendations">
                    {results.recommendations.map((rec, i) => (
                      <div className={`recommendation ${rec.type}`} key={i}>
                        <div className="rec-icon">{rec.icon}</div>
                        <div className="rec-content">
                          <div className="rec-title">{rec.title}</div>
                          <div className="rec-desc">{rec.description}</div>
                          {rec.items && (
                            <div className="rec-items">
                              {rec.items.map((item, j) => (
                                <span key={j} className="rec-item">{item}</span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
