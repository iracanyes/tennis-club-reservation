<script setup lang="ts">

import MemberProfileCardsView from "@components/card/MemberProfileCardsView.vue";
import ProfileUpdateForm from "@components/form/ProfileUpdateForm.vue";
</script>

<template>
	<div class="h-full w-full flex flex-col bg-amber-400">
		<h1 class="text-white text-lg font-semibold text-center p-2">
			Dashboard : Mise à jour du profil
		</h1>


		<div class="h-full w-full flex flex-row bg-amber-400">
			<div class="h-full w-full ">
				<!-- 4 small cards -->
				<MemberProfileCardsView />

				<!-- member's reservations list  -->
				<div class="card flex">
					<ProfileUpdateForm />
				</div>


			</div>




		</div>

	</div>
</template>

<style scoped>

</style>