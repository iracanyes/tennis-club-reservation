<script setup lang="ts">
import {ref, onMounted, type Ref, computed} from "vue";
import { useRouter} from "vue-router";
import {isNil} from "lodash";
import {
	Button,
	ButtonGroup,
	Checkbox,
	Column,
	DataTable,
	FloatLabel,
	InputGroup,
	InputGroupAddon,
	InputText,
	Select,
	ScrollPanel,
	Tag,
	ToggleSwitch
} from "primevue";
import type {Category, Member, Rank} from "@dto";
import {MemberService, TokenService} from "@services";
import AppRoutes from "@navigation/app.routes.ts";
import {formatISO} from "date-fns";

const router = useRouter();
const tokenService = TokenService.getInstance();
const memberService = MemberService.getInstance();
const members = ref<Member[]>([]);
const enableCategoryFilter = ref(false);
const enableRankFilter = ref(false);
const enableRankSorting = ref(false);
const toggleRankSortDirection = ref(false);
const category : Ref<Category| null> = ref(null);
const categories: Ref<Category[]> = ref([]);
const rank: Ref<Rank|null> = ref(null);
const ranks: Ref<Rank[]> = ref([]);


onMounted(async () => {

	try {
		members.value = await memberService.getMembers();
	}catch (e) {
		console.error(e);
	}

	try {
		ranks.value = await memberService.getRanks();
	}catch (e) {
		console.error(e);
	}

	try {
		categories.value = await memberService.getCategories();
	}catch (e) {
		console.error(e);
	}

});

/**
 *
 * @param member
 */
const getSeverity = (member: Member) => {
	console.log("MembersView.getSeverity - ",member);
	if(member.annual_fee_paid){
		return 'success';
	}else{
		return 'warn';
	}
	return 'secondary';
};

/**
 * Delete member method
 * @param member
 */
const deleteMember = async (member: Member) => {
	console.log("MembersView.deleteMember - ",member);
	try {
		const result = await memberService.deleteMember(member);

		console.log("MembersView.deleteMember result : ",result);
		if(result){
			router.go(0);
		}
	}catch (e: any) {
		console.error("MembersView.deleteMember errors : ",e);
	}
}

/**
 * Computed list of members after filter and sort
 */
const filteredMembers  = computed (() => {
	if(members.value.length === 0){
		return [];
	}

	let memberList = [...members.value];

	if(enableCategoryFilter.value && !isNil(category.value)){
		memberList = memberList.filter( item => item.categories[0].name === category.value.name);
	}

	if(enableRankFilter.value && !isNil(rank.value)){
		memberList = memberList.filter( item => item.member_ranks[0].rank.name === rank.value.name);
	}

	if(enableRankSorting.value){
		memberList = memberList.sort((a, b) => {
			if(a.member_ranks[0].rank.name === b.member_ranks[0].rank.name) {
				if (a.member_ranks[0].points > b.member_ranks[0].points) {
					return toggleRankSortDirection ? -1 : 1;
				} else if (a.member_ranks[0].points < b.member_ranks[0].points) {
					return toggleRankSortDirection ? 1 : -1;
				} else {
					return 0;
				}
			}

			return a.member_ranks[0].rank.name.localeCompare(b.member_ranks[0].rank.name);
		}).reverse();

		if(toggleRankSortDirection.value){
			memberList = memberList.reverse();
		}


	}

	return memberList;
});


const resetFilters = () => {
	enableCategoryFilter.value = false;
	enableRankFilter.value = false;
	category.value = null;
	rank.value = null;
	enableRankSorting.value = false;
	toggleRankSortDirection.value = false;
}

</script>

