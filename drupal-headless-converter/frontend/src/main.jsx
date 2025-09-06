import React, { useState, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom/client';
import { marked } from 'marked';

function App() {
  const [url, setUrl] = useState('');
  const [logs, setLogs] = useState('');
  const [isConverting, setIsConverting] = useState(false);
  const [conversionComplete, setConversionComplete] = useState(false);
  const logsEndRef = useRef(null);

  const scrollToBottom = () => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [logs]);

  const startConversion = async () => {
    setIsConverting(true);
    setConversionComplete(false);
    setLogs('Starting conversion...\n');

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
      const lines = chunk.split('\n');
      for (const line of lines) {
        if (line.startsWith('data:')) {
          const data = JSON.parse(line.substring(5));
          setLogs((prev) => prev + data.content);
        }
      }
    }

    setLogs((prev) => prev + '\nConversion complete!\n');
    setIsConverting(false);
    setConversionComplete(true);
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

  return (
    <div className="container mx-auto p-4 font-sans">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800">Drupal to Headless CMS Converter</h1>
        <p className="text-lg text-gray-600 mt-2">
          Instantly convert your legacy Drupal site into a modern, headless CMS-powered static website.
        </p>
      </header>

      <div className="bg-white shadow-lg rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">Instructions</h2>
        <ol className="list-decimal list-inside text-gray-600 space-y-2">
          <li>Enter the full URL of the Drupal website you want to convert.</li>
          <li>Click "Start Conversion" to begin the process.</li>
          <li>The agent will first analyze the sitemap, then identify global elements (header, footer), and finally extract content from each page.</li>
          <li>Once the conversion is complete, you can download the generated code as a zip file.</li>
        </ol>
      </div>

      <div className="flex items-center gap-4 mb-8">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter Drupal URL (e.g., https://www.drupal.org)"
          className="input input-bordered w-full p-3 text-lg"
        />
        <button className="btn btn-primary btn-lg" onClick={startConversion} disabled={isConverting}>
          {isConverting ? (
            <>
              <span className="loading loading-spinner"></span>
              Converting...
            </>
          ) : 'Start Conversion'}
        </button>
        <button className="btn btn-secondary btn-lg" onClick={downloadCode} disabled={!conversionComplete}>
          Download Code
        </button>
      </div>

      <div className="mockup-code bg-gray-800 text-white">
        <pre data-prefix="$" className="p-4">
          <code dangerouslySetInnerHTML={{ __html: marked(logs) }} />
          <div ref={logsEndRef} />
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
