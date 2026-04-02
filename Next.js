'use client';
import { useState } from 'react';

export default function Home() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleHumanize = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/humanize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText })
      });
      const data = await response.json();
      setOutputText(data.result);
    } catch (error) {
      setOutputText("Error connecting to the AI.");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '50px', maxWidth: '800px', margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1>🤖 AI to Human Text Converter</h1>
      <textarea 
        rows="8" 
        style={{ width: '100%', marginBottom: '20px', padding: '10px' }} 
        placeholder="Paste your AI text here..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <button 
        onClick={handleHumanize} 
        disabled={loading}
        style={{ padding: '10px 20px', cursor: 'pointer', backgroundColor: '#0070f3', color: 'white', border: 'none', borderRadius: '5px' }}>
        {loading ? 'Humanizing...' : 'Humanize Text'}
      </button>
      <h2 style={{ marginTop: '30px' }}>Humanized Output:</h2>
      <div style={{ minHeight: '100px', padding: '20px', backgroundColor: '#f5f5f5', borderRadius: '5px' }}>
        {outputText}
      </div>
    </div>
  );
}