<template>
	<section id="ownReservationsTable" class="flex flex-col h-full justify-center items-center w-full mx-auto">
		<section id="filtres" class="m-4">
			<div class="flex flex-row gap-x-4">
				<div class="flex flex-col gap-y-4">
					<div class="flex flex-row">
						<div class="flex w-30 justify-center items-center">
							<h5 class="text-center text-lg font-semibold">
								Filtres :
							</h5>
						</div>
						<div class="flex flex-row gap-5 w-120">
							<InputGroup>
								<InputGroupAddon>
									<Checkbox v-model="enableCategoryFilter" :binary="true" />
								</InputGroupAddon>
								<FloatLabel>
									<Select
										v-model="category"
										:options="categories"
										optionLabel="name"
										checkmark
										:highlightOnSelect="false"
										class="w-full md:w-14rem"
									/>
									<label for="lastname">Catégorie</label>
								</FloatLabel>
							</InputGroup>
							<InputGroup>
								<InputGroupAddon>
									<Checkbox v-model="enableRankFilter" :binary="true" />
								</InputGroupAddon>
								<FloatLabel>
									<Select
										v-model="rank"
										:options="ranks"
										optionLabel="name"
										checkmark
										:highlightOnSelect="false"
										class="w-full md:w-14rem"
									/>
									<label for="lastname">Classement</label>
								</FloatLabel>

							</InputGroup>
						</div>
					</div>
					<div class="flex flex-row">
						<div class="flex w-30 justify-center items-center">
							<h5 class="text-center text-lg font-semibold">
								Tri :
							</h5>
						</div>
						<div class="flex flex-row gap-5 w-120">
							<InputGroup>
								<InputGroupAddon>
									<Checkbox v-model="enableRankSorting" :binary="true" />
								</InputGroupAddon>
								<FloatLabel>
									<InputText
										disabled
										size="small"
										class="w-full md:w-14rem"
									/>
									<label for="lastname">Classement</label>
								</FloatLabel>
								<InputGroupAddon class="w-20">
									<ToggleSwitch v-model="toggleRankSortDirection" >
										<template #handle="{ checked }">
											<i :class="['!text-xs pi', { 'pi-sort-amount-up': checked, 'pi-sort-amount-up-alt': !checked }]" />
										</template>
									</ToggleSwitch>
								</InputGroupAddon>
								<InputGroupAddon class="w-40">Asc/Desc</InputGroupAddon>
							</InputGroup>
						</div>
					</div>
				</div>


				<div class="flex flex-row gap-5">
					<div class="h-10">
						<Button
							severity="info"
							icon="pi pi-trash"
							label="Effacer"
							size="small"
							raised
							@click="resetFilters()"
						/>
					</div>

				</div>
			</div>
		</section>
		<ScrollPanel style="min-width: 790px;width: 1080px;height: 500px">
			<DataTable
				:value="filteredMembers"
				size="small"
				paginator
				:rows="5"
				:rowsPerPageOptions="[5, 10, 20, 50]"
				tableStyle="min-width: 30rem; font-size: small;max-width: 650px;margin: 0 auto"
			>
				<Column
					field="aft_id"
					header="AFT ID"
					style="width: 25%"
					sortable
				></Column>
				<Column
					field="firstname"
					header="Prénom"
					style="width: 25%"
					sortable
				></Column>
				<Column
					field="lastname"
					header="Nom"
					style="width: 25%"
					sortable
				>
					<template #body="slotProps">
						{{ slotProps.data.lastname }}
					</template>
				</Column>
				<Column field="gender" header="Sexe" style="width: 25%"></Column>
				<Column header="Date de naissance" style="width: 25%">
					<template #body="slotProps">
						{{ formatISO(slotProps.data.birthdate, { representation: "date" }) }}
					</template>
				</Column>
				<Column field="email" header="Email" style="width: 25%"></Column>
				<Column field="phone_number" header="N° de téléphone" style="width: 25%"></Column>
				<Column
					header="Catégorie"
					style="width: 25%"
					field="categories[0].name"
				>
					<template #body="slotProps">
						<span v-if="slotProps.data.categories.length > 0">
							{{ slotProps.data.categories[0].name }}
						</span>
					</template>
				</Column>
				<Column
					header="Classement"
					style="width: 25%"
					field="member_ranks[0].rank.name"
				>
					<template #body="slotProps">
						<span v-if="slotProps.data.member_ranks.length > 0">
							{{ slotProps.data.member_ranks[0].rank.name }}
						</span>
					</template>
				</Column>
				<Column
					header="Points"
					style="width: 25%"
				>
					<template #body="slotProps">
						<span v-if="slotProps.data.member_ranks.length > 0">
							{{ slotProps.data.member_ranks[0].points }}
						</span>
					</template>
				</Column>
				<Column header="En ordre de côtisation">
					<template #body="slotProps">
						<Tag :value="slotProps.data.annual_fee_paid" :severity="getSeverity(slotProps.data)" />
					</template>
				</Column>
				<Column v-if="tokenService.isAdmin.value" field="address" header="Adresse" style="width: 25%">
					<template #body="slotProps">
						{{   ( slotProps.data.address.street
						+ " "
						+ slotProps.data.address.number + ", \n"
						+ slotProps.data.address.city + "(" + slotProps.data.address.state + ")\n"
						+ slotProps.data.address.zip_code + " " + slotProps.data.address.country ) }}
					</template>
				</Column>
				<Column header="Action">
					<template #body="slotProps">

						<div class="flex flex-col gap-2 ">

							<Button
								v-if="tokenService.isAdmin.value"
								icon="pi pi-pen-to-square"
								as="a"
								:href="router.resolve({ name: 'member_update', params : { id: slotProps.data.id}}).href"
								severity="info"
								label="Update"
								size="small"
							/>


							<Button
								v-if="tokenService.isAdmin.value"
								label="Delete"
								icon="pi pi-trash"
								severity="warn"
								size="small"
								@click="deleteMember(slotProps.data)"
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
		</ScrollPanel>

	</section>
</template>

<style scoped>
table{
	width: 30rem;
}
</style>