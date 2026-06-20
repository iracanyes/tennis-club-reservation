<script setup lang="ts">
import CourtReservationsTableView from "@components/table/CourtReservationsTableView.vue";
import MemberProfileCardsView from "@components/card/MemberProfileCardsView.vue";



</script>

<template>
	<div class="h-full w-full flex flex-col bg-amber-400">
		<h1 class="text-white text-lg font-semibold text-center p-2">Dashboard : Réservations par court de tennis</h1>


		<div class="h-full w-full flex flex-row bg-amber-400">
			<div class="h-full w-full ">
				<!-- 4 small cards -->
				<MemberProfileCardsView />

				<!-- member's reservations list  -->
				<div class="card flex">
					<CourtReservationsTableView />
				</div>


			</div>




		</div>

	</div>
</template>

<style scoped>

</style>