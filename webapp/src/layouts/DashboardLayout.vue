<script setup lang="ts">
import SidebarLeftNav from "@components/navigation/SidebarLeftNav.vue";
import LogoutButton from "@components/button/LogoutButton.vue";
import { Toast } from "primevue";

</script>

<template>
	<section class="h-full flex flex-row">
		<aside class="flex h-full w-1/8 bg-lime-500">
			<SidebarLeftNav />
		</aside>
		<section class="flex flex-col h-full flex-1 bg-amber-600">
			<header class="h-12 bg-amber-700 flex flex-row">
				<div class="w-1/3 flex "></div>
				<div class="w-1/3 flex-1 "></div>
				<div class="w-1/3 flex p-2 justify-end">
					<LogoutButton
						type="button"
						id="logout_button"
						cssClasses="border-1 rounded-sm border-gray-400"
						buttonText="Quitter"
					/>
				</div>
			</header>

			<div class="flex flex-1">
				<Toast />
				<router-view />
			</div>

		</section>
	</section>

</template>

<style scoped>

</style>