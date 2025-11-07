// src/components/Button.jsx
import React from "react";

const Button = ({ label, onClick, disabled }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        padding: "10px 10px",
        borderRadius: "8px",
        border: "none",
        backgroundColor: "#71B071",
        color: "#FCFBFC",
        cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.5 : 1,
        transition: "opacity 0.3s",
        margin: "0px",
      }}
    >
      {label}
    </button>
  );
};

export default Button;
