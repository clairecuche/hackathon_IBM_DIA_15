// src/App.jsx
import React, { useState } from "react";
import TopBar from "./components/topbar.jsx";
import NavBar from "./components/nav_bar.jsx";
import HomePage from "./pages/homepage.jsx";
import DashboardPage from "./pages/Dashboard.jsx";
import ResponseToAQuery from "./pages/Responce_to_a_query.jsx";
import Settings from "./pages/Settings.jsx";

function App() {
  const [activeTab, setActiveTab] = useState("query");
  const [currentQuery, setCurrentQuery] = useState("");
  const [selectedZone, setSelectedZone] = useState("");

  return (
    <div
      style={{
        width: "100%",          // largeur totale de l'extension
        minHeight: "100vh",     // hauteur totale de l'extension
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
        {activeTab === "query" && (
          <HomePage
            onTabChange={setActiveTab}
            setCurrentQuery={setCurrentQuery} // transmettre le setter
          />
        )}
        {activeTab === "dashboard" && <DashboardPage onTabChange={setActiveTab} />}        
        {activeTab === "response" && (
          <ResponseToAQuery
            query={currentQuery}
            onTabChange={setActiveTab}     // passer la fonction de changement de page
            setCurrentQuery={setCurrentQuery} // passer la fonction pour réinitialiser la query
          />
        )}
        {activeTab === "settings" && <Settings onTabChange={setActiveTab} selectedZone={selectedZone} setSelectedZone={setSelectedZone} />}
      </div>
    </div>
  );
}

export default App;