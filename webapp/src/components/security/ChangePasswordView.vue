<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import ApiRoutes from "@navigation/api.routes.ts";
import { ApiService } from "@services";

const password = ref('');
const newPassword = ref('');
const confirmNewPassword = ref('');
const router = useRouter();
const apiService = ApiService.getInstance();
const hasError = ref(false);
const error = ref('')

const submit = async (e: Event) => {
	e.preventDefault();

	if(newPassword.value !== confirmNewPassword.value) {
		// Display message
		error.value = "Le nouveau mot de passe doit correspondre dans les 2 champs!";
		hasError.value = true;
		return;
	}

	try {
		let response = await apiService.post(ApiRoutes.ChangePassword, {
			password: password.value,
			new_password: newPassword.value,
			confirm_new_password: confirmNewPassword.value,
		});

		console.log(`submit - response : ${JSON.stringify(response)}`);

		if(response){
			// Notify successfully changed password

			// Return to dashboard
			await router.push({ name: "home" });
		}
	}catch(e : any){
		// Notify error on API call
		console.log(`${e.message}`)
	}
}

</script>

<template>
	<div class="flex-auto w-full min-h-full flex-col justify-center bg-yellow-600 px-6 py-15 lg:px-8">
		<div class="sm:mx-auto sm:w-full sm:max-w-sm justify-center">
			<img src="/src/assets/img/tsc_logo.png" alt="Your Company" class="mx-auto h-10 w-auto" />
			<h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-white">
				Profil - Changer mot de passe
			</h2>
			<p class="text-white text-md font-semibold text-center">
				Activer votre compte ou connectez-vous pour accéder à la plateforme de réservations
			</p>
		</div>

		<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
			<form class="space-y-6">

				<div>
					<div class="flex items-center justify-between">
						<label for="password" class="block text-sm font-semibold text-gray-100">
							Mot de passe
						</label>
						<div class="text-sm">
							<a href="#" class="font-semibold text-indigo-400 hover:text-indigo-300">
								Mot de passe oublié?
							</a>
						</div>
					</div>
					<div class="mt-2">
						<input
							id="password"
							type="password"
							name="password"
							v-model="password"
							required
							autocomplete="current-password"
							class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-black outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6" />
					</div>
				</div>

				<div>
					<div class="flex items-center justify-between">
						<label for="new_password" class="block text-sm font-semibold text-gray-100">
							Nouveau mot de passe
						</label>
					</div>
					<div class="mt-2">
						<input
							id="new_password"
							type="password"
							name="new_password"
							v-model="newPassword"
							required
							class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-black outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6" />
					</div>
				</div>

				<div>
					<div class="flex items-center justify-between">
						<label for="confirm_new_password" class="block text-sm font-semibold text-gray-100">
							Confirmer le nouveau mot de passe
						</label>
					</div>
					<div class="mt-2">
						<input
							id="confirm_new_password"
							type="password"
							name="confirm_new_password"
							v-model="confirmNewPassword"
							required
							class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-black outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6" />
					</div>
				</div>

				<div class="flex flex-col gap-y-4 mt-10">
					<button
						type="submit"
						@click="submit"
						class="w-full justify-center rounded-md bg-lime-400 px-3 py-1.5 text-sm/6 font-semibold text-white hover:bg-lime-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
					>
						Confirmer
					</button>
					<RouterLink to="/dashboard" class="w-full">
						<button
							type="button"
							class="w-full justify-center rounded-md bg-amber-800 px-3 py-1.5 text-sm/6 font-semibold text-white hover:bg-amber-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
						>
							Retour
						</button>
					</RouterLink>

				</div>

			</form>




		</div>
	</div>
</template>

<style scoped>

</style>