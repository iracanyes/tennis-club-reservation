const ReservationDurationEnum = {
  ONE_HOUR : 1,
  TWO_HOURS : 2,
  FOUR_HOURS : 4,
  ONE_DAY : 13,
} as const;

type ReservationDurationEnum = (typeof ReservationDurationEnum)[keyof typeof ReservationDurationEnum];

export default ReservationDurationEnum;