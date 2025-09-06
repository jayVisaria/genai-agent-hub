import React from "react";
import { marked } from "marked";

const LogOutput = ({ logs, logsEndRef }) => {
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
    <div className="mockup-code bg-gray-800 text-sm shadow-2xl">
      <div className="p-4 h-96 overflow-y-auto">
