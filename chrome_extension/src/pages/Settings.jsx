import React from "react";
import DropdownButton from "../components/dropdown_button.jsx";
import Button from "../components/button.jsx";

const Settings = ({ onTabChange, selectedZone, setSelectedZone }) => {
  return (
    <div style={{ width: "100%", padding: "16px", boxSizing: "border-box" }}>
      <h2>Settings</h2>

      {/* Dropdown avec valeur initiale */}
      <DropdownButton
        selected={selectedZone}           // affiche la valeur sélectionnée
        setSelected={setSelectedZone}     // permet de mettre à jour la valeur
      />

      <Button
        label="Save Settings"
        onClick={() => onTabChange("query")}
      />
    </div>
  );
};

export default Settings;
