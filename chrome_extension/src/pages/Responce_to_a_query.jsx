import React from "react";
import Back from "../components/back.jsx";
import Consumption from "../components/consuption.jsx"; // ou ConsumptionWithSignal si tu veux les barres
import GoogleResearch from "../components/googlesearch.jsx"; // <-- nouveau composant
import LeafFill from "../components/leaf.jsx";

const ResponseToAQuery = ({ query, onTabChange, setCurrentQuery }) => {
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
      {/* ----------------------------
          Bouton Back
          ---------------------------- */}
      <Back
        onClick={() => {
          setCurrentQuery(""); // réinitialise la variable
          onTabChange("query"); // revient à la page query
        }}
      />

      <div style={{ borderBottom: "1px solid #CBC9C9", paddingBottom: "8px" }}>
        <h3 style={{ padding: "12px 0px 6px 0px", borderBottom: "0px solid #CBC9C9" }}>
          Your query
        </h3>
        <p>{query}</p>

        <h3 style={{ padding: "12px 0px 6px 0px", borderBottom: "0px solid #CBC9C9" }}>
          Response from Llama
        </h3>
        <p>La réponse de chat</p>

        {/* Consommation affichée avec valeur */}
        <Consumption value={27} />
      </div>

      <div style={{ marginTop: "16px" }}>
        <h2>Your consumption today</h2>

        {/* ----------------------------
            Google Research
            ---------------------------- */}
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
          <GoogleResearch count={15} /> 
          <LeafFill value={50} />
        </div>
      </div>
    </div>
  );
};

export default ResponseToAQuery;

