const ReservationTypeEnum : ReservationTypeEnumType[] = [
  {
    key: "CLUB_RESERVATION",
    value: "club_reservation",
    text: "Réservation du club",
  },
  {
    key: "EVENT",
    value: "event",
    text: "Événement"
  },
] as const;

type ReservationTypeEnumType = {
  key: string;
  value: string;
  text: string;
};

export { type ReservationTypeEnumType, ReservationTypeEnum };