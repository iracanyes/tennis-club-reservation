const EventReasonEnum = Object.freeze({
  CLUB_RESERVATION: "club_reservation",
  INTER_CLUBS: "interclubs",
  CHAMPIONSHIP: "championship",
  COMPETITION: "competition",
  LESSON: "lesson",
  RENOVATION: "renovation",
});

type EventReasonEnum = (typeof EventReasonEnum)[keyof typeof EventReasonEnum];

export default EventReasonEnum;