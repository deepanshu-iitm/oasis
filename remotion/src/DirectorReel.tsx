import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type DirectorBeat = {
  id: string;
  caption_heading: string;
  caption_desc: string;
  duration_sec: number;
};

export type DirectorReelProps = {
  accentColor?: string;
  beats: DirectorBeat[];
  brandName?: string;
};

const BACKGROUNDS = [
  ["#090A14", "#17205C"],
  ["#101229", "#34236B"],
  ["#071B24", "#0D4C5B"],
  ["#1B102B", "#61306C"],
  ["#0B1120", "#163D63"],
];

export const DirectorReel = ({
  accentColor = "#8EA2FF",
  beats,
  brandName = "Oasis",
}: DirectorReelProps) => {
  const frame = useCurrentFrame();
  const { fps, height, width } = useVideoConfig();
  const beatFrames = beats.map((beat) => Math.round(beat.duration_sec * fps));
  let elapsedFrames = 0;
  let activeIndex = 0;

  for (let index = 0; index < beatFrames.length; index += 1) {
    if (frame < elapsedFrames + beatFrames[index]) {
      activeIndex = index;
      break;
    }
    elapsedFrames += beatFrames[index];
    activeIndex = index;
  }

  const activeBeat = beats[activeIndex] ?? beats[0];
  const beatNumber = activeIndex + 1;
  const localFrame = frame - elapsedFrames;
  const beatDuration = beatFrames[activeIndex] ?? fps;
  const sceneProgress = interpolate(localFrame, [0, beatDuration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(
    localFrame,
    [0, 10, Math.max(14, beatDuration - 12), beatDuration],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const copyY = interpolate(localFrame, [0, 18], [72, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const cardScale = spring({
    frame: Math.max(0, localFrame - 3),
    fps,
    config: { damping: 16, stiffness: 105 },
  });
  const glowScale = interpolate(localFrame, [0, beatDuration], [0.75, 1.25], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const [backgroundStart, backgroundEnd] = BACKGROUNDS[activeIndex % BACKGROUNDS.length];
  const isOutro = activeIndex === beats.length - 1;

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 18% 12%, ${accentColor}70 0%, transparent 28%), linear-gradient(145deg, ${backgroundStart}, ${backgroundEnd})`,
        color: "#FFFFFF",
        fontFamily: "Arial, sans-serif",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          backgroundImage: "linear-gradient(rgba(255,255,255,0.055) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.055) 1px, transparent 1px)",
          backgroundSize: "72px 72px",
          inset: 0,
          opacity: 0.55,
          position: "absolute",
        }}
      />
      <div
        style={{
          background: accentColor,
          borderRadius: "50%",
          filter: "blur(22px)",
          height: 560,
          opacity: 0.3,
          position: "absolute",
          right: -180 + Math.sin(frame * 0.035) * 45,
          top: 210 + Math.cos(frame * 0.03) * 55,
          transform: `scale(${glowScale})`,
          width: 560,
        }}
      />
      <div
        style={{
          border: `2px solid ${accentColor}88`,
          borderRadius: "50%",
          height: 700,
          left: -330,
          opacity: 0.32,
          position: "absolute",
          top: 1080,
          transform: `rotate(${frame * 0.25}deg)`,
          width: 700,
        }}
      />

      <div style={{ alignItems: "center", display: "flex", justifyContent: "space-between", left: 82, position: "absolute", right: 82, top: 72 }}>
        <div style={{ fontSize: 26, fontWeight: 800, letterSpacing: 7, textTransform: "uppercase" }}>{brandName}</div>
        <div style={{ border: "1px solid rgba(255,255,255,0.26)", borderRadius: 999, fontSize: 20, fontWeight: 700, letterSpacing: 2, padding: "12px 18px" }}>
          {beatNumber < 10 ? `0${beatNumber}` : beatNumber} / {beats.length < 10 ? `0${beats.length}` : beats.length}
        </div>
      </div>

      <div style={{ bottom: 74, display: "flex", gap: 10, left: 82, position: "absolute", right: 82 }}>
        {beats.map((beat, index) => (
          <div key={beat.id} style={{ background: "rgba(255,255,255,0.2)", borderRadius: 99, flex: 1, height: 8, overflow: "hidden" }}>
            <div
              style={{
                background: index < activeIndex ? "#FFFFFF" : accentColor,
                borderRadius: 99,
                height: "100%",
                transformOrigin: "left center",
                transform: `scaleX(${index < activeIndex ? 1 : index === activeIndex ? sceneProgress : 0})`,
              }}
            />
          </div>
        ))}
      </div>

      <div style={{ alignItems: "center", display: "flex", inset: 0, justifyContent: "center", padding: "160px 74px 150px", position: "absolute" }}>
        <div style={{ opacity, transform: `translateY(${copyY}px) scale(${0.9 + cardScale * 0.1})`, width: "100%" }}>
          <div style={{ color: accentColor, fontSize: 26, fontWeight: 800, letterSpacing: 5, marginBottom: 28, textTransform: "uppercase" }}>
            {isOutro ? "Ready when you are" : "Oasis video director"}
          </div>
          <div style={{ fontSize: isOutro ? 112 : 98, fontWeight: 800, letterSpacing: -4, lineHeight: 0.98, maxWidth: width - 148 }}>
            {activeBeat.caption_heading}
          </div>
          <div
            style={{
              backdropFilter: "blur(18px)",
              background: "rgba(8, 10, 22, 0.42)",
              border: "1px solid rgba(255,255,255,0.18)",
              borderRadius: 32,
              boxShadow: "0 24px 80px rgba(0,0,0,0.22)",
              color: "#E7EBFF",
              fontSize: 34,
              lineHeight: 1.28,
              marginTop: 46,
              padding: "30px 34px",
            }}
          >
            {activeBeat.caption_desc}
          </div>
          {isOutro && (
            <div style={{ alignItems: "center", background: "#FFFFFF", borderRadius: 999, color: "#101329", display: "flex", fontSize: 30, fontWeight: 800, justifyContent: "center", marginTop: 42, padding: "23px 34px", width: 310 }}>
              Explore now
            </div>
          )}
        </div>
      </div>

      <div style={{ bottom: 108, color: "rgba(255,255,255,0.65)", fontSize: 18, fontWeight: 700, left: 82, letterSpacing: 4, position: "absolute", textTransform: "uppercase" }}>
        Directed from a brief
      </div>
    </AbsoluteFill>
  );
};