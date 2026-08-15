import { Composition } from "remotion";

import { DirectorReel, type DirectorReelProps } from "./DirectorReel";

const defaultProps: DirectorReelProps = {
  accentColor: "#8EA2FF",
  brandName: "Oasis",
  beats: [
    { id: "b01", caption_heading: "Your next launch", caption_desc: "Starts with a clear story.", duration_sec: 4 },
    { id: "b02", caption_heading: "From brief to beats", caption_desc: "Plan every moment with intent.", duration_sec: 4 },
    { id: "b03", caption_heading: "One visual direction", caption_desc: "Copy, timing, and motion aligned.", duration_sec: 4 },
    { id: "b04", caption_heading: "Designed to move", caption_desc: "A polished reel in one render lane.", duration_sec: 4 },
    { id: "b05", caption_heading: "Oasis Director", caption_desc: "Turn your brief into video.", duration_sec: 4 },
  ],
};

export const RemotionRoot = () => {
  return (
    <Composition
      id="DirectorReel"
      component={DirectorReel}
      defaultProps={defaultProps}
      durationInFrames={600}
      fps={30}
      height={1920}
      width={1080}
    />
  );
};