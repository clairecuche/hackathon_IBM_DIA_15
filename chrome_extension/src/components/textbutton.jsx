// src/components/TextButton.jsx
import React, { useState } from "react";

const TextButton = ({ label, onClick, color = "#A8A8A8" }) => {
  const [isHovered, setIsHovered] = useState(false);
  const [isActive, setIsActive] = useState(false);

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onMouseDown={() => setIsActive(true)}
      onMouseUp={() => setIsActive(false)}
      style={{
        background: "transparent",
        border: "none",
        padding: 0,
        fontFamily: "'Poppins', sans-serif",
        fontSize: "14px",
        color: color,
        textDecoration: isActive ? "underline" : "none", // souligné au clic
        cursor: "pointer",
        outline: "none",
        transition: "all 0.2s ease",
        textShadow: isHovered ? "1px 1px 2px rgba(0,0,0,0.15)" : "none", // ✅ drop shadow au hover
      }}
    >
      {label}
    </button>
  );
};

export default TextButton;
