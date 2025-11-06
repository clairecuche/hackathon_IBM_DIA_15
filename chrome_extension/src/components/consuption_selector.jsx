// src/components/ConsumptionSelector.jsx
import React, { useState, useRef, useEffect } from "react";

const options = ["weekly", "monthly", "yearly"];

const ConsumptionSelector = () => {
  const [selected, setSelected] = useState("weekly");
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef();

  // Fermer le dropdown quand on clique en dehors
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
      style={{ position: "relative", width: "200px", margin: "16px 0" }}
    >
      <button
        onClick={() => setOpen(!open)}
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          justifyContent: "center",
          padding: "8px 12px",
          borderRadius: "8px",
          border: "1px solid transparent",
          backgroundColor: "#FCFBFC",
          fontFamily: "'Poppins', sans-serif",
          cursor: "pointer",
          color: "#212121",
          fontSize: "16px",
          outline: "none", // supprime le contour au clic
        }}
      >
        <span style={{ fontSize: "16px", color: "#212121" }}>Your consommation</span>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "4px",
            fontSize: "16px",
            fontWeight: 500,
          }}
        >
          <span>{selected}</span>
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
        </div>
      </button>

      {open && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            width: "100%",
            borderRadius: "8px",
            backgroundColor: "#FCFBFC",
            marginTop: "4px",
            zIndex: 1000,
            boxShadow: "0 2px 6px rgba(0,0,0,0.15)",
            overflow: "hidden",
          }}
        >
          {options.map((option, index) => (
            <div
              key={option}
              onClick={() => {
                setSelected(option);
                setOpen(false);
              }}
              style={{
                padding: "8px 12px",
                cursor: "pointer",
                fontFamily: "'Poppins', sans-serif",
                fontSize: "16px",
                color: "#212121",
                position: "relative",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#ECECEC")}
              onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#FCFBFC")}
            >
              {option}
              {/* Border-bottom partiel, sauf pour le dernier élément */}
              {index !== options.length - 1 && (
                <div
                  style={{
                    position: "absolute",
                    bottom: 0,
                    left: "12px",
                    right: "12px",
                    height: "1px",
                    backgroundColor: "#E0E0E0",
                  }}
                />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ConsumptionSelector;
