<script setup lang="ts">
import { ref } from "vue";

import {
	PhAddressBookTabs,
	PhCalendarDots,
	PhRacquet,
	PhTennisBall,
	PhUserCircleCheck, PhUserCirclePlus,
	PhUserSwitch
} from "@phosphor-icons/vue";
import ApiService from "@services/api.service.ts";


</script>

<template>
	<section id="profile">
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
	</section>
</template>

<style scoped>

</style>