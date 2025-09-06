import React, { useState, useEffect, useRef } from "react";
import ReactDOM from "react-dom/client";
import { marked } from "marked";

function App() {
  const [url, setUrl] = useState("");
  const [logs, setLogs] = useState([]);
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
    setLogs([{ type: "info", content: "Starting conversion..." }]);

    const response = await fetch("/convert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");
      for (const line of lines) {
        if (line.startsWith("data:")) {
          const data = JSON.parse(line.substring(5));
          const logType = data.content.includes("**Error**") ? "error" : "info";
          setLogs((prev) => [...prev, { type: logType, content: data.content }]);
        }
      }
    }

    setLogs((prev) => [...prev, { type: "success", content: "\nConversion complete!" }]);
    setIsConverting(false);
    setConversionComplete(true);
  };

  const downloadCode = async () => {
    const response = await fetch("/download");
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "website.zip";
    a.click();
  };

  const copyLogsToClipboard = () => {
    const logText = logs.map((log) => log.content).join("\n");
    navigator.clipboard.writeText(logText);
  };

  const renderLog = (log, index) => {
    const htmlContent = marked(log.content);
    let prefix = "$";
    let textColor = "text-white";

    if (log.type === "error") {
      prefix = "!";
      textColor = "text-red-400";
    } else if (log.type === "success") {
      prefix = "+";
      textColor = "text-green-400";
    }

    return (
      <div key={index} className={`flex items-start ${textColor}`}>
        <pre data-prefix={prefix} className="mr-2"></pre>
        <code dangerouslySetInnerHTML={{ __html: htmlContent }} />
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans">
      <div className="container mx-auto p-4 md:p-8">
        <header className="text-center mb-10">
          <h1 className="text-5xl font-bold text-cyan-400">Drupal Headless Converter</h1>
          <p className="text-xl text-gray-400 mt-3">
            Seamlessly migrate your Drupal site to a modern, static architecture.
          </p>
        </header>

        <div className="bg-gray-800 shadow-2xl rounded-xl p-6 md:p-8 mb-10">
          <div className="flex flex-col md:flex-row items-center gap-4">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter Drupal URL (e.g., https://www.drupal.org)"
              className="input input-bordered w-full p-3 text-lg bg-gray-700 border-gray-600 focus:ring-cyan-500 focus:border-cyan-500"
            />
            <div className="flex gap-4">
              <button
                className="btn btn-primary btn-lg bg-cyan-500 hover:bg-cyan-600 border-none"
                onClick={startConversion}
                disabled={isConverting}
              >
                {isConverting ? (
                  <>
                    <span className="loading loading-spinner"></span>
                    Converting...
                  </>
                ) : "Start Conversion"}
              </button>
              <button
                className={`btn btn-secondary btn-lg border-none ${
                  conversionComplete ? "bg-green-500 hover:bg-green-600 animate-pulse" : "bg-gray-600 hover:bg-gray-700"
                }`}
                onClick={downloadCode}
                disabled={!conversionComplete}
              >
                Download Code
              </button>
            </div>
          </div>
        </div>

        <div className="relative">
          <div className="mockup-code bg-gray-800 text-sm shadow-2xl">
            <div className="p-4 h-96 overflow-y-auto">
              {logs.map(renderLog)}
              <div ref={logsEndRef} />
            </div>
          </div>
          <button className="absolute top-2 right-2 btn btn-sm btn-ghost" onClick={copyLogsToClipboard}>
            Copy Logs
          </button>
        </div>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
