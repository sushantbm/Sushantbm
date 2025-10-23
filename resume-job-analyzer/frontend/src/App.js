import React, { useState } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [resumeText, setResumeText] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setResumeFile(file);
      setResumeText(''); // Clear text input if file is selected
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();

      if (resumeFile) {
        formData.append('resume_file', resumeFile);
      } else if (resumeText) {
        formData.append('resume_text', resumeText);
      } else {
        setError('Please provide either resume text or upload a file');
        setLoading(false);
        return;
      }

      formData.append('job_title', jobTitle);
      formData.append('job_description', jobDescription);

      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
      const response = await fetch(`${apiUrl}/predict_fit/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Analysis failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#28a745';
    if (score >= 60) return '#ffc107';
    if (score >= 40) return '#fd7e14';
    return '#dc3545';
  };

  return (
    <div className="App">
      <div className="container py-5">
        <div className="text-center mb-5">
          <h1 className="display-4 fw-bold text-primary">🤖 AI Resume Analyzer</h1>
          <p className="lead text-muted">Analyze resume-job compatibility using AI-powered insights</p>
        </div>

        <div className="row">
          <div className="col-lg-6 mb-4">
            <div className="card shadow-sm h-100">
              <div className="card-header bg-primary text-white">
                <h5 className="mb-0">📄 Resume Input</h5>
              </div>
              <div className="card-body">
                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label className="form-label fw-bold">Upload Resume</label>
                    <input
                      type="file"
                      className="form-control"
                      accept=".pdf,.doc,.docx,.txt"
                      onChange={handleFileChange}
                    />
                    <small className="text-muted">Supported: PDF, DOC, DOCX, TXT (Max 10MB)</small>
                  </div>

                  <div className="text-center my-3">
                    <span className="badge bg-secondary">OR</span>
                  </div>

                  <div className="mb-3">
                    <label className="form-label fw-bold">Paste Resume Text</label>
                    <textarea
                      className="form-control"
                      rows="6"
                      value={resumeText}
                      onChange={(e) => {
                        setResumeText(e.target.value);
                        setResumeFile(null);
                      }}
                      placeholder="Paste your resume content here..."
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label fw-bold">Job Title *</label>
                    <input
                      type="text"
                      className="form-control"
                      value={jobTitle}
                      onChange={(e) => setJobTitle(e.target.value)}
                      placeholder="e.g., Senior Python Developer"
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label fw-bold">Job Description (Optional)</label>
                    <textarea
                      className="form-control"
                      rows="4"
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                      placeholder="Enter job requirements and responsibilities..."
                    />
                  </div>

                  <button
                    type="submit"
                    className="btn btn-primary btn-lg w-100"
                    disabled={loading || !jobTitle || (!resumeText && !resumeFile)}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2"></span>
                        Analyzing...
                      </>
                    ) : (
                      '🚀 Analyze Fit'
                    )}
                  </button>
                </form>
              </div>
            </div>
          </div>

          <div className="col-lg-6">
            <div className="card shadow-sm h-100">
              <div className="card-header bg-success text-white">
                <h5 className="mb-0">📊 Analysis Results</h5>
              </div>
              <div className="card-body">
                {error && (
                  <div className="alert alert-danger" role="alert">
                    <strong>Error:</strong> {error}
                  </div>
                )}

                {!result && !error && !loading && (
                  <div className="text-center text-muted py-5">
                    <i className="bi bi-clipboard-data" style={{ fontSize: '4rem' }}></i>
                    <p className="mt-3">Results will appear here after analysis</p>
                  </div>
                )}

                {loading && (
                  <div className="text-center py-5">
                    <div className="spinner-border text-primary" style={{ width: '3rem', height: '3rem' }}></div>
                    <p className="mt-3 text-muted">Analyzing your resume with AI...</p>
                  </div>
                )}

                {result && (
                  <div className="results-container">
                    <div className="text-center mb-4">
                      <h2 className="display-3 fw-bold" style={{ color: getScoreColor(result.similarity_score) }}>
                        {result.similarity_score}%
                      </h2>
                      <p className="text-muted">Compatibility Score</p>
                    </div>

                    <div className="mb-4">
                      <h6 className="fw-bold text-primary">📝 Detailed Analysis</h6>
                      <div className="bg-light p-3 rounded" style={{ whiteSpace: 'pre-line' }}>
                        {result.fit_explanation}
                      </div>
                    </div>

                    {result.extracted_skills && result.extracted_skills.length > 0 && (
                      <div className="mb-4">
                        <h6 className="fw-bold text-primary">💼 Extracted Skills</h6>
                        <div className="d-flex flex-wrap gap-2">
                          {result.extracted_skills.map((skill, index) => (
                            <span key={index} className="badge bg-info">{skill}</span>
                          ))}
                        </div>
                      </div>
                    )}

                    {result.experience && result.experience.total_years > 0 && (
                      <div className="mb-4">
                        <h6 className="fw-bold text-primary">⏱️ Experience</h6>
                        <p className="mb-0">{result.experience.total_years} years of experience detected</p>
                      </div>
                    )}

                    <div className="text-end">
                      <small className="text-muted">
                        Analysis method: {result.analysis_method} | 
                        Processing time: {result.processing_time}s
                      </small>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="text-center mt-5">
          <p className="text-muted">
            <small>Powered by Django REST API + LangChain + OpenAI</small>
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
