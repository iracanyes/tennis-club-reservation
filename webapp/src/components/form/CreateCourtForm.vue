<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import {
	useToast,
	Button,
	InputGroup,
	InputGroupAddon,
	InputNumber,
	FloatLabel,
	Select,
} from "primevue";
import ApiRoutes from "@navigation/api.routes.ts";
import ApiService from "@services/api.service.ts";
import type { Court } from "@dto/index.ts";
import {isEmpty} from "lodash";
import {TokenService} from "@services";
import CourtTypeEnum from "@enums/CourtTypeEnum.ts";

const router = useRouter();
const toast = useToast();
const apiService = ApiService.getInstance();
const tokenService = TokenService.getInstance();
const loading = ref(false);
const courtNumber = ref(0);
const courtTypes : string[] = Object.values(CourtTypeEnum);
const courtType = ref("hard")
const courts: Ref<Court[]> = ref([]);


onMounted(() => {
	// Retrieve members
	loading.value = true;

	try{

		// Get courts' list
		apiService.get(ApiRoutes.CourtList)
			.then((res) => {
				if (res.length > 0) {
					courts.value = res;
				}
			}).catch((err) => {
				console.log(`CreateReservation.getCourts ERRORS : ${err}`);
				toast.add({
					severity: "error",
					summary: "Unable to retrieve court's list.",
					detail: err.message,
				});
			});

		loading.value = false;
	}catch (err: any) {
		console.error(`CreateReservation.getCourts ERRORS : ${err}`);

		toast.add({
			severity: "error",
			summary: "Unable to retrieve courts.",
		});
	}
})


const onSubmit = async (e: Event) => {
	e.preventDefault();

	loading.value = true;

	if (isEmpty(courtType.value)){
		toast.add({
			severity: "error",
			summary: "Please select the court's type.",
		})
		return;
	}

	if(courtNumber.value === 0){
		toast.add({
			severity: "error",
			summary: "Please select a court number.",
		})
		return;
	}


	const payload = {
		number: courtNumber.value,
		type: courtType.value,
	};

	console.log("CreateReservation.submit - payload", payload);

	try {
		const data: Court = await apiService.post(ApiRoutes.CreateCourt, payload);

		if("id" in data){
			toast.add({
				severity: "success",
				summary: "Court created",
				detail: "Court n° " + data.number + " is of type  " + data.type,
				life: 5000
			});

			router.go(0);
		}


	}catch (e : any) {
		console.log(`Create Court error: ${e}`);
		toast.add({
			severity: "error",
			summary: "Court could not be created",
			detail: e.message,
			life: 3000
		});



	}

	loading.value = false;
}

</script>

<template>
	<div class="">
		<h3 class="font-semibold mb-2 text-center">Ajouter un événement</h3>
		<form class="flex flex-col gap-y-6 mt-4">
			<!-- InputGroup : Tennis court -->
			<InputGroup v-if="tokenService.isAdmin.value">
				<InputGroupAddon>
					<i class="pi pi-objects-column"></i>
				</InputGroupAddon>
				<FloatLabel  variant="in">
					<Select
						id="court_type"
						v-model="courtType"
						:options="courtTypes"
						checkmark
					/>
					<label for="court_type" class="text-black">Type de terrain</label>
				</FloatLabel>
			</InputGroup>
			<!-- InputGroup : Tennis court -->
			<InputGroup>
				<InputGroupAddon>
					<i class="pi pi-objects-column"></i>
				</InputGroupAddon>
				<FloatLabel  variant="in">
					<InputNumber
						id="court_number"
						v-model="courtNumber"
						placeholder="N° de terrain"
					/>
					<label for="court_number" class="text-black">Numéro du court de tennis</label>
				</FloatLabel>
			</InputGroup>



			<div class="flex flex-row sm:flex-col gap-y-4">
				<Button
					type="button"
					severity="success"
					label="Valider"
					icon="pi pi-check"
					@click="onSubmit"
					raised
				/>
				<Button
					type="button"
					severity="danger"
					label="Effacer"
					icon="pi pi-times"
					raised
					disabled
				/>
			</div>
		</form>
	</div>
</template>

<style scoped>

</style>