import React from "react";
import { Leaf } from "lucide-react";

const LeafFill = ({ value, max = 100, size = 40 }) => {
  const fillPercentage = Math.min(Math.max(value / max, 0), 1);

  return (
    <div style={{ position: "relative", width: size, height: size }}>
      {/* Feuille remplie */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          width: "100%",
          height: `${fillPercentage * 100}%`,
          backgroundColor: "#71B071",
          clipPath: "polygon(0 100%, 0 0, 100% 0, 100% 100%)",
          zIndex: 0,
        }}
      />

      {/* Icône Leaf au-dessus */}
      <Leaf
        size={size}
        stroke="#212121"
        style={{
          position: "relative",
          zIndex: 1,
        }}
      />
    </div>
  );
};

export default LeafFill;

