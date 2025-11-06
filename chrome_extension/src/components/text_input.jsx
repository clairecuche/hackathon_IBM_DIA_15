// src/components/TextInput.jsx
import React from "react";

const TextInput = ({ label, value, onChange, placeholder = "", disabled = false }) => {
  return (
    <div style={{ marginBottom: "12px" }}>
      {label && <label style={{ display: "block", marginBottom: "4px", fontWeight: 500 }}>{label}</label>}
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        style={{
          width: "100%",
          padding: "8px 12px",
          borderRadius: "8px",
          border: "1px solid #ccc",
          fontFamily: "'Poppins', sans-serif",
          fontSize: "14px",
          outline: "none",
          backgroundColor: disabled ? "#f0f0f0" : "white",
          opacity: disabled ? 0.6 : 1,
          boxSizing: "border-box",
        }}
      />
    </div>
  );
};

export default TextInput;
