<script setup lang="ts">
import {ref, onMounted, type Ref} from "vue";
import { Card, Button, useToast } from "primevue";
import {ApiService} from "@services";
import ApiRoutes from "@navigation/api.routes.ts";
import type {Plan} from "../dto";
const toast = useToast();
const apiService = ApiService.getInstance();
const plans: Ref<Plan[], Plan[]> = ref([]);

onMounted(async () => {
	try{
		const response = await apiService.get(ApiRoutes.PlanList);

		console.log(`SubscribeView onMounted - plans - response : `, JSON.stringify(response));

		if(response.length > 0){
			plans.value = response;
		}
	}catch(error: any){
		console.error(error);

		toast.add({
			severity: "error",
			summary: "Une erreur est survenue lors de la récupérations des abonnements.",
			detail: error.message,
		});
	}
})

const buy = async (plan: Plan) => {
	console.log(`SubscribeView buy() - plan : ${JSON.stringify(plan)}`);

	try{
		const response = await apiService.post(ApiRoutes.StripeCheckoutSession, { id : plan.id });

		console.log(`SubscribeView.buy() - response.url : `, JSON.stringify(response));

		if(response.url.startsWith("https://checkout.stripe.com")){
			//await router.push(response.url);
			globalThis.location.href = response.url;
		}

	}catch(error: any){
		console.error(`SubscribeView errors: `, error);

		toast.add({
			severity: "error",
			summary : "Erreur : Stripe checkout session",
			detail: error.message,
		})
	}
}


</script>

<template>
	<main class="h-full w-full bg-amber-500 flex flex-col justify-center items-center">
		<div class="p-2 bg-blue-400 mb-8">
			<h1 class="text-xl font-semibold text-center">S'abonner</h1>
			<p class="font-semibold text-black-500">
				Sélectionner votre abonnement, puis procéder au paiement. <br>
				Vous serez redirigé vers notre partenaire pour les paiements en ligne Stripe.
			</p>
		</div>
		<div class="flex flex-row gap-x-4">
			<Card v-for="plan in plans" style="width: 25rem; overflow: hidden">
				<template #header>
					<img class="h-48 w-full" alt="user header" :src="plan.img_src" />
				</template>
				<template #title>
					<span class="font-semibold">
						{{ plan.title }}
					</span>
				</template>
				<template #subtitle>
					<span class="text-amber-600 font-semibold text-lg">
						{{ plan.price }} {{ plan.currency_symbol}}
					</span>
				</template>
				<template #content>
					<h4 class="mb-2 font-semibold">
						{{ plan.subtitle }}
					</h4>
					<p class="m-0 text-sm">
						{{ plan.summary}}
					</p>
				</template>
				<template #footer>
					<div class="flex gap-4 mt-1">
						<Button label="Voir le détail" class="w-full" />
						<Button label="S'abonner" class="w-full" @click.prevent="buy(plan)"/>
					</div>
				</template>
			</Card>

		</div>
	</main>
</template>

<style scoped>

</style>