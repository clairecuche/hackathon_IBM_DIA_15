import React, { useState } from "react";

const TextInput = ({ label, value, onChange, placeholder = "", disabled = false }) => {
  const [isFocused, setIsFocused] = useState(false);

  return (
    <div style={{ marginBottom: "12px" }}>
      {label && (
        <label
          style={{
            display: "block",
            marginBottom: "4px",
            fontWeight: 500,
            fontFamily: "'Poppins', sans-serif",
          }}
        >
          {label}
        </label>
      )}

      <input
        type="text"
        value={value}
        onChange={onChange} // ✅ simple et correct
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder={isFocused ? "" : placeholder}
        disabled={disabled}
        style={{
          width: "100%",
          padding: "8px 12px",
          borderRadius: "8px",
          border: isFocused ? "1.5px solid #0078ff" : "1px solid #ccc",
          fontFamily: "'Poppins', sans-serif",
          fontSize: "14px",
          outline: "none",
          backgroundColor: disabled ? "#f0f0f0" : "white",
          color: "#000",
          opacity: disabled ? 0.6 : 1,
          boxSizing: "border-box",
          transition: "border-color 0.2s ease, box-shadow 0.2s ease",
          boxShadow: isFocused ? "0 0 4px rgba(0, 120, 255, 0.3)" : "none",
        }}
      />
    </div>
  );
};

export default TextInput;
