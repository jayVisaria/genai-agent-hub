import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  const [url, setUrl] = useState('');
  const [logs, setLogs] = useState('Logs will appear here...');
  const [isConverting, setIsConverting] = useState(false);

  const startConversion = async () => {
    setIsConverting(true);
    setLogs('');

    const response = await fetch('/convert', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value);
      const lines = chunk.split('
      for (const line of lines) {
        if (line.startsWith('data:')) {
          const data = JSON.parse(line.substring(5));
          setLogs((prev) => prev + data.content);
        }
      }
    }

    setIsConverting(false);
  };

  const downloadCode = async () => {
    // To be implemented in step 9
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Drupal to Headless CMS Converter</h1>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter Drupal URL"
          className="input input-bordered w-full max-w-xs"
        />
        <button className="btn btn-primary" onClick={startConversion} disabled={isConverting}>
          {isConverting ? 'Converting...' : 'Start Conversion'}
        </button>
        <button className="btn btn-secondary" onClick={downloadCode}>
          Download Code
        </button>
      </div>
      <div className="mockup-code">
        <pre data-prefix="$">
          <code>{logs}</code>
        </pre>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);


