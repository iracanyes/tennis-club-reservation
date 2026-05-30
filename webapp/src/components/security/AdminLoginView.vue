
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ApiRoutes from "@navigation/api.routes.ts";
import { APIService, TokenService, CSRFService } from "@services";
import { useToast } from "primevue";

const email = ref('');
const password = ref('');
const router = useRouter();
const apiService = APIService.getInstance();
const tokenService = TokenService.getInstance();
const csrfTokenService = CSRFService.getInstance();
const toast = useToast();

onMounted(() => {
	// @ts-ignore
	if(typeof google !== 'undefined'){
		initGoogleSignIn();
	}
})

// Local connection using email
async function submit(e : Event){
  // Prevent default form behavior on submit
	e.preventDefault();

  try{
    let response = await apiService.post(ApiRoutes.AdminLogin, { email: email.value, password: password.value });

    if(response.data){
      // Set access token
			await tokenService.setToken(response.data);

			// CSRF Token has been rotated on login. Delete CSRF Token
			csrfTokenService.deleteToken();

      // Redirect to dashboard
			// Redirect to dashboard
			if(typeof router.options.history.state.back === "string" ){
				router.push((router.options.history.state.back as string));
			}else{
				router.push({
					name: 'admin_home',
				});
			}

    }

  }catch (e: any) {
    console.log(`AdminLoginView - error occured :\n ${e.message}`);

		// Afficher un message d'erreur
		toast.add({
			severity: 'error',
			summary: 'Error occured while logging in',
			detail : e.message,
			life : 3000
		});
  }

}

// Google Sign-in
const initGoogleSignIn = () => {
	console.log('initGoogleSignIn');

	// @ts-ignore
	google.accounts.id.initialize({
		client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
		//login_uri: import.meta.env.VITE_GOOGLE_LOGIN_URI,
		callback : (response: any) => {
			// Send the response code to serveur

			apiService.post(
				ApiRoutes.AdminLoginGoogle,
				{ credentials : response.credential },
			).then((response: any) => {
				console.log(`Google Auth Api response : ${JSON.stringify(response)}`);

				localStorage.setItem(import.meta.env.VITE_TOKEN_KEY, JSON.stringify(response));

				// Redirect to dashboard
				router.push({
					name: 'admin_home',
				});
			}).catch((e) => {
				console.error(`Google Auth Api response error : ${e}`);
			});
		}
	});

	// @ts-ignore
	google.accounts.id.prompt();

	// @ts-ignore
	google.accounts.id.renderButton(
		document.getElementById('google-sign-in-button'),
		{
			type:  "standard",
			text: "Connexion via Google",
			theme: "outline",
			size: "large",
			shape: "pill",
			logo_alignment: "center"
		}
	);


}

</script>

<template>
	<!-- Script for Google Sign-in -->
	<component is="script" src="https://accounts.google.com/gsi/client" @load="initGoogleSignIn" async />

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

      <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form method="post" class="space-y-6">
          <div>
            <label for="email" class="block text-sm/6 font-semibold text-gray-100">
              Email
            </label>
            <div class="mt-2">
              <input
                  id="email"
                  type="email"
                  name="email"
                  v-model="email"
                  placeholder="your_email@provider.ext"
                  required
                  autocomplete="email"
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
              <i data-feather="google" class="bg-white-600 text-white w-6 mr-2"></i>
              Premier connexion?
              <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-300">
                Activer votre compte
              </a>
            </p>
          </div>
        </form>
				<div id="google-sign-in-button" class="mt-10 flex justify-center">
				</div>
      </div>
    </div>
  </main>
</template>

<style scoped>

</style>