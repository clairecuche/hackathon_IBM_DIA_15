import React from "react";
import SignalBars from "./signbar.jsx";

const ConsumptionWithSignal = ({ value, maxValue = 20 }) => {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        fontFamily: "'Poppins', sans-serif",
        fontSize: "14px",
        color: "#333",
        padding: "8px 12px",
        border: "0px solid #transparent",
        borderRadius: "8px",
        width: "200px",
        boxSizing: "border-box",
        width: "100%",
      }}
    >
      {/* Valeur à gauche */}
      <p style={{ margin: 0 }}>{value} g of CO2</p>

      {/* Barres à droite */}
      <SignalBars value={value} maxValue={maxValue} />
    </div>
  );
};

export default ConsumptionWithSignal;