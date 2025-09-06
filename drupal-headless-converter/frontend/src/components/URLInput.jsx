import React from "react";

const URLInput = ({ url, setUrl, startConversion, isConverting, downloadCode, conversionComplete }) => (
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
          className="btn btn-secondary btn-lg bg-gray-600 hover:bg-gray-700 border-none"
          onClick={downloadCode}
          disabled={!conversionComplete}
        >
          Download Code
        </button>
      </div>
    </div>
  </div>
);
