const GenderTypeEnum = [
  {
    key: "MALE",
    value: "M",
    text: "Mâle"
  },
  {
    key: "FEMALE",
    value: "F",
    text: "Femelle"
  }
];

type GenderType = {
  key: string;
  value: string;
  text: string;
}

export {  GenderTypeEnum, type GenderType };