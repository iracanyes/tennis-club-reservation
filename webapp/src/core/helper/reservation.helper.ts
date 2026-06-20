
class ReservationHelper {
  public static displayCourtType(courtType: string): string{
    switch (courtType) {
      case "hard":
        return "Dur";
      case "grass":
        return "Gazon naturel";
      case "clay":
        return "Terre battue";
      case "carpet":
        return "Indoor";
      default:
        return "None";

    }
  }

}

export default ReservationHelper;