import React, { useRef, useEffect, useState } from "react";

const NavBar = ({ activeTab = "query", onTabChange }) => {
  const tabs = [
    { id: "query", label: "Query" },
    { id: "dashboard", label: "Dashboard" },
  ];

  const [lineStyle, setLineStyle] = useState({ left: 0, width: 0 });
  const navRef = useRef(null);

  useEffect(() => {
    // Calcule la position et largeur du bouton actif
    const activeButton = navRef.current.querySelector(
      `button[data-id='${activeTab}']`
    );
    if (activeButton) {
      setLineStyle({
        left: activeButton.offsetLeft,
        width: activeButton.offsetWidth,
      });
    }
  }, [activeTab]);

  return (
    <nav
      ref={navRef}
      style={{
        display: "flex",
        justifyContent: "space-around",
        width: "100%",
        backgroundColor: "#F1F7F1",
        fontFamily: "'Poppins', sans-serif",
        borderRadius: "8px",
        overflow: "hidden",
        position: "relative", // ✅ nécessaire pour la ligne active
      }}
    >
      {tabs.map((tab) => (
        <button
          key={tab.id}
          data-id={tab.id}
          onClick={() => onTabChange(tab.id)}
          style={{
            flex: 1,
            padding: "10px 0",
            background: "transparent",
            border: "none",
            color: activeTab === tab.id ? "#527F52" : "#71B071",
            fontWeight: activeTab === tab.id ? 600 : 400,
            cursor: "pointer",
            position: "relative",
            fontSize: "14px",
            outline: "none",
          }}
        >
          {tab.label}
        </button>
      ))}

      {/* Ligne active animée */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: lineStyle.left,
          width: lineStyle.width,
          height: "2px",
          backgroundColor: "#527F52",
          transition: "left 0.3s ease, width 0.3s ease", // ✅ animation fluide
        }}
      />
    </nav>
  );
};

export default NavBar;
