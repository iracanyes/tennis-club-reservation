<script setup lang="ts">

import {Button, Card} from "primevue";
import {router} from "../router.ts";
</script>

<template>
	<div class="flex justify-center align-center">
		<Card class="flex">
			<template #title>
				<span>Félicitation pour ce nouveau abonnement</span>
			</template>
			<template #content>
				<p class="m-0">
					Merci pour l'achat d'un abonnement : <br>
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