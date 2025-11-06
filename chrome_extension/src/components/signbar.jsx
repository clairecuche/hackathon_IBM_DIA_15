import React from "react";

const SignalBars = ({ value, maxValue = 20 }) => {
  /**
   * value : nombre représentant le niveau (ex: CO₂, consommation…)
   * maxValue : valeur max pour que toutes les barres soient colorées
   */

  const numBars = 4; // nombre de barres
  const thresholds = Array.from({ length: numBars }, (_, i) =>
    ((i + 1) * maxValue) / numBars
  ); // [5, 10, 15, 20] si maxValue=20

  // Fonction pour savoir si une barre doit être colorée
  const isActive = (i) => value >= thresholds[i];

  const barStyles = (height, active) => ({
    width: "12px",
    height: `${height}px`,
    margin: "0 3px",
    backgroundColor: active ? "#71B071" : "#E0E0E0", // verte si active, gris sinon
    borderRadius: "3px",
    transition: "background-color 0.3s ease",
  });

  return (
    <div style={{ display: "flex", alignItems: "flex-end", height: "40px" }}>
      <div style={barStyles(10, isActive(0))} />
      <div style={barStyles(18, isActive(1))} />
      <div style={barStyles(26, isActive(2))} />
      <div style={barStyles(34, isActive(3))} />
    </div>
  );
};

export default SignalBars;