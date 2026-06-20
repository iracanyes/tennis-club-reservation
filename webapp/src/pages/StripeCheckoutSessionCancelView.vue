<script setup lang="ts">

import { Button, Card } from "primevue";
import { router } from "../router.ts";
</script>

<template>
	<div class="h-full w-full flex justify-center items-center">
		<Card>
			<template #title>
				<span>La transaction a été interrompue.</span>
			</template>
			<template #content>
				<p class="m-0">
					Veuillez ré-essayer ultérieurement!  <br>
					Envie d'une réservation ?
				</p>
			</template>
			<template #footer>
				<div class="flex justify-center items-center gap-4 mt-1">
					<Button asChild v-slot="slotProps" size="small" class="">
						<RouterLink to="{{ AppRoutes.Subscribe }}" :class="[slotProps.class, 'flex w-38']">
							S'abonner
						</RouterLink>
					</Button>

					<Button asChild v-slot="slotProps" size="small" severity="info" class="flex w-92">
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