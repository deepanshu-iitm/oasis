import {
  AbsoluteFill,
  interpolate,
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

export const DirectorReel = ({
  accentColor = "#8EA2FF",
  beats,
  brandName = "OASIS",
}: DirectorReelProps) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
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
  const opacity = interpolate(
    localFrame,
    [0, 12, Math.max(12, beatDuration - 12), beatDuration],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const translateY = interpolate(localFrame, [0, 18], [50, 0], {
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
          background: accentColor,
          borderRadius: 999,
          height: 18,
          left: 100,
          opacity: 0.9,
          position: "absolute",
          right: 100,
          top: 110,
        }}
      />
      <div style={{ fontSize: 30, fontWeight: 700, left: 100, letterSpacing: 8, position: "absolute", top: 165 }}>
        {brandName}
      </div>
      <div
        style={{
          alignItems: "center",
          display: "flex",
          flexDirection: "column",
          opacity,
          padding: 100,
          transform: `translateY(${translateY}px)`,
        }}
      >
        <div style={{ color: accentColor, fontSize: 34, fontWeight: 700, letterSpacing: 6 }}>
          {beatNumber < 10 ? `0${beatNumber}` : beatNumber}
        </div>
        <div style={{ fontSize: 112, fontWeight: 800, lineHeight: 1.04, marginTop: 32, textAlign: "center" }}>
          {activeBeat.caption_heading}
        </div>
        <div style={{ color: "#BFC8E8", fontSize: 42, lineHeight: 1.3, marginTop: 36, textAlign: "center" }}>
          {activeBeat.caption_desc}
        </div>
      </div>
    </AbsoluteFill>
  );
};