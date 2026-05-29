<script setup lang="ts">

import { Button, Card } from "primevue";
import { router } from "../router.ts";
</script>

<template>
	<div class="h-full flex justify-center items-center">
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
				<div class="flex gap-4 mt-1">
					<Button label="S'abonner" class="w-full"  @click.prevent="router.push({ name : 'subscribe'})"/>
					<Button label="Retour au dashboard" class="w-full" @click.prevent="router.push({ name : 'home'})"/>
				</div>
			</template>
		</Card>
	</div>
</template>

<style scoped>

</style>