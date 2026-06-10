<script setup lang="ts">
import { onMounted, reactive, ref, type Ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Form, type FormSubmitEvent } from "@primevue/forms";
import {
	Button,
	ButtonGroup,
	DatePicker,
	Fieldset,
	FloatLabel,
	InputGroup,
	InputGroupAddon,
	InputNumber,
	InputText,
	Password,
	ScrollPanel,
	Select,
	useToast,
} from "primevue";
import { MemberService } from "@services";
import {
	PhCake,
	PhCity,
	PhExam,
	PhGenderIntersex,
	PhGlobeHemisphereWest,
	PhGlobeX,
	PhHashStraight,
	PhHouse,
	PhIdentificationCard,
	PhMapTrifold,
	PhRanking,
	PhTennisBall,
	PhUserFocus
} from "@phosphor-icons/vue";
import { GenderTypeEnum } from "@enums/index.ts";
import type { Category, Rank } from "@dto";
import { isEmpty, isNil } from "lodash";
import {formatISO} from "date-fns";

const router = useRouter();
const toast = useToast();
const memberService = MemberService.getInstance();
const genders = ref(GenderTypeEnum);
const ranks: Ref<Rank[]> = ref([]);
const categories: Ref<Category[]> = ref([]);


const resolver = ({ values } : any) => {
	const errors = {
		aft_id: [],
		email: [],
		firstname: [],
		lastname: [],
		gender: [],
		birthdate: [],
		phone_number: [],
		category: [],
		rank: [],
		street: [],
		number: [],
		city: [],
		state: [],
		zip_code: [],
		country: [],
	};

	console.log(`ProfileUpdateForm.resolvers : ${JSON.stringify(values)}`);

	if(isNil(values.aft_id)){
		errors.aft_id.push({ message : "AFT ID est requis."});
	}

	const myAftId = parseInt( values.aft_id );
	console.log("myAftId : ", myAftId, "\nvalues.aft_id : ", values.aft_id );

	if( myAftId < 1000000 || myAftId > 9999999 ){
		errors.aft_id.push({ message : "AFT ID doit être compris entre 1000000 et 9999999."});
	}

	const validEmail = String(values.email)
		.toLowerCase()
		.match(
			/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
		);

	if(isNil(values.email) || !validEmail){
		errors.email.push({
			message : "Email is invalid."
		});
	}



	if(isNil(values.aft_id)){
		errors.aft_id.push({ message : "AFT ID est requis."});
	}

	return { values, errors };

}

/**
 * Submit method
 * @param param0
 * @param param0.states
 * @param param0.values
 * @param param0.valid
 */
const onSubmit = async ({ states, values, valid }: FormSubmitEvent) => {
	if( valid ){
		toast.add({  severity: "success", summary: "Mise à jour en cours...", life: 3000});
	}

	if(values.new_password.length === 0 || values.confirm_password.length === 0){
		toast.add({
			severity: "error",
			summary : "Mot de passe incorrect!",
			detail : "Entrez votre mot de passe et validez le.",
			life : 3000

		});
		return;
	}

	if(values.new_password.length === 0 || values.new_password !== values.confirm_password){
		toast.add({
			severity: "error",
			summary : "Mot de passe incorrect!",
			detail : "Les deux mots de passe doivent correspondre.",
			life : 3000

		});
		return;
	}

	let ranksInput = [];
	let categoriesInput = [];

	if(states.category.touched && values.category !== ""){
		categoriesInput.push(values.category);
	}

	if(states.rank.touched || states.rank_points.touched){
		if(isNil(values.rank)){
			toast.add({
				severity: "warning",
				summary: "Classement requis.",
				detail : "Sélectionner un classement.",
				life: 3000
			});
			return;
		}else{
			ranksInput.push({
				rank_id : values.rank.id,
				points : values.rank_points,
			});
		}

	}

	let payload = {
		aft_id: values.aft_id,
		email: values.email,
		password : values.new_password,
		annual_fee_paid : false,
		firstname :  values.firstname,
		lastname :  values.lastname,
		gender :  values.gender.value,
		birthdate :  formatISO(values.birthdate, { representation: "date" }),
		phone_number : values.phone_number,
		address: {
			street : values.street,
			number :  values.firstname,
			city :  values.city,
			state :  values.firstname,
			zip_code :  values.zip_code,
			country :  isNil(values.country) ? "Belgique" : values.country,
		},
		member_ranks : ranksInput,
		categories_ids : states.category.touched ? [values.category.id] : []
	}

	const result = await memberService.createMember(payload);

	console.log("MemberCreateForm.onSubmit - response : ");
	console.log(result);

	if(result){
		toast.add({
			severity: "success",
			summary: "Nouveau membre enregistré.",
			life: 3000
		});

		await router.push({ name : "member_list"});
	}

}

onMounted(async () => {



	categories.value = await memberService.getCategories();

	ranks.value = await memberService.getRanks();
})

</script>

