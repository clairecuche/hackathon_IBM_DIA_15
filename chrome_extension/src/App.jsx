// src/App.jsx
import React, { useState } from "react";
import Button from "./components/button.jsx";

function App() {
  const [query, setQuery] = useState("");

  return (
    <div style={{ padding: "16px", width: "300px", fontFamily: "'Poppins', sans-serif" }}>
      <h2>LLM CO2 Tracker</h2>

      <Button
        label="Submit"
        onClick={() => alert(`Votre requête : ${query}`)}
        disabled={query.trim() === ""}
      />
    </div>
  );
}

export default App;
