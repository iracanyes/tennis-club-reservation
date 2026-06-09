import type Rank from "@dto/rank.dto.ts";


export default interface MemberRank {
  id: string;
  date_created: Date;
  points: number;
  rank: Rank;
}