<template>
	<section class="flex h-full w-full">
		<ScrollPanel style="width: 100%; height: 400px" class="flex justify-center items-center py-4">
			<Form
				v-slot="$form"
				:resolver
				@submit="onSubmit"
				class="flex w-1/2 gap-4 m-auto justify-center  items-center bg-amber-100 bg-opacity-50 p-4 rounded"
			>
				<div class="flex flex-col gap-y-4 justify-center items-center">
					<Fieldset legend="Informations personnelles" class="gap-4">
						<div class="card grid grid-cols-1 md:grid-cols-2 gap-6 px-4 py-2">
							<InputGroup>
								<InputGroupAddon>
									<PhUserFocus :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="firstname" name="firstname" />
									<label for="firstname">Prénom</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhIdentificationCard :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="lastname" name="lastname" />
									<label for="lastname">Nom</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhGenderIntersex :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<Select
										id="gender"
										name="gender"
										:options="genders"
										optionLabel="text"
									/>
									<label for="gender">Sexe</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhCake :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<DatePicker id="birthdate" name="birthdate" dateFormat="dd/mm/yy" />
									<label for="birthdate">Date de naissance</label>
								</FloatLabel>
							</InputGroup>


						</div>

						<div class="card grid grid-cols-1 md:grid-cols-2 gap-6 px-4 py-4">
							<InputGroup>
								<InputGroupAddon>
									<i class="pi pi-at"></i>
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="email" name="email" type="email" />
									<label for="email">Email</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<i class="pi pi-phone"></i>
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="phone_number" name="phone_number" />
									<label for="phone_number">Numéro de téléphone</label>
								</FloatLabel>
							</InputGroup>
						</div>
					</Fieldset>

					<Fieldset legend="Mot de passe" class="gap-4">
						<div class="card grid grid-cols-1 md:grid-cols-2 gap-6 px-4 py-2">
							<InputGroup>
								<InputGroupAddon>
									<PhUserFocus :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<Password id="new_password" name="new_password" type="password" />
									<label for="new_password">Nouveau mot de passe</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhIdentificationCard :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<Password id="confirm_password" name="confirm_password" type="password" />
									<label for="confirm_password">Confirmer le mot de passe</label>
								</FloatLabel>
							</InputGroup>

						</div>


					</Fieldset>

					<Fieldset legend="Adresse" class="gap-4">
						<div class="card grid grid-cols-1 md:grid-cols-2 gap-6 px-4 py-4">
							<InputGroup>
								<InputGroupAddon>
									<PhHouse :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="street" type="text" name="street" />
									<label for="street">Rue</label>
								</FloatLabel>


							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhHashStraight :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="number" name="number" />
									<label for="number">Numéro</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhCity :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="city" name="city" />
									<label for="city">Ville</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhMapTrifold :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="state" name="state" />
									<label for="state">Province</label>
								</FloatLabel>
							</InputGroup>
						</div>

						<div class="card grid grid-cols-1 md:grid-cols-2 gap-4 px-4 py-4">
							<InputGroup>
								<InputGroupAddon>
									<PhGlobeX :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="zip_code" name="zip_code" />
									<label for="zip_code">Code Postal</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhGlobeHemisphereWest :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="country" name="country" value="Belgique"/>
								</FloatLabel>
							</InputGroup>

						</div>
					</Fieldset>

					<Fieldset legend="Informations AFT" class="gap-4">
						<div class="card grid grid-cols-1 md:grid-cols-2 gap-6 px-4 py-4">
							<InputGroup>
								<InputGroupAddon>
									<PhIdentificationCard :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText id="aft_id" name="aft_id"/>
									<label for="aft_id">AFT ID</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhExam :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<Select
										name="category"
										:options="categories"
										optionLabel="name"
										checkmark
										:highlightOnSelect="false"
										class="w-full md:w-14rem"
									/>
									<label for="category">Choix de catégorie</label>
								</FloatLabel>
							</InputGroup>


							<InputGroup>
								<InputGroupAddon>
									<PhRanking :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<Select
										name="rank"
										:options="ranks"
										optionLabel="name"
										checkmark
										:highlightOnSelect="false"
										class="w-full md:w-14rem"
									/>
									<label for="lastname">Classement</label>
								</FloatLabel>
							</InputGroup>

							<InputGroup>
								<InputGroupAddon>
									<PhTennisBall :size="32" weight="duotone" />
								</InputGroupAddon>
								<FloatLabel>
									<InputNumber id="rank_points" name="rank_points" :min-fraction-digits="2" fluid/>
									<label for="rank_points">Points</label>
								</FloatLabel>
							</InputGroup>
						</div>
					</Fieldset>
					<Fieldset legend="Action" class="w-14 flex p-4">
						<ButtonGroup class="flex gap-4">
							<Button type="submit" severity="success" class="w-50">Valider</Button>
							<Button as="a" href="/home" severity="info" class="text-center">Retour à la page d'accueil</Button>
						</ButtonGroup>
					</Fieldset>
				</div>

			</Form>
		</ScrollPanel>

	</section>
</template>

<style scoped>

</style>