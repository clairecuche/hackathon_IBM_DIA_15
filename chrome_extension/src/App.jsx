// src/App.jsx
import React, { useState } from "react";
import Button from "./components/button.jsx";
import TextInput from "./components/text_input.jsx";
import Back from "./components/back.jsx";
import NavBar from "./components/nav_bar.jsx";
import DropdownButton from "./components/dropdown_button.jsx";
import TopBar from "./components/topbar.jsx";
import ConsumptionSelector from "./components/consuption_selector.jsx";
import TextButton from "./components/textbutton.jsx";

function App() {
  const [query, setQuery] = useState("");
  const [activeTab, setActiveTab] = useState("query"); // état pour NavBar

  return (
    <div
      style={{
        padding: "16px",
        width: "300px",
        fontFamily: "'Poppins', sans-serif",
        backgroundColor: "#FCFBFC", 
      }}
    >
      {/* TopBar */}
      <TopBar />

      <h2 style={{ marginBottom: "16px", marginTop: "16px", color: "#212121" }}>LLM CO2 Tracker</h2>

      {/* NavBar */}
      <NavBar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Dropdown */}
      <div style={{ margin: "16px 0" }}>
        <DropdownButton initialText="Choisir une option" />
      </div>

      {/* ConsumptionSelector */}
      <div style={{ margin: "16px 0" }}>
        <ConsumptionSelector />
      </div>

      {/* Bouton TextButton */}
      <div style={{ margin: "16px 0" }}>
        <TextButton
          label="Déconnexion"
          onClick={() => alert("TextButton cliqué !")}
        />
      </div>

      {/* Bouton Back */}
      <div style={{ padding: "16px 0" }}>
        <Back onClick={() => alert("Retour !")} />
      </div>

      {/* Input texte */}
      <TextInput
        label="Requête LLM"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Tapez votre texte ici..."
      />

      {/* Bouton Submit */}
      <Button
        label="Submit"
        onClick={() => alert(`Votre requête : ${query}`)}
        disabled={query.trim() === ""}
      />
    </div>
  );
}

export default App;
