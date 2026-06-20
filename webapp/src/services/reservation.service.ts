import { ApiService } from "@services";
import {useToast} from "primevue/usetoast";
import {isNil} from "lodash";
import type { Reservation } from "@dto";
import ApiRoutes from "@navigation/api.routes.ts";

class ReservationService {
  private readonly apiService: ApiService = ApiService.getInstance();
  private static instance: ReservationService;
  private readonly toast = useToast();

  public static getInstance(): any {
    if(isNil(ReservationService.instance)) {
      ReservationService.instance = new ReservationService();
    }

    return ReservationService.instance;
  }

  public async getReservations(): Promise<Reservation[]> {
    try {
      const reservations = await this.apiService.get(ApiRoutes.ListReservations);

      if(reservations.length > 0) {
        return reservations;
      }
    }catch(err) {
      console.error(err);
      this.toast.add({
        severity: 'error',
        summary: 'Reservations : Erreur',
        detail: 'Impossible de récupérer la liste des réservations',
        life : 3000
      });
    }

    return [];
  }

  public async deleteReservation(reservation: Reservation): Promise<boolean> {
    try {
      const result = await this.apiService.delete(ApiRoutes.DeleteReservation + reservation.id);

      if(result) {
        this.toast.add({
          severity: 'success',
          summary: 'Réservation supprimée',
          life : 3000
        });
      }

      return true;
    }catch(err) {
      console.error(err);
      this.toast.add({
        severity: 'erreur',
        summary: 'Réservation : Erreur',
        detail : 'Erreur lors de la suppression de la réservation',
        life : 3000
      });
    }

    return false;
  }
}

export default ReservationService;

