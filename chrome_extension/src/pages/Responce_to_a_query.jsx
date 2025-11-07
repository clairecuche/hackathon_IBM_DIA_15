import React from "react";
import Back from "../components/back.jsx";
import Consumption from "../components/consuption.jsx";
import GoogleResearch from "../components/googlesearch.jsx";
import LeafFill from "../components/leaf.jsx";

const ResponseToAQuery = ({ 
  query, 
  selectedZone, 
  onTabChange, 
  setCurrentQuery,
  responseText,          
  amountConsumption,
  hectareEq,
  pourcentage
}) => {
  return (
    <div
      style={{
        width: "100%",
        padding: "16px",
        boxSizing: "border-box",
        gap: "12px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Bouton Back */}
      <Back onClick={() => {
        setCurrentQuery("");
        onTabChange("query");
      }} />

      <div style={{ borderBottom: "1px solid #CBC9C9", paddingBottom: "8px" }}>
        <h3 style={{ padding: "12px 0px 6px 0px" }}>Your query</h3>
        <p>{query}</p>

        <h3 style={{ padding: "12px 0px 6px 0px" }}>Selected country</h3>
        <p>{selectedZone || "No country selected"}</p>

        <h3 style={{ padding: "12px 0px 6px 0px" }}>Response from Llama</h3>
        <p>{responseText || "Aucune réponse disponible"}</p>

        {/* Consommation d'énergie */}
        <Consumption value={amountConsumption} />
      </div>

      <div style={{ marginTop: "16px" }}>
        <h2>Your consumption today</h2>

        <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginTop: "12px", justifyContent: "center", alignItems: "center" }}>
          <GoogleResearch count={Math.round(pourcentage)} />
          <LeafFill value={hectareEq} />
        </div>
      </div>
    </div>
  );
};

export default ResponseToAQuery;
