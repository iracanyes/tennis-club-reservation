<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import ApiRoutes from "@navigation/api.routes.ts";
import {APIService, CSRFService, TokenService} from "@services";

const aft_id = ref('');
const password = ref('');
const router = useRouter();
const apiService = APIService.getInstance();
const tokenService = TokenService.getInstance();
const csrfTokenService = CSRFService.getInstance();

async function submit(e : Event){
  e.preventDefault();

  try{
    let response = await apiService.post(
			ApiRoutes.MemberLogin,
			{ aft_id : aft_id.value, password: password.value }
		);

		console.log(`submit - response : ${JSON.stringify(response)}`)
    if(response.token && response.token !== ""){
      tokenService.setToken(response);

			// CSRF Token has been rotated on login. Delete CSRF Token
			csrfTokenService.deleteToken();

			console.log(`LoginView - previous route : `, router.options.history.state.back)

      // Redirect to dashboard
			if(typeof router.options.history.state.back === "string" ){
				await router.push((router.options.history.state.back as string));
			}else{
				await router.push({
					name: 'home',
				});
			}

    }

  }catch (e: any) {
    console.log(`LoginView - error occured :\n ${e.message}`);
  }


}
</script>

<template>
  <main class="h-full flex">
    <div class="flex-auto w-1/2 min-h-full bg-yellow-600 ">
      <img src="/src/assets/tennis_smash.webp" alt="logo" class="w-3xl h-full"></img>
    </div>
    <div class="flex-auto w-1/2 min-h-full flex-col justify-center bg-yellow-600 px-6 py-15 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm justify-center">
        <img src="/src/assets/tsc_logo.png" alt="Your Company" class="mx-auto h-10 w-auto" />
        <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-white">
          Tennis Club - Réservations
        </h2>
        <p class="text-white text-md font-semibold text-center">
          Activer votre compte ou connectez-vous pour accéder à la plateforme de réservations
        </p>
      </div>

      <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form class="space-y-6">
          <div>
            <label for="aft_id" class="block text-sm/6 font-semibold text-gray-100">
              Identifiant AFT
            </label>
            <div class="mt-2">
              <input
                  id="aft_id"
                  type="number"
                  name="aft_id"
                  v-model="aft_id"
                  required
                  autocomplete="number"
                  class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-black outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6" />
            </div>
          </div>

          <div>
            <div class="flex items-center justify-between">
              <label for="password" class="block text-sm font-semibold text-gray-100">Password</label>
              <div class="text-sm">
                <a href="#" class="font-semibold text-indigo-400 hover:text-indigo-300">Forgot password?</a>
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
            <button
                type="submit"
                @click="submit"
                class="flex w-full justify-center rounded-md bg-lime-600 px-3 py-1.5 text-sm/6 font-semibold text-white hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
              Sign in
            </button>
          </div>
          <div class="mt-5">
            <p class="text-center text-white font-semibold">
              Premier connexion?
              <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-300">
                Activer votre compte
              </a>
            </p>
          </div>
        </form>




      </div>
    </div>
  </main>
</template>

<style scoped>

</style>