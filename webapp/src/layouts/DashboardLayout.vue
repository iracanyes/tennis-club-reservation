<script setup lang="ts">
import SidebarLeftNav from "@components/navigation/SidebarLeftNav.vue";


</script>

<template>
	<section class="h-full flex flex-row">
		<aside class="flex h-full w-1/8 bg-lime-500">
			<SidebarLeftNav />
		</aside>
		<section class="h-full flex-1 bg-red-500">
			<header class="h-10 bg-lime-50">

			</header>
			<router-view />
		</section>
	</section>

</template>

<style scoped>

</style>