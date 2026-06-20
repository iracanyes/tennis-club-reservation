<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter} from "vue-router";
import type Reservation from "@dto/reservation.dto.ts";
import { ApiService, TokenService } from "@services";
import ApiRoutes from "@navigation/api.routes.ts";
import {isNil} from "lodash";
import { DataTable, Column, Tag, Button, ButtonGroup } from "primevue";
import { ReservationHelper } from "@helper";

const router = useRouter();
const myReservations = ref<Reservation[]>([]);
const apiService = ApiService.getInstance();
const tokenService = TokenService.getInstance();
let tomorrow = new Date();


onMounted(async () => {

	tomorrow = new Date();
	tomorrow.setDate(tomorrow.getDate() + 1);

	try {
		const result = await apiService.get(ApiRoutes.MyReservations);

		console.log("MyReservationTableView.MyReservations - result ",result);

		if(result){
			myReservations.value = result as Reservation[];
		}
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
	console.log()
	try {
		const result = await apiService.delete(ApiRoutes.DeleteReservation + reservation.id);

		console.log("MyReservationsTableView.deleteReservation() result : ",result);
		if(result){
			router.go(0);
		}
	}catch (e: any) {
		console.error("MyReservationsTableView.deleteReservation() errors : ",e);
	}
}



</script>

<template>
	<section id="ownReservationsTable" class="flex h-full justify-center items-center w-full">
		<DataTable
			:value="myReservations"
			paginator
			:rows="5"
			:rowsPerPageOptions="[5, 10, 20, 50]"
			tableStyle="min-width: 50rem"
		>
			<Column field="date_reservation" header="Date réservation" style="width: 7rem"></Column>
			<Column field="start_time" header="Heure de début" style="width: 3.5rem"></Column>
			<Column field="duration" header="Durée" style="width: 3rem">
				<template #body="slotProps">
					{{ slotProps.data.duration + "h"}}
				</template>
			</Column>
			<Column field="is_double" header="En double?" style="width: 3rem">
				<template #body="slotProps">
					{{   ( slotProps.data.is_double ? "Oui" : "Non") }}
				</template>
			</Column>
			<Column header="Terrain" style="width: 3.5rem">
				<template #body="slotProps">
					{{ "#"+ slotProps.data.court.number + " " + ReservationHelper.displayCourtType(slotProps.data.court.type) }}
				</template>
			</Column>
			<Column header="Participants" style="width: 6.5rem">
				<template #body="slotProps">
					<div>
						<p v-for="participant in slotProps.data.participants" :key="participant.id">
							<span class="font-semibold">
								{{participant.aft_id }}
							</span>
							<br>
							<span style="font-size: 11px;">
								{{ participant.firstname + " " + participant.lastname }}
							</span>

						</p>
					</div>
				</template>
			</Column>
			<Column header="Statut" style="width: 6rem">
				<template #body="slotProps">
					<Tag :value="slotProps.data.status" :severity="getSeverity(slotProps.data)" />
				</template>
			</Column>
			<Column header="Action">
				<template #body="slotProps">

					<ButtonGroup class="flex flex-col gap-y-2">
						<!--
						<Button label="Save" icon="pi pi-check" />
						-->

						<Button
							v-if="(new Date((slotProps.data.date_reservation + 'T' + slotProps.data.start_time))) > tomorrow"
							label="Delete"
							icon="pi pi-trash"
							severity="warn"
							@click.prevent="deleteReservation(slotProps.data)"
						/>
						<!--
						<Button label="Cancel" icon="pi pi-times" />
						-->
					</ButtonGroup>
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
div.p-datatable{
	font-size: 12px;
}
div.p-select-list-container{
	font-size: 12px;
}

span.p-select-option-label{
	font-size: 12px !important;
}


</style>