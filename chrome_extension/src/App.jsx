// src/App.jsx
import React, { useState } from "react";
import TopBar from "./components/topbar.jsx";
import NavBar from "./components/nav_bar.jsx";
import HomePage from "./pages/homepage.jsx";
import DashboardPage from "./pages/Dashboard.jsx";
import ResponseToAQuery from "./pages/Responce_to_a_query.jsx";
import Settings from "./pages/Settings.jsx";

function App() {
  const [activeTab, setActiveTab] = useState("settings"); // première page : settings
  const [currentQuery, setCurrentQuery] = useState("");
  const [selectedZone, setSelectedZone] = useState("");

  // Fonction pour envoyer les données au backend
  const sendToBackend = async (query, country) => {
    if (!query || !country) {
      alert("Veuillez remplir la requête et sélectionner un pays !");
      return;
    }

    const payload = { query, country };

    try {
      const response = await fetch("https://ton-backend.com/api/endpoint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error(`Erreur: ${response.status}`);
      const data = await response.json();
      console.log("Réponse du backend :", data);
      alert("Données envoyées avec succès !");
    } catch (error) {
      console.error("Erreur lors de l'envoi :", error);
      alert("Erreur lors de l'envoi au backend.");
    }
  };

  return (
    <div
      style={{
        width: "100%",
        minHeight: "100vh",
        fontFamily: "'Poppins', sans-serif",
        backgroundColor: "#FCFBFC",
        margin: 0,
        padding: 0,
        boxSizing: "border-box",
      }}
    >
      <TopBar onTabChange={setActiveTab} />
      <NavBar activeTab={activeTab} onTabChange={setActiveTab} />

      <div style={{ width: "100%" }}>
        {activeTab === "settings" && (
          <Settings
            onTabChange={setActiveTab}
            selectedZone={selectedZone}
            setSelectedZone={setSelectedZone}
          />
        )}

        {activeTab === "query" && (
          <HomePage
            onTabChange={setActiveTab}
            setCurrentQuery={setCurrentQuery}
            sendToBackend={sendToBackend}
            selectedZone={selectedZone} // pour vérifier la sélection du pays
          />
        )}

        {activeTab === "dashboard" && (
          <DashboardPage onTabChange={setActiveTab} />
        )}

        {activeTab === "response" && (
          <ResponseToAQuery
            query={currentQuery}
            onTabChange={setActiveTab}
            setCurrentQuery={setCurrentQuery}
            selectedZone={selectedZone} // pour l’afficher dans ResponseToAQuery
          />
        )}
      </div>
    </div>
  );
}

export default App;
