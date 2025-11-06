// src/components/DropdownButton.jsx
import React, { useState, useRef, useEffect } from "react";

const DropdownButton = ({ initialText = "Sélectionner une option" }) => {
  const optionsData = [
    { id: 1, label: "France" },
    { id: 2, label: "Irlande" },
    { id: 3, label: "Allemagne" },
  ];

  const [selected, setSelected] = useState(initialText);
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef();

  // Fermer le menu si clic en dehors
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div
      ref={dropdownRef}
      style={{
        position: "relative",
        width: "100%",
        margin: "16px 0",
        color : "#212121",
      }}
    >
      {/* Bouton principal */}
      <button
        onClick={() => setOpen(!open)}
        style={{
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "8px 12px",
          borderRadius: "8px",
          border: "0px solid #FCFBFC",
          backgroundColor: "#FCFBFC",
          fontFamily: "'Poppins', sans-serif",
          cursor: "pointer",
          color : "#212121",
        }}
      >
        {selected}
        {/* Chevron maison */}
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          style={{
            transform: open ? "rotate(180deg)" : "rotate(0deg)",
            transition: "transform 0.2s ease",
          }}
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {/* Menu déroulant */}
      {open && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            width: "100%",
            border: "0px solid #FCFBFC",
            borderRadius: "8px",
            backgroundColor: "#FCFBFC",
            marginTop: "4px",
            zIndex: 1000,
            boxShadow: "0 2px 6px rgba(0,0,0,0.15)",
            borderRadius: "8px",
          }}
        >
          {optionsData.map((option) => (
            <div
              key={option.id}
              onClick={() => {
                setSelected(option.label);
                setOpen(false);
              }}
              style={{
                padding: "8px 12px",
                cursor: "pointer",
                fontFamily: "'Poppins', sans-serif",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#f0f0f0")}
              onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#fff")}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DropdownButton;
