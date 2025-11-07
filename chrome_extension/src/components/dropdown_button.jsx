import React, { useState } from "react";


const DropdownButton = ({ selected, setSelected, initialText = "Select an option" }) => {
  const optionsData = [
    { id: 1, label: "France" },
    { id: 2, label: "Irlande" },
    { id: 3, label: "Allemagne" },
  ];

  const [open, setOpen] = useState(false);

  // Valeur affichée : si selected est vide, afficher initialText
  const displayText = selected || initialText;

  return (
    <div style={{ position: "relative", width: "100%", margin: "16px 0", color: "#212121" }}>
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
          color: "#212121",
        }}
      >
        {displayText}
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
             style={{ transform: open ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.2s ease" }}>
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {open && (
        <div style={{ position: "absolute", top: "100%", left: 0, width: "100%", backgroundColor: "#FCFBFC", marginTop: "4px", zIndex: 1000, boxShadow: "0 2px 6px rgba(0,0,0,0.15)", borderRadius: "8px" }}>
          {optionsData.map((option) => (
            <div
              key={option.id}
              onClick={() => {
                setSelected(option.label); // <-- met à jour la valeur dans App.jsx
                setOpen(false);
              }}
              style={{ padding: "8px 12px", cursor: "pointer", fontFamily: "'Poppins', sans-serif" }}
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
