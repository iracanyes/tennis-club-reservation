<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter} from "vue-router";
import ApiService from "@services/api.service.ts";
import ApiRoutes from "@navigation/api.routes.ts";
import {isNil} from "lodash";
import { DataTable, Column, Tag, Button, ButtonGroup } from "primevue";
import type Court from "@dto/court.dto.ts";

const router = useRouter();
const courts = ref<Court[]>([]);
const apiService = ApiService.getInstance();

onMounted(async () => {

	try {
		const result = await apiService.get(ApiRoutes.ListCourts);

		console.log("MyReservationTableView.MyReservations - result ",result);

		if(result){
			courts.value = result as Court[];
		}
	}catch (e) {
		console.error(e);
	}

});

const getType = (court: Court) => {
	// console.log("MyReservationTableView.getType - ",court);
	switch (court.type) {
		case 'grass':
			return 'success';

		case 'clay':
			return 'warn';

		case 'hard':
			return 'danger';

		case 'carpet':
			return 'info'

		default:
			return 'secondary';
	}
};

const deleteCourt = async (court: Court) => {
	console.log("CourtsTableView.DeleteCourt ", court);
	try {
		const result = await apiService.delete(ApiRoutes.DeleteCourt + court.id);

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
			:value="courts"
			paginator
			:rows="5"
			:rowsPerPageOptions="[5, 10, 20, 50]"
			tableStyle="min-width: 50rem"
		>
			<Column field="number" header="N° du court de tennis" style="width: 25%"></Column>
			<Column header="Type">
				<template #body="slotProps">
					<Tag :value="slotProps.data.type" :severity="getType(slotProps.data)" />
				</template>
			</Column>
			<Column header="Action">
				<template #body="slotProps">

					<ButtonGroup class="flex flex-col gap-y-2">
						<!--
						<Button label="Save" icon="pi pi-check" />
						-->

						<Button
							label="Delete"
							icon="pi pi-trash"
							severity="warn"
							@click.prevent="deleteCourt(slotProps.data)"
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

</style>