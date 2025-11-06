import React, { useState } from "react";
import Button from "./components/button.jsx";
import TextInput from "./components/text_input.jsx";

function App() {
  const [query, setQuery] = useState("");

  return (
    <div style={{ padding: "16px", width: "300px", fontFamily: "'Poppins', sans-serif" }}>
      <h2>LLM CO2 Tracker</h2>

      <TextInput
        label="Requête LLM"
        value={query}
        onChange={(e) => setQuery(e.target.value)} // ✅ ici on gère bien l’événement
        placeholder="Tapez votre texte ici..."
      />

      <Button
        label="Submit"
        onClick={() => alert(`Votre requête : ${query}`)}
        disabled={query.trim() === ""}
      />
    </div>
  );
}

export default App;
