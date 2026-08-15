import { Composition } from "remotion";

import { DirectorReel } from "./DirectorReel";

export const RemotionRoot = () => {
  return (
    <Composition
      id="DirectorReel"
      component={DirectorReel}
      durationInFrames={600}
      fps={30}
      height={1920}
      width={1080}
    />
  );
};