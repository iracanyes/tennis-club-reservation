<script setup lang="ts">

import { Button, Card } from "primevue";
import { router } from "../router.ts";
</script>

<template>
	<div class="flex justify-center align-center">
		<Card>
			<template #title>
				<span>La transaction a été interrompue, une erreur est survenue</span>
			</template>
			<template #content>
				<p class="m-0">
					Veuillez ré-essayer ultérieurement!  <br>
					Envie d'une réservation ?
				</p>
			</template>
			<template #footer>
				<div class="flex gap-4 mt-1">
					<Button label="Ajouter une réservation" class="w-full"  @click.prevent="router.push({ name : 'add_reservation'})"/>
					<Button label="Retour au dashboard" class="w-full" @click.prevent="router.push({ name : 'home'})"/>
				</div>
			</template>
		</Card>
	</div>
</template>

<style scoped>

</style>