import React, { useState } from "react";
import Button from "./components/button.jsx";
import TextInput from "./components/text_input.jsx";
import Back from "./components/back.jsx";
import NavBar from "./components/nav_bar.jsx";

function App() {
  const [query, setQuery] = useState("");
  const [activeTab, setActiveTab] = useState("query"); // ✅ ajout de l’état

  return (
    <div style={{ padding: "16px", width: "300px", fontFamily: "'Poppins', sans-serif" }}>
      <h2>LLM CO2 Tracker</h2>

      <NavBar activeTab={activeTab} onTabChange={setActiveTab} />

      <div style={{ padding: "16px 0" }}>
        <Back onClick={() => alert("Retour !")} />
      </div>

      <TextInput
        label="Requête LLM"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
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
