import React from "react";

const NavBar = ({ activeTab = "query", onTabChange }) => {
  const tabs = [
    { id: "query", label: "Query" },
    { id: "dashboard", label: "Dashboard" },
  ];

  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",
        width: "100%", // ✅ prend toute la largeur
        backgroundColor: "#F1F7F1",
        fontFamily: "'Poppins', sans-serif",
        borderRadius: "8px",
        overflow: "hidden",
      }}
    >
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          style={{
            flex: 1, // ✅ chaque bouton prend 50%
            padding: "10px 0",
            background: "transparent",
            border: "none",
            borderBottom:
              activeTab === tab.id ? "2px solid #527F52" : "2px solid transparent", // ✅ souligne l’actif
            color: activeTab === tab.id ? "#527F52" : "#71B071",
            fontWeight: activeTab === tab.id ? 600 : 400,
            cursor: "pointer",
            transition: "all 0.2s ease",
            borderRadius: "0px",
          }}
        >
          {tab.label}
        </button>
      ))}
    </nav>
  );
};

export default NavBar;
