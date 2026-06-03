<script setup lang="ts">
import { ref, onMounted, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import {
	useToast,
	Button,
	Checkbox,
	DatePicker,
	InputGroup,
	InputGroupAddon,
	InputText,
	FloatLabel,
	Select,
	MultiSelect,
} from "primevue";
import ApiRoutes from "@navigation/api.routes.ts";
import ApiService from "@services/api.service.ts";
import type { Court, Member, Reservation } from "@dto/index.ts";
import {
	ReservationDurationEnum,
	EventReasonEnum,
	ReservationStartTime,
	type ReservationStartTimeType,
	ReservationTypeEnum,
	type ReservationTypeEnumType
} from "@enums/index.ts";
import {isEmpty, isNil} from "lodash";
import {TokenService} from "@services";
import {formatISO} from "date-fns";

const router = useRouter();
const toast = useToast();
const apiService = ApiService.getInstance();
const tokenService = TokenService.getInstance();
const courts: Ref<Court[]> = ref([]);
const members : Ref<Member[]> = ref([]);


const court : Ref<Court | null> = ref(null);
const dateReservation : Ref<Date | null>  = ref(null);
const start_time : Ref<ReservationStartTimeType| null> = ref(null);
const start_times: Ref<ReservationStartTimeType[]> = ref(ReservationStartTime);
const duration = ref(0);
let durations: number[] = Object.values(ReservationDurationEnum)
const event_type: Ref<ReservationTypeEnumType | null> = ref(ReservationTypeEnum[0]);
const isDouble = ref(false);
const participants : Ref<Member[]> = ref([]);
const loading = ref(false);
const reasons: string[] = Object.values(EventReasonEnum);
const reason = ref("");


onMounted(() => {
	// Retrieve members
	loading.value = true;

	// Remove day reservation for member
	if(!tokenService.isAdmin.value)
		durations.pop();



	try{
		// Get members' list
		apiService.get(ApiRoutes.MemberList)
			.then((res) => {
				console.log(`CreateReservation.getMembers : ${res}`);
				if (res.length > 0) {
					members.value = res;
				}
			}).catch((err) => {
				console.log(`CreateReservation.getMembers ERRORS : ${err}`);
				toast.add({
					severity: "error",
					summary: "Unable to retrieve members.",
					detail: err.message,
				});
			});

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
		console.error(`CreateReservation.getMembers ERRORS : ${err}`);

		toast.add({
			severity: "error",
			summary: "Unable to retrieve courts and members.",
		});
	}
})


const onSubmit = async (e: Event) => {
	e.preventDefault();

	loading.value = true;

	const courtInput = court.value;

	if (courtInput == null){
		toast.add({
			severity: "error",
			summary: "Please select the court.",
		})
		return;
	}


	if(isNil(dateReservation.value)
		|| isNil(start_time.value)
		|| new Date((formatISO(dateReservation.value, { representation: "date" }) + "T" + start_time.value.str)).getTime() < Date.now()
	){
		toast.add({
			severity: "error",
			summary: "Please select a reservation's date greater or equal to today.",
		})
		return;
	}

	if(isEmpty(start_time.value)){
		toast.add({
			severity: "error",
			summary: "Please select a start time.",
		})
		return;
	}

	if(isDouble.value && duration.value < 2){
		toast.add({
			severity: "error",
			summary: "Please select a correct duration for the selected reservation.",
			detail: "Simple reservation's duration is between 1 and 2 hours." +
				"\nDouble reservation's duration is between 2 and 4 hours for a double reservation.",
			life: 3000
		})
		return;
	}

	if(isNil(event_type.value)){
		toast.add({
			severity: "error",
			summary: "Please select an event type.",
			life: 5000
		});
		return;
	}

	const payload = {
		date_reservation: formatISO(dateReservation.value, { representation: "date"}),
		start_time: start_time.value.str,
		duration: duration.value,
		is_double: isDouble.value,
		court : courtInput.id,
		event_type: "event",
		reason: reason.value,
		participants: participants.value.map((p) => p.id)
	};

	console.log("CreateReservation.submit - court.value", court.value);
	console.log("CreateReservation.submit - payload", payload);

	try {
		const data: Reservation = await apiService.post(ApiRoutes.CreateEvent, payload);

		if(data.id){
			toast.add({
				severity: "success",
				summary: "Event created",
				detail: data.event_type + " is " + data.status,
				life: 5000
			});

			router.go(0);
		}


	}catch (e : any) {
		console.log(`Create Reservation error: ${e}`);
		toast.add({
			severity: "error",
			summary: "Reservation could not be created",
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
						id="event_type"
						v-model="reason"
						:options="reasons"
						checkmark
					/>
					<label for="court" class="text-black">Raison de l'événement</label>
				</FloatLabel>
			</InputGroup>
			<!-- InputGroup : Tennis court -->
			<InputGroup>
				<InputGroupAddon>
					<i class="pi pi-objects-column"></i>
				</InputGroupAddon>
				<FloatLabel  variant="in">
					<Select
						id="court"
						v-model="court"
						:options="courts"
						optionLabel="number"
						checkmark
					/>
					<label for="court" class="text-black">Numéro du court de tennis</label>
				</FloatLabel>
			</InputGroup>

			<!-- InputGroup : Date of reservation -->
			<InputGroup>
				<InputGroupAddon>
					<i class="pi pi-calendar"></i>
				</InputGroupAddon>
				<FloatLabel variant="in">
					<DatePicker
						id="date_reservation"
						v-model="dateReservation"
						dateFormat="yy-mm-dd"
					/>
					<label for="date_reservation">Date de réservation</label>
				</FloatLabel>
			</InputGroup>

			<!-- InputGroup : Start time -->
			<InputGroup>
				<InputGroupAddon>
					<i class="pi pi-calendar-clock"></i>
				</InputGroupAddon>
				<FloatLabel  variant="in">
					<Select
						id="start_time"
						v-model="start_time"
						:options="start_times"
						optionLabel="str"
						checkmark
					/>
					<label for="court" class="text-black">Heure de début</label>
				</FloatLabel>
			</InputGroup>

			<!-- InputGroup : Tennis court -->
			<InputGroup>
				<InputGroupAddon>
					<i class="pi pi-objects-column"></i>
				</InputGroupAddon>
				<FloatLabel>
					<Select
						id="duration"
						v-model="duration"
						:options="durations"
						placeholder="Sélectionner la durée"
					/>
					<label for="court" class="text-black">Sélectionner la durée</label>
				</FloatLabel>
			</InputGroup>

			<!-- InputGroup : Is double party -->
			<InputGroup>
				<InputGroupAddon>
					<Checkbox v-model="isDouble" :binary="true" size="small" />
				</InputGroupAddon>
				<InputText placeholder="Réservation en double? Cochez." disabled />
			</InputGroup>

			<!-- InputGroup : Participantes-->
			<InputGroup>
				<InputGroupAddon>
					<i class="pi pi-user"></i>
				</InputGroupAddon>
				<FloatLabel>
					<MultiSelect
						id="participants"
						v-model="participants"
						name="participant.aft_id"
						:options="members"
						optionLabel="aft_id"
						placeholder="Sélectionner les participants"
						filter
						:maxSelectedLabels="4"
					/>
					<label for="participants" class="text-black">Participants</label>
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