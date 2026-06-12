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
	ScrollPanel,
	Select,
	useToast,
} from "primevue";
import { APIService, MemberService } from "@services";
import ApiRoutes from "@navigation/api.routes.ts";
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
import z from "zod";
import {zodResolver} from "@primevue/forms/resolvers/zod";

const route = useRoute();
const router = useRouter();
const toast = useToast();
const apiService = APIService.getInstance();
const memberService = MemberService.getInstance();
const profile = ref();
const genders = ref(GenderTypeEnum);
const ranks: Ref<Rank[]> = ref([]);
const categories: Ref<Category[]> = ref([]);
const resolver = ref();
const initialValues = reactive({
	id: "",
	aft_id: "",
	email: "",
	firstname: "",
	lastname: "",
	gender: null,
	birthdate: "",
	phone_number: "",
	category: null,
	rank: null,
	rank_points : null,
	address_id: "",
	street: "",
	number: "",
	city: "",
	state: "",
	zip_code: "",
	country: "",
});



const onSubmit = async ({ errors, states, values, valid }: FormSubmitEvent) => {
	if( valid ){
		toast.add({  severity: "success", summary: "Mise à jour en cours...", life: 3000});
	}

	console.log("resolver.errors")
	console.log(errors);
	console.log("FormSubmitEvent.values")
	console.log(values);

	for(let key in errors){
		for (let error in errors[key]){
			toast.add({
				severity: "error",
				summary: key + " : Error",
				detail: errors[key][error]["message"],
				life: 5000
			})
		}
	}

	if(isNil(values)){
		return;
	}

	// Member's rank and category input
	let ranksInput = [];
	let categoriesInput = profile.value.categories;

	if(states.category.touched && values.category !== ""){
		categoriesInput.push(values.category);
	}

	if(states.rank.touched || states.rank_points.touched){
		if(isNil(initialValues.rank)){
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
		}else{
			ranksInput.push({
				rank_id : initialValues.rank.id,
				points : values.rank_points,
			});
		}

	}

	let payload = {
		id: profile.value.id,
		aft_id: profile.value.aft_id,
		email: profile.value.email,
		annual_fee_paid : profile.value.annual_fee,
		firstname : isEmpty(values.firstname) ? profile.value.firstname : values.firstname,
		lastname : isEmpty(values.lastname) ?  profile.value.lastname : values.lastname,
		gender : isEmpty(values.gender) ? profile.value.gender : values.gender.value,
		birthdate : isEmpty(values.birthdate) ? profile.value.birthdate : formatISO(values.birthdate, { representation: "date" }),
		phone_number : isEmpty(values.phone_number) ? profile.value.phone_number : values.phone_number,
		address: {
			street : isEmpty(values.street) ? profile.value.address.street : values.street,
			number : isEmpty(values.number) ? profile.value.address.number : values.firstname,
			city : isEmpty(values.city) ? profile.value.address.city : values.city,
			state : isEmpty(values.number) ? profile.value.address.number : values.firstname,
			zip_code : isEmpty(values.zip_code) ? profile.value.address.zip_code : values.zip_code,
			country : isEmpty(values.country) ? profile.value.address.country : values.country,
		},
		member_ranks : ranksInput,
		categories_ids : states.category.touched ? [values.category.id] : []
	}

	const result = await memberService.updateProfile(payload);

	console.log("ProfileUpdateForm.onSubmit - response : ");
	console.log(result);

	if(result){
		toast.add({
			severity: "success",
			summary: "Successfully updated profile update.",
			life: 3000
		});

		await router.push({ name : "home"});
	}

}

