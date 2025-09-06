import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Drupal to Headless CMS Converter</h1>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          placeholder="Enter Drupal URL"
          className="input input-bordered w-full max-w-xs"
        />
        <button className="btn btn-primary">Start Conversion</button>
      </div>
      <div className="mockup-code">
        <pre data-prefix="$">
          <code>Logs will appear here...</code>
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

