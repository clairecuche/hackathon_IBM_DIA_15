import React from "react";
import Back from "../components/back.jsx";

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
          setCurrentQuery("");    // réinitialise la variable
          onTabChange("query");   // revient à la page query
        }}
      />

      <h3 style={{ padding: "12px 0px 6px 0px", borderBottom: "1px solid #888" }}>
        Your query
      </h3>
      <p>{query}</p>

      <h3 style={{ padding: "12px 0px 6px 0px", borderBottom: "1px solid #888" }}>
        Response from Llama
      </h3>
      <p>La réponse de chat</p>
    </div>
  );
};

export default ResponseToAQuery;