onMounted(async () => {

	console.log("MemberUpdateForm.onSubmit - route.params.id : : ", route.params.id);
	// Get profile info
	const result = await apiService.get(ApiRoutes.MemberRetrieve + route.params.id);

	console.log("Profile : \n", result);
	console.log("member_rank0_points : ", result.member_ranks.length > 0 && result.member_ranks[0].points > 0 ? result.member_ranks[0].points : null)

	if (result) {
		profile.value = result;
		initialValues.id = result.id;
		initialValues.aft_id = result.aft_id;
		initialValues.email = result.email;
		initialValues.firstname = result.firstname;
		initialValues.lastname = result.lastname;
		initialValues.gender = result.gender === "M" ? GenderTypeEnum[0] : GenderTypeEnum[1];
		initialValues.birthdate = new Date(result.birthdate).toLocaleDateString();
		initialValues.phone_number = result.phone_number;
		initialValues.rank = result.member_ranks.length > 0 ? result.member_ranks[0].rank : null;
		initialValues.rank_points = result.member_ranks.length > 0 && result.member_ranks[0].points > 0 ? result.member_ranks[0].points : null;
		initialValues.category = result.categories.length > 0 ? result.categories[0] : null;
		initialValues.address_id = result.address.id;
		initialValues.street = result.address.street;
		initialValues.number = result.address.number;
		initialValues.city = result.address.city;
		initialValues.state = result.address.state;
		initialValues.zip_code = result.address.zip_code;
		initialValues.country = result.address.country;

		console.log("ProfileUpdate.onMounted - initialValues : ")
		console.log( initialValues)


	}

	categories.value = await memberService.getCategories();

	ranks.value = await memberService.getRanks();

	// Define validation resolver using zod library
	resolver.value = zodResolver(
		z.object({
			firstname : z.string().min(2, "Prénom requis.").or(z.literal('')),
			lastname : z.string().min(2, "Nom requis.").or(z.literal('')),
			gender : z.nullable(
				z.object({
					key : z.enum(['MALE', 'FEMALE']),
					value : z.string().min(1, "La valeur pour le genre doit être 'M' ou 'F'."),
					text : z.enum(['Mâle', 'Femelle'])
				})
					.or(z.literal(''))
			),
			birthdate : z.nullable(
				z.date()
					.min(new Date("1945-01-01"), { error : "Trop âgé."})
					.max(new Date(new Date().setFullYear(new Date().getFullYear() - 5)))
					.or(z.literal(''))
			),
			email : z.email({ message : "Entrez un email valide."})
				.min(2, "Nom requis.")
				.or(z.literal('')),
			phone_number : z.string()
				.trim()
				.min(2, "N° de téléphone requis.")
				.or(z.literal('')),
			street : z.string()
				.min(3, "Indiquez pour votre adresse la rue.")
				.or(z.literal('')),
			number : z.string()
				.min(1, "Indiquez pour votre adresse le numéro.")
				.or(z.literal('')),
			city : z.string()
				.min(2, "Indiquez pour votre adresse la ville.")
				.or(z.literal('')),
			state : z.string()
				.min(2, "Indiquez pour votre adresse la province.")
				.or(z.literal('')),
			zip_code : z.string()
				.min(3, "Indiquez pour votre adresse le code postal.")
				.or(z.literal('')),
			country : z.string()
				.min(3, "Indiquez pour votre adresse la rue.")
				.or(z.literal('')),
			aft_id : z.preprocess(
				(val) => {
					if (typeof val === "string") {
						return Number.parseInt(val);
					}
					return val;
				},
				z.int()
					.min(1000000, "AFT ID doit être supérieur à 1000000")
					.max(9999999, "AFT ID doit être inférieur à 9999999")
			).or(z.literal('')),
			category : z.nullable(z.strictObject({
				id : z.uuid(),
				name : z.enum(Array.from(categories.value, (category) => category.name)),
				age_min : z.nullable(z.number().min(1, "Âge minimum : 5ans")),
				age_max : z.nullable(z.number().max(80, "Âge maximum : 80ans")),
				birth_year_min : z.nullable(z.number().min(1946, "Année de naissance minimale : 5ans")),
				birth_year_max : z.nullable(z.number().max(new Date().getFullYear() - 5, "Année de naissance minimale : 5ans")),
				gender : z.enum(Array.from(GenderTypeEnum, (x) => x.value)),
				description : z.string()

			})),
			rank : z.nullable(z.strictObject({
				id : z.uuid(),
				name: z.enum(Array.from(ranks.value, (rank) => rank.name)),
			})),
			rank_points : z.number(),

		})
	);
})

</script>

<template>
	<section class="flex h-full w-full">
		<ScrollPanel style="width: 100%; height: 400px" class="flex justify-center items-center py-4">
			<Form
				v-slot="$form"
				:initialValues
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
									<DatePicker id="birthdate" name="birthdate"  dateFormat="dd/mm/yy" />
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
									<InputText id="email" name="email" type="email"/>
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
									<InputText id="aft_id" name="aft_id" disabled="true"/>
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