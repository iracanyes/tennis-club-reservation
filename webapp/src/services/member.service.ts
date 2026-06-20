import ApiService from "@services/api.service.ts";
import {isNil} from "lodash";
import ApiRoutes from "@navigation/api.routes.ts";
import { useToast } from "primevue";
import type {Category, Member, Rank} from "@dto";

class MemberService {
  private readonly apiService: ApiService  = ApiService.getInstance();
  private static instance: MemberService;
  private readonly toast = useToast();

  public static getInstance(): MemberService{
    if (isNil(MemberService.instance)){
      MemberService.instance = new MemberService();
    }
    return MemberService.instance;
  }

  public async getCategories(): Promise<Category[]>{
    try{
      const result = await this.apiService.get(ApiRoutes.ListCategories);

      if(result){
        console.log("MemberService.getCategories");
        console.log(result);
        return result;
      }
    }catch (e) {
      console.error(e);
      this.toast.add({
        severity: "danger",
        summary: "Catégories : Erreur",
        detail: "Erreur lors de la récupération des catégories",
        life: 3000
      });
    }

    return [];

  }

  public async getRanks(): Promise<Rank[]> {
    try {
      const result = await this.apiService.get(ApiRoutes.ListRanks);

      if(result){
        console.log("MemberService.getRanks");
        console.log(result);
        return result;
      }
    }catch (e) {
      console.error(e);

      this.toast.add({
        severity: "danger",
        summary: "Classement : Erreur",
        detail: "Erreur lors de la récupération des classements",
        life: 3000
      });
    }

    return [];
  }

  /**
   * Get members
   */
  public async getMembers(): Promise<Member[]>{
    try{
      const result = await this.apiService.get(ApiRoutes.MemberList);

      if(result){
        console.log("MemberService.getMembers");
        console.log(result);
        return result;
      }
    }catch (e) {
      console.error(e);
      this.toast.add({
        severity: "danger",
        summary: "Membres : Erreur",
        detail: "Erreur lors de la récupération des membres",
        life: 3000
      });
    }

    return [];

  }

  /**
   * Create member
   * @param payload
   */
  public async createMember(payload : Member){
    try{
      const result = await this.apiService.post(ApiRoutes.MemberCreate, payload);

      if(result){
        return true;
      }
    }catch (e) {
      console.error(e);

      this.toast.add({
        severity: "danger",
        summary: "Profile : Erreur",
        detail: "Erreur lors de la mise à jour du profile",
        life: 3000
      });
    }

    return false;
  }

  /**
   * Update profile
   * @param payload
   */
  public async updateProfile(payload : Member){
    try{
      const result = await this.apiService.put(ApiRoutes.UpdateProfile + payload.id, payload);

      if(result){
        return true;
      }
    }catch (e) {
      console.error(e);

      this.toast.add({
        severity: "danger",
        summary: "Profile : Erreur",
        detail: "Erreur lors de la mise à jour du profile",
        life: 3000
      });
    }

    return false;
  }

  /**
   * Delete member
   * @param member
   */
  public async deleteMember(member: Member){
    const payload = {
      id : member.id,
      email : member.email,
      aft_id : member.aft_id,
    }

    try {
      const result = await this.apiService.delete(ApiRoutes.MemberDelete + member.id, payload);

      console.log("MembersService.deleteMember result : ",result);
      if(result){
        return true;
      }
    }catch (e: any) {
      console.error("MembersService.deleteMember() errors : ",e);
      this.toast.add({
        severity: "danger",
        summary: "Profile : Erreur",
        detail : e.message
      });
    }

    return false;
  }

  public async toggleSubscriptionStatus(member: Member){
    const payload = {
      id: member.id,
      aft_id: member.aft_id,
      email : member.email,
      annual_fee_paid : !member.annual_fee_paid,
    }

    try{
      const response = await this.apiService.put(ApiRoutes.SubscriptionStatus, payload);

      if(response){
        return true;
      }
    }catch (e: any) {
      this.toast.add({
        severity: "danger",
        summary: "Profile : Erreur",
        detail : e.message,
        life : 3000
      });

    }

    return false;
  }
}

export default MemberService;