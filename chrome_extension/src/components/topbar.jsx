// src/components/TopBar.jsx
import React from "react";

// Tu peux remplacer ces images par tes icônes réelles
import people_img from "../assets/people.png";
import settings_img from "../assets/settings.png";
import cross_img from "../assets/cross.png";
//import extensionIcon from "../assets/extension_icon.png";

const TopBar = () => {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        width: "100%",
        padding: "8px 12px",
        backgroundColor: "#f8f8f8",
        boxSizing: "border-box",
        borderBottom: "1px solid #e0e0e0",
      }}
    >
      {/* Icône de l’extension à gauche */}
      <img
        src="/icon.png"
        alt="Extension Icon"
        style={{ width: "32px", height: "32px" }}
      />

      {/* Boutons à droite */}
      <div style={{ display: "flex", alignItems: "center", gap: "0px" }}>
        <button
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "4px 8px",
            border: "none",
            background: "transparent",
            cursor: "pointer",
          }}
        >
          <img src={people_img} alt="Icon 1" style={{ width: "30px", height: "30px" }} />
        </button>

        {/* Séparateur vertical */}
        <div
          style={{
            width: "1px",
            height: "24px",
            backgroundColor: "#ccc",
            margin: "0 4px",
          }}
        />

        <button
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "4px 8px",
            border: "none",
            background: "transparent",
            cursor: "pointer",
          }}
        >
          <img src={settings_img} alt="Icon 2" style={{ width: "30px", height: "30px" }} />
        </button>

        <div
          style={{
            width: "1px",
            height: "24px",
            backgroundColor: "#ccc",
            margin: "0 4px",
          }}
        />

        <button
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "4px 8px",
            border: "none",
            background: "transparent",
            cursor: "pointer",
          }}
        >
          <img src={cross_img} alt="Icon 3" style={{ width: "30px", height: "30px" }} />
        </button>
      </div>
    </div>
  );
};

export default TopBar;
