import React from "react";

const Back = ({ onClick, disabled = false }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        display: "flex",
        alignItems: "center",
        gap: "5px",
        backgroundColor: "transparent",
        border: "none",
        cursor: disabled ? "not-allowed" : "pointer",
        color: disabled ? "#A8A8A8" : "#A8A8A8",
        padding: "4px 0px",
        fontFamily: "'Poppins', sans-serif",
        fontSize: "14px",
        fontWeight: 500,
        transition: "color 0.2s ease",
        textAlign: "left", 
      }}
    >
      {/* Chevron gauche SVG */}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke={disabled ? "#A8A8A8" : "#A8A8A8"}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <polyline points="15 18 9 12 15 6" />
      </svg>

      Back
    </button>
  );
};

export default Back;
