import React from "react";

const GoogleResearch = ({ count }) => { 
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        width: "fit-content",
        gap: "12px",
        fontFamily: "'Poppins', sans-serif",
        fontSize: "14px",
        color: "#212121",
        padding: "8px 12px",
        border: "1px solid #FCFBFC",
        borderRadius: "8px",
        boxSizing: "border-box",

        backgroundColor: "#FCFBFC",
      }}
    >
      {/* Icône loupe */}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="#333"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>

      {/* Texte avec variable */}
      <span>
        {<div>{Math.max(count, 1)}</div>} Google Research
      </span>
    </div>
  );
};

export default GoogleResearch;