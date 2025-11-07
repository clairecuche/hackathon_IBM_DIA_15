import React from "react";
import { TreeDeciduous } from "lucide-react";

const TreeFill = ({ value, max = 100, size = 40 }) => { // même taille que LeafFill
  // Pourcentage de remplissage
  const fillPercentage = Math.min(Math.max(value / max, 0), 1);

  return (
    <div style={{ position: "relative", width: size, height: size }}>
      {/* Remplissage de l'arbre */}
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

      {/* Icône TreeDeciduous au-dessus */}
      <TreeDeciduous
        size={size}  // même taille que LeafFill
        stroke="#212121"
        style={{
          position: "relative",
          zIndex: 1,
        }}
      />
    </div>
  );
};

export default TreeFill;
