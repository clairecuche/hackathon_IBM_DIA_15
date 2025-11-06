// src/App.jsx
import React, { useState } from "react";
import TopBar from "./components/topbar.jsx";
import NavBar from "./components/nav_bar.jsx";
import HomePage from "./pages/homepage.jsx";
import DashboardPage from "./pages/Dashboard.jsx";

function App() {
  const [activeTab, setActiveTab] = useState("query");

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
      <TopBar />
      <NavBar activeTab={activeTab} onTabChange={setActiveTab} />

      <div style={{ width: "100%" }}>
        {activeTab === "query" && <HomePage />}
        {activeTab === "dashboard" && <DashboardPage />}
      </div>
    </div>
  );
}

export default App;