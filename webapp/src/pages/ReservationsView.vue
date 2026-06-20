<script setup lang="ts">
import {
	PhChartLineUp, PhCurrencyEur,
} from "@phosphor-icons/vue";
import CreateReservationForm from "@components/form/CreateReservationForm.vue";
import MemberProfileCardsView from "@components/card/MemberProfileCardsView.vue";
import ReservationsTableView from "@components/table/ReservationsTableView.vue";
import {TokenService} from "@services";

const tokenService = TokenService.getInstance();
</script>

<template>
	<div class="h-full w-full flex flex-col bg-amber-400">
		<h1 class="text-white text-lg font-semibold text-center p-2">
			Dashboard : Réservations
		</h1>


		<div class="h-full w-full flex flex-row bg-amber-400">
			<div class="h-full flex-1 ">
				<!-- User profile cards -->
				<MemberProfileCardsView />

				<!-- member's reservations list  -->
				<div class="card flex">
					<ReservationsTableView />
				</div>


			</div>
			<div v-if="tokenService.isAdmin.value" class="w-1/4 h-full gap-y-4">
				<div class="flex flex-col p-2 gap-y-4">
					<!-- Card -->
					<div  class="flex flex-row p-0 justify-between rounded-md border shadow-lg border-emerald-600 bg-emerald-400 ">
						<div class="bg-white-200 p-2 flex justify-center items-center">
							<PhCurrencyEur :size="42" weight="duotone"/>
						</div>
						<div class="p-2">
							<p class="text-xl font-semibold">Chiffre d'affaires</p>
							<p class="text-base">1231231.23 €</p>
						</div>
						<div class="flex justify-end items-end p-2">
							<PhChartLineUp color="gray" :size="52" stroke="2" weight="duotone" />
						</div>
					</div>


					<div>
						<!-- Create reservation form -->
						<CreateReservationForm />
					</div>
				</div>
			</div>

		</div>

	</div>
</template>

<style scoped>

</style>