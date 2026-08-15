import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const DirectorReel = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15, 150, 180], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const scale = interpolate(frame, [0, 150], [0.92, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        alignItems: "center",
        background: "#0B1020",
        color: "#FFFFFF",
        fontFamily: "Arial, sans-serif",
        justifyContent: "center",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          alignItems: "center",
          display: "flex",
          flexDirection: "column",
          opacity,
          transform: `scale(${scale})`,
        }}
      >
        <div style={{ color: "#8EA2FF", fontSize: 38, fontWeight: 700, letterSpacing: 10 }}>
          OASIS
        </div>
        <div style={{ fontSize: 112, fontWeight: 800, marginTop: 28, textAlign: "center" }}>
          Video Director
        </div>
        <div style={{ color: "#BFC8E8", fontSize: 42, marginTop: 36 }}>
          Brief to video, directed by an agent.
        </div>
      </div>
    </AbsoluteFill>
  );
};