import React, { useState, useRef, useEffect } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  const [url, setUrl] = useState('');
  const [logs, setLogs] = useState('Logs will appear here...');
  const [isConverting, setIsConverting] = useState(false);
  const logsEndRef = useRef(null);

  const startConversion = async () => {
    if (!url) return;
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

    try {
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
    } catch (error) {
      setLogs((prev) => prev + '
      console.error('Error reading stream:', error);
    }

    setIsConverting(false);
  };

  const downloadCode = async () => {
    const response = await fetch('/download');
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'website.zip';
    a.click();
  };

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <div className="w-full max-w-4xl bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Drupal to Headless Converter
        </h1>
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter Drupal URL"
            className="input input-bordered w-full flex-grow"
            disabled={isConverting}
          />
          <button
            className="btn btn-primary w-full md:w-auto"
            onClick={startConversion}
            disabled={isConverting || !url}
          >
            {isConverting ? (
              <>
                <span className="loading loading-spinner"></span>
                Converting...
              </>
            ) : (
              'Start Conversion'
            )}
          </button>
          <button className="btn btn-secondary w-full md:w-auto" onClick={downloadCode}>
            Download Code
          </button>
        </div>
        <div className="mockup-code h-96 overflow-y-auto">
          <pre>
            <code>{logs}</code>
          </pre>
          <div ref={logsEndRef} />
        </div>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);




