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
        backgroundColor: disabled ? "#71B071" : "#71B071",
        color: "#FCFBFC",
        cursor: disabled ? "#B8D7B8" : "pointer",
        margin: "0px",
      }}
    >
      {label}
    </button>
  );
};

export default Button;
