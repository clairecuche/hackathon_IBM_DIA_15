// src/App.jsx
import React, { useState } from "react";
import TopBar from "./components/topbar.jsx";
import NavBar from "./components/nav_bar.jsx";
import HomePage from "./pages/homepage.jsx";
import DashboardPage from "./pages/Dashboard.jsx";
import ResponseToAQuery from "./pages/Responce_to_a_query.jsx";
import Settings from "./pages/Settings.jsx";

function App() {
  const [activeTab, setActiveTab] = useState("settings");
  const [currentQuery, setCurrentQuery] = useState("");
  const [selectedZone, setSelectedZone] = useState("");

  // States pour stocker la réponse du backend
  const [responseText, setResponseText] = useState("");
  const [amountConsumption, setAmountConsumption] = useState(0);
  const [hectareEq, setHectareEq] = useState(0);
  const [pourcentage, setPourcentage] = useState(0);

  const sendToBackend = async (query, country) => {
    if (!query || !country) {
      alert("Veuillez remplir la requête et sélectionner un pays !");
      return;
    }
    const prompt = query;
    const payload = { prompt, country, model_name :"llama3.2" , temperature:0.7};
    console.log("Envoi au backend :", payload);

   try {
    const response = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error(`Erreur: ${response.status}`);

    const data = await response.json();

    // Mapping des données du backend vers vos states
    setResponseText(data.llama_response);
    setAmountConsumption(data.energy_consumption_kwh);
    setHectareEq(data.equivalents.forest_area_acres);
    setPourcentage(data.equivalents.google_searches);

    console.log("Données reçues :", data);
    
    // Passer à la page de réponse
    setActiveTab("response");
    
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
            selectedZone={selectedZone}
          />
        )}

        {activeTab === "dashboard" && <DashboardPage onTabChange={setActiveTab} />}

        {activeTab === "response" && (
          <ResponseToAQuery
            query={currentQuery}
            onTabChange={setActiveTab}
            setCurrentQuery={setCurrentQuery}
            selectedZone={selectedZone}
            responseText={responseText}
            amountConsumption={amountConsumption}
            hectareEq={hectareEq}
            pourcentage={pourcentage}
          />
        )}
      </div>
    </div>
  );
}

export default App;
