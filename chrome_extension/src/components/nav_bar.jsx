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
        position: "relative", // ✅ nécessaire pour la ligne
        width: "100%",
        backgroundColor: "#F1F7F1",
        fontFamily: "'Poppins', sans-serif",
        borderRadius: "8px",
        overflow: "hidden",
        padding: "0 0", // pas de padding vertical
      }}
    >
      {tabs.map((tab, index) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          style={{
            flex: 1,
            padding: "10px 0",
            background: "transparent",
            border: "none",
            color: activeTab === tab.id ? "#527F52" : "#71B071",
            fontWeight: activeTab === tab.id ? 600 : 400,
            cursor: "pointer",
            position: "relative", // ✅ pour positionner la ligne
            fontSize: "14px",
            transition: "color 0.5s ease",
          }}
        >
          {tab.label}

          {/* Ligne animée */}
          {activeTab === tab.id && (
            <div
              style={{
                position: "absolute",
                bottom: 0,
                left: 0,
                width: "100%",
                height: "2px",
                backgroundColor: "#527F52",
                borderRadius: "2px 2px 0 0",
                transition: "all 0.5s ease",
              }}
            />
          )}
        </button>
      ))}
    </nav>
  );
};

export default NavBar;
