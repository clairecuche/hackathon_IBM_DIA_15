// src/pages/HomePage.jsx
import React, { useState } from "react";
import NavBar from "../components/nav_bar.jsx";
import TextInput from "../components/text_input.jsx";

const HomePage = () => {
  const [query, setQuery] = useState("");

  return (
    <div style={{ width: "100%", padding: "16px", boxSizing: "border-box" }}>
      <h2>LLM CO2 Tracker</h2>
      <TextInput
        label="Requête LLM"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Tapez votre texte ici..."
      />
    </div>
  );
};

export default HomePage;