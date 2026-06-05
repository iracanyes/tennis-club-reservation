<script setup lang="ts">
import {
	PhAddressBookTabs, PhCalendarDots,
	PhChartLineUp, PhCurrencyEur,
	PhRacquet,
	PhTennisBall,
	PhUserCircleCheck,
	PhUserCirclePlus, PhUserSwitch
} from "@phosphor-icons/vue";
import CourtsTableView from "@components/table/CourtsTableView.vue";
import CreateCourtForm from "@components/form/CreateCourtForm.vue";



</script>

<template>
	<div class="h-full flex flex-col bg-amber-400">
		<h1 class="text-white text-lg font-semibold text-center p-2">Dashboard : Terrains</h1>


		<div class="h-full w-full flex flex-row bg-amber-400">
			<div class="h-full w-3/4 ">
				<!-- 4 small cards -->
				<div class="p-2 flex flex-row justify-center gap-x-4 p-4">
					<!-- Card -->
					<div  class="flex flex-row p-0 rounded-md shadow-lg border border-sky-600 outline-sky-600 bg-sky-400 ">
						<div class="bg-white-200 p-2 flex justify-center items-center">
							<PhUserCirclePlus :size="32" />
						</div>
						<div class="p-2">
							<p class="text-base font-semibold">Rang</p>
							<p class="text-sm font-semibold">123</p>
						</div>
						<div class="flex justify-end items-end p-2">
							<PhAddressBookTabs color="gray" :size="42" stroke="2" weight="duotone" />
						</div>
					</div>

					<!-- Card -->
					<div id="home_card1"  class="flex flex-row p-0 rounded-md shadow-lg border border-lime-600 bg-lime-400 ">
						<div class="bg-white-200 p-2 flex justify-center items-center">
							<PhTennisBall :size="32" stroke="1" weight="duotone"/>
						</div>
						<div class="p-2">
							<h4 class="font-semibold">Catégorie</h4>
							<h5 class="font-semibold">Inconnu</h5>
						</div>
						<div class="flex justify-end items-end p-2">
							<PhRacquet color="orange" :size="42" stroke="1" weight="duotone" />
						</div>
					</div>

					<!-- Card -->
					<div id="home_card2" class="flex flex-row p-0 rounded-md shadow-lg border border-cyan-600 bg-cyan-400 ">
						<div class="bg-white-200 p-2 flex justify-center items-center">
							<PhTennisBall :size="32" stroke="1" weight="duotone"/>
						</div>
						<div class="p-2">
							<h4 class="font-semibold">Événements</h4>
							<h5 class="font-semibold">12</h5>
						</div>
						<div class="flex justify-end items-end p-2">
							<PhCalendarDots color="orange" :size="42" stroke="1" weight="duotone" />
						</div>
					</div>

					<!-- Card -->
					<div id="home_card3" class="flex flex-row p-0 rounded-md border shadow-lg border-indigo-600 bg-indigo-400">
						<div class="bg-white-200 p-2 flex justify-center items-center">
							<PhUserCircleCheck :size="32" weight="duotone"/>
						</div>
						<div class="p-2">
							<p class="text-md font-semibold">Réservations</p>
							<p class="text-sm font-semibold">12</p>
						</div>
						<div class="flex justify-end items-end p-2">
							<PhUserSwitch color="orange" :size="42" stroke="2" weight="duotone"/>
						</div>
					</div>
				</div>

				<!-- member's reservations list  -->
				<div class="card flex">
					<CourtsTableView />
				</div>


			</div>
			<div class="w-1/4 h-full gap-y-4">
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
						<CreateCourtForm />
					</div>
				</div>
			</div>

		</div>

	</div>
</template>

<style scoped>

</style>