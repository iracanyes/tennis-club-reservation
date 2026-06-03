
<script setup lang="ts">


import LoginWithEmailForm from "@components/form/LoginWithEmailForm.vue";
</script>

<template>
  <main class="h-full flex">
    <div class="flex-auto w-1/2 min-h-full bg-yellow-600 ">
      <img src="/src/assets/img/tennis_smash.webp" alt="logo" class="w-3xl h-full"></img>
    </div>
    <div class="flex-auto w-1/2 min-h-full flex-col justify-center bg-yellow-600 px-6 py-15 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm justify-center">
        <img src="/src/assets/img/tsc_logo.png" alt="Your Company" class="mx-auto h-10 w-auto" />
        <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-white">
          Tennis Club - Réservations
        </h2>
        <p class="text-white text-md font-semibold text-center">
          Activer votre compte ou connectez-vous pour accéder à la plateforme d'administration des réservations
          du club de tennis
        </p>
      </div>

			<LoginWithEmailForm />
    </div>
  </main>
</template>

<style scoped>

</style>