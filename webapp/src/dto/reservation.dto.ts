import type Member from "./member.dto.ts";
import type Court from "./court.dto.ts";

export default interface Reservation {
  id: string;
  dateCreated: Date;
  dateModified: Date;
  event_type : string;
  status : string;
  isDouble : boolean;
  author : Member,
  court : Court,
  participants : [Member];
}