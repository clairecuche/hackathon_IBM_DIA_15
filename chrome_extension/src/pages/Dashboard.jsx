import React from "react";
import Consumption from "../components/consuption.jsx";
import ConsumptionSelector from "../components/consuption_selector.jsx";
import TreeFill from "../components/tree.jsx";
import GoogleResearch from "../components/googlesearch.jsx";

const DashboardPage = () => {
  return (
    <div style={{ width: "100%", padding: "16px", boxSizing: "border-box" }}>
      <div style={{ borderBottom: "1px solid #CBC9C9", paddingBottom: "8px" }}>
        <h2>This week</h2>
        <p>Nice chart</p>
        <Consumption value={5} />
      </div>

      <div style={{ marginTop: "16px" }}>
        <ConsumptionSelector />
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "12px",
            marginTop: "12px",
            justifyContent: "center", // centre verticalement si hauteur définie
            alignItems: "center",     // centre horizontalement
          }}
        >
          {/* Taille réduite pour correspondre à LeafFill */}
          <TreeFill value={70} size={60} />
          <GoogleResearch count={42} />
          <p
      style={{
        display: "flex",
        alignItems: "center",
        width: "fit-content",
        gap: "12px",
        fontFamily: "'Poppins', sans-serif",
        fontSize: "14px",
        color: "#212121",
        padding: "8px 12px",
        border: "1px solid #FCFBFC",
        borderRadius: "8px",
        boxSizing: "border-box",

        backgroundColor: "#FCFBFC",
      }}
    >
            {70} hectares of forest</p>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
