<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter} from "vue-router";
import type Reservation from "@dto/reservation.dto.ts";
import {isNil} from "lodash";
import { DataTable, Column, Tag, Button, ButtonGroup } from "primevue";
import {ReservationService, TokenService} from "@services";
import {useToast} from "primevue/usetoast";

const router = useRouter();
const toast = useToast();
const tokenService = TokenService.getInstance();
const reservations = ref<Reservation[]>([]);
const reservationService = ReservationService.getInstance();
let tomorrow = new Date();


onMounted(async () => {

	tomorrow = new Date();
	tomorrow.setDate(tomorrow.getDate() + 1);

	try {
		reservations.value = await reservationService.getReservations();
	}catch (e) {
		console.error(e);
	}

});

const getSeverity = (reservation: Reservation) => {
	console.log("MyReservationTableView.getSeverity - ",reservation);
	switch (reservation.status) {
		case 'active':
			return 'success';

		case 'uncompleted':
			return 'warn';

		case 'canceled':
			return 'danger';

		case 'completed':
			return 'info'

		default:
			return 'secondary';
	}
};

const deleteReservation = async (reservation: Reservation) => {
	try {
		const result = await reservationService.deleteReservation(reservation.id);

		console.log("MyReservationsTableView.deleteReservation() result : ",result);
		if(result){
			router.go(0);
		}
	}catch (e: any) {
		console.error("MyReservationsTableView.deleteReservation() errors : ",e);
		toast.add({
			severity: "error",
			summary: "Réservation : Erreur",
			detail: `Erreur lors de la suppression de la réservation.`
		});
	}
}



</script>

<template>
	<section id="ownReservationsTable" class="flex h-full justify-center items-center w-full">
		<DataTable
			:value="reservations"
			paginator
			:rows="5"
			:rowsPerPageOptions="[5, 10, 20, 50]"
			tableStyle="min-width: 50rem"
		>
			<Column field="date_reservation" header="Date réservation" style="width: 25%" sortable></Column>
			<Column field="start_time" header="Heure de début" style="width: 25%"></Column>
			<Column field="duration" header="Durée" style="width: 25%">
				<template #body="slotProps">
					{{ slotProps.data.duration + "h"}}
				</template>
			</Column>
			<Column field="is_double" header="En double?" style="width: 25%">
				<template #body="slotProps">
					{{   ( slotProps.data.is_double ? "Oui" : "Non") }}
				</template>
			</Column>
			<Column header="Terrain" style="width: 25%">
				<template #body="slotProps">
					{{ "#"+ slotProps.data.court.number + " " + slotProps.data.court.type }}
				</template>
			</Column>
			<Column header="Statut">
				<template #body="slotProps">
					<Tag :value="slotProps.data.status" :severity="getSeverity(slotProps.data)" />
				</template>
			</Column>
			<Column header="Action">
				<template #body="slotProps">

					<div class="flex flex-col gap-y-2">
						<Button
							v-if="tokenService.isAdmin && (new Date((slotProps.data.date_reservation + 'T' + slotProps.data.start_time))) > tomorrow"
							label="Éditer"
							icon="pi pi-pen-to-square"
							severity="info"
							size="small"
							class="text-sm"
							disabled
							@click.prevent="deleteReservation(slotProps.data)"
						/>

						<Button
							v-if="tokenService.isAdmin && (new Date((slotProps.data.date_reservation + 'T' + slotProps.data.start_time))) > tomorrow"
							label="Supprimer"
							icon="pi pi-trash"
							severity="warn"
							size="small"
							@click.prevent="deleteReservation(slotProps.data)"
						/>
					</div>
				</template>
			</Column>

			<template #paginatorcontainer="{ first, last, page, pageCount, prevPageCallback, nextPageCallback, totalRecords }">
				<div class="flex items-center gap-4 border border-primary bg-transparent rounded-full w-full py-1 px-2 justify-between">
					<Button icon="pi pi-chevron-left" rounded text @click="prevPageCallback" :disabled="page === 0" />
					<div class="text-color font-medium">
						<span class="hidden sm:block">Showing {{ first }} to {{ last }} of {{ totalRecords }}</span>
						<span class="block sm:hidden">Page {{ page + 1 }} of {{ pageCount }}</span>
					</div>
					<Button icon="pi pi-chevron-right" rounded text @click="nextPageCallback" :disabled="isNil(pageCount) || (page === pageCount - 1)" />
				</div>
			</template>
		</DataTable>
	</section>
</template>

<style scoped>

</style>