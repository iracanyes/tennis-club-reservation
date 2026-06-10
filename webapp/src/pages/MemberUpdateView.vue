<script setup lang="ts">
import MemberProfileCardsView from "@components/card/MemberProfileCardsView.vue";
import {useRoute, useRouter} from "vue-router";
import {TokenService} from "@services";
import {onMounted} from "vue";
import MemberUpdateForm from "@components/form/MemberUpdateForm.vue";

const route = useRoute();
const router = useRouter();
const tokenService = TokenService.getInstance();

onMounted(() => {
	if(!tokenService.isAdmin){
		router.push('home')
	}

	console.log("MemberUpdateView route.params.id : ", "\nRoute : ", route.params.id);
})
</script>

<template>
	<div class="h-full flex flex-col bg-amber-400">
		<h1 class="text-white text-lg font-semibold text-center p-2">
			Dashboard : Mise à jour du profil d'un membre
		</h1>


		<div class="h-full w-full flex flex-row bg-amber-400">
			<div class="h-full w-full ">
				<!-- 4 small cards -->
				<MemberProfileCardsView />

				<!-- member's reservations list  -->
				<div class="card flex">
					<MemberUpdateForm :id="route.params.id" />
				</div>


			</div>




		</div>

	</div>
</template>

<style scoped>

</style>