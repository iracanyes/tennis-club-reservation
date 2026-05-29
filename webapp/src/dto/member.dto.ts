
export default interface Member {
  id: number;
  aft_id: number;
  email: string;
  firstname: string;
  lastname: string;
  gender: string;
  birthdate: Date;
  phone_number: string;
  annual_fee_paid: boolean;
  date_joined: Date;
  last_login: Date
}