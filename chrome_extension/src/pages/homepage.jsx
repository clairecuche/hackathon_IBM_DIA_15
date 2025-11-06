import React, { useState } from "react";
import TextInput from "../components/text_input.jsx";
import Button from "../components/button.jsx";

const HomePage = ({ onTabChange, setCurrentQuery, sendToBackend, selectedZone }) => {
  const [query, setQuery] = useState("");

  // bouton désactivé si query vide ou zone non sélectionnée
  const isDisabled = query === "" || selectedZone === "";

  return (
    <div
      style={{
        width: "100%",
        padding: "16px",
        boxSizing: "border-box",
        gap: "20px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <h2>Type your query</h2>
      <TextInput
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type your query here..."
      />
      <Button
        label="Send"
        disabled={isDisabled}
        onClick={() => {
          setCurrentQuery(query); // mettre à jour l'état pour ResponseToAQuery
          sendToBackend(query, selectedZone); // ⚡ passer les valeurs directement
          onTabChange("response"); // passe à la page ResponseToAQuery
        }}
      />
    </div>
  );
};

export default HomePage;
