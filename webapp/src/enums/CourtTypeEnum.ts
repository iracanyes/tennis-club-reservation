const CourtTypeEnum = Object.freeze( {
  HARD: "hard",
  CLAY: "clay",
  GRASS: "grass",
  CARPET: "carpet",
});

type CourtTypeEnum = (typeof CourtTypeEnum)[keyof typeof CourtTypeEnum];

export default CourtTypeEnum;