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
		<section class="h-full flex-1 bg-red-500">
			<header class="h-10 bg-lime-50 flex flex-row">
				<div class="w-1/3 flex bg-red-400"></div>
				<div class="w-1/3 flex bg-yellow-400"></div>
				<div class="w-1/3 flex bg-lime-400 p-2 justify-end">
					<LogoutButton
						type="button"
						id="logout_button"
						cssClasses="w-12 border-1 rounded-sm border-gray-400"
						buttonText="Se déconnecter"
					/>
				</div>
			</header>
			<Toast />
			<router-view />
		</section>
	</section>

</template>

<style scoped>

</style>