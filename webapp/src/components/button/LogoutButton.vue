<script setup lang="ts">
defineProps({
	type: String,
	buttonId: String,
	cssClasses: String,
})

const logout = async () => {
	try{

	}catch (e: any) {
		console.log(e.message)
	}
}
</script>

<template>
	<button
		id="{{ buttonId }}"
		type="button"
		class="{{ cssClasses }}"
		@click="logout"
	/>
</template>

<style scoped>

</style>