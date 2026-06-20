<script setup lang="ts">
import ApiRoutes from "@navigation/api.routes.ts";
import ApiService from "@services/api.service.ts";
import { useRouter } from "vue-router";
import { TokenService } from "@services";
import { Button } from "primevue";

defineProps({
	type: String,
	buttonId: String,
	cssClasses: String,
	buttonText: String,
})

const router = useRouter();
const apiService = ApiService.getInstance();
const tokenService = TokenService.getInstance();

const logout = async () => {
	try{
		await apiService.post(ApiRoutes.Logout, {});

		tokenService.setToken(null);

		await router.push({ name: "login" });
	}catch (e: any) {
		console.log(e.message)


	}
}
</script>

<template>
	<Button
		id="{{ buttonId }}"
		:label="buttonText"
		icon="pi pi-sign-out"
		@click="logout"
		severity="warn"
		aria-label="Quitter"
		size="small"
		rounded
		raised
		:class="[cssClasses, 'text-sm', 'p-2', 'border-2', 'rounded-sm']"
	/>
</template>

<style scoped>

</style>