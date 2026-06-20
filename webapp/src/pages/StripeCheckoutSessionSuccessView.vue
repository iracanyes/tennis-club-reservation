<script setup lang="ts">
import {Button, Card} from "primevue";
import AppRoutes from "@navigation/app.routes.ts";

</script>

<template>
	<div class="flex w-full h-full justify-center items-center">
		<Card class="flex h-content">
			<template #title>
				<span>Félicitation pour ce nouveau abonnement</span>
			</template>
			<template #content>
				<p class="m-0">
					Profitez de nos services : <br>
					Envie d'une réservation ?
				</p>
			</template>
			<template #footer>
				<div class="flex justify-center items-center gap-4 mt-1">

					<Button asChild v-slot="slotProps" size="small">
						<RouterLink to="{{ AppRoutes.MyReservations }}" :class="slotProps.class">
							Ajouter une réservation
						</RouterLink>
					</Button>

					<Button asChild v-slot="slotProps" size="small">
						<RouterLink to="{{ AppRoutes.DashboardHome }}" :class="slotProps.class">
							Retour page d'accueil
						</RouterLink>
					</Button>
				</div>
			</template>
		</Card>
	</div>
</template>

<style scoped>

</style>