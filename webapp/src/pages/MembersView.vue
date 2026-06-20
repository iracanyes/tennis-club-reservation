<script setup lang="ts">
import MemberProfileCardsView from "@components/card/MemberProfileCardsView.vue";
import MembersTableView from "@components/table/MembersTableView.vue";
</script>

<template>
	<div class="h-full w-full flex flex-col bg-amber-400">
		<h1 class="text-white text-lg font-semibold text-center p-2">Dashboard : Gestion des membres</h1>


		<div class="h-full w-full flex flex-row bg-amber-400">
			<div class="h-full w-full">
				<!-- User profile cards -->
				<MemberProfileCardsView />

				<!-- member's reservations list  -->
				<div class="card flex">
					<MembersTableView />
				</div>


			</div>

		</div>

	</div>
</template>

<style scoped>

</style>