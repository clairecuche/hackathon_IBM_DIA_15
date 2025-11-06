import React, { useState } from "react";
import TextInput from "../components/text_input.jsx";
import Button from "../components/button.jsx";

const HomePage = ({ onTabChange, setCurrentQuery }) => {
  const [query, setQuery] = useState("");

  return (
    <div style={{ width: "100%", padding: "16px", boxSizing: "border-box" }}>
      <h2>LLM CO2 Tracker</h2>
      <TextInput
          label="Requête LLM"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your query here..."
        />
        <Button
          label="Send"
          disabled={query === ""} // bouton désactivé si rien tapé
          onClick={() => {setCurrentQuery(query); onTabChange("response")}} // passe à la page ResponseToAQuery
        />
      </div>
    );
};

export default HomePage;
