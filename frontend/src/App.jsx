import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSummary('');
    setError('');
    const formData = new FormData();
    if (file) formData.append('file', file);
    if (url) formData.append('url', url);
    formData.append('geminiApiKey', apiKey);
    try {
      const res = await fetch('/mcp', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (data.summary) setSummary(data.summary);
      else setError(data.error || 'Unknown error');
    } catch (err) {
      setError('Failed to summarize.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Summarization Tool</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>PDF File: </label>
          <input type="file" accept="application/pdf" onChange={e => setFile(e.target.files[0])} />
        </div>
        <div>
          <label>or Paper URL: </label>
          <input type="url" value={url} onChange={e => setUrl(e.target.value)} placeholder="https://..." />
        </div>
        <div>
          <label>Gemini API Key: </label>
          <input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)} required />
        </div>
        <button type="submit" disabled={loading}>{loading ? 'Summarizing...' : 'Summarize'}</button>
      </form>
      {summary && (
        <div className="summary">
          <h2>Summary</h2>
          <pre>{summary}</pre>
        </div>
      )}
      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default App; 