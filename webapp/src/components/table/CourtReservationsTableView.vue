<script setup lang="ts">
import {ref, onMounted, type Ref} from "vue";
import {Column, DataTable, Tag, useToast} from "primevue";
import ApiRoutes from "@navigation/api.routes.ts";
import { APIService } from "@services";
import type Reservation from "@dto/reservation.dto.ts";

const apiService = APIService.getInstance();
const reservations: Ref<Reservation[]> = ref([]);
const expandedRowGroups = ref();
const toast = useToast();

const onRowGroupExpand = (event: any) => {
	toast.add({ severity: 'info', summary: 'Row Group Expanded', detail: 'Value: ' + event.data, life: 3000 });
};
const onRowGroupCollapse = (event: any) => {
	toast.add({ severity: 'success', summary: 'Row Group Collapsed', detail: 'Value: ' + event.data, life: 3000 });
};

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

const calculateReservationTotal = (court_number: number) => {
	let total = 0;

	if (reservations.value) {
		for (let reservation of reservations.value) {
			if (reservation.court.number === court_number) {
				total++;
			}
		}
	}

	return total;
};

onMounted(async () => {
	// Get reservations
	const result = await apiService.get(ApiRoutes.ListReservations);
	console.log("Result count : ",result.length);
	console.log(result);
	if(result.length > 0){
		reservations.value = result;
	}
})

</script>

<template>
	<section class="flex h-full w-full justify-center items-center">
		<DataTable
			v-model:expandedRowGroups="expandedRowGroups"
			:value="reservations"
			tableStyle="min-width: 50rem"
			scrollable
			scrollHeight="400px"
			expandableRowGroups
			rowGroupMode="subheader"
			groupRowsBy="court.number"
			@rowgroup-expand="onRowGroupExpand"
			@rowgroup-collapse="onRowGroupCollapse"
		  sortMode="single"
			sortField="court.number"
			:sortOrder="1"
			class="bg-white"
		>
			<template #groupheader="slotProps">
				<img :alt="slotProps.data.court.number" :src="''" width="32" style="vertical-align: middle; display: inline-block" class="ml-2" />
				<span class="align-middle ml-2 font-bold leading-normal">
					{{ `Terrain n° ${slotProps.data.court.number} : ${slotProps.data.court.type}` }}
				</span>
			</template>
			<Column field="date_reservation" header="Date réservation" style="width: 25%"></Column>
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
			<Column field="event_type" header="Type d'événement" style="width: 25%"></Column>
			<Column header="Statut">
				<template #body="slotProps">
					<Tag :value="slotProps.data.status" :severity="getSeverity(slotProps.data)" />
				</template>
			</Column>
			<template #groupfooter="slotProps">
				<div class="flex justify-end font-bold w-full">Total des réservations: {{ calculateReservationTotal(slotProps.data.court.number) }}</div>
			</template>
		</DataTable>
	</section>
</template>

<style scoped>

</style>