
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ApiRoutes from "@navigation/api.routes.ts";
import { APIService, TokenService } from "@services";
import { jwtDecode } from "jwt-decode";

const email = ref('');
const password = ref('');
const router = useRouter();
const apiService = APIService.getInstance();
const tokenService = TokenService.getInstance();


onMounted(() => {
	if(typeof google !== 'undefined'){
		initGoogleSignIn();
	}
})

async function submit(e : Event){
  // Prevent default form behavior on submit
	e.preventDefault();

  try{
    let response = await apiService.post(ApiRoutes.AdminLogin, { email: email.value, password: password.value });

    if(response.token){
      // Use token
			tokenService.setToken(response);

      // Redirect to dashboard
      await router.push({
        name: 'dashboard',
      });
    }

  }catch (e: any) {
    console.log(`AdminLoginView - error occured :\n ${e.message}`);
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
					name: 'dashboard',
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
      <img src="/src/assets/tennis_smash.webp" alt="logo" class="w-3xl h-full"></img>
    </div>
    <div class="flex-auto w-1/2 min-h-full flex-col justify-center bg-yellow-600 px-6 py-15 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm justify-center">
        <img src="/src/assets/tsc_logo.png" alt="Your Company" class="mx-auto h-10 w-auto" />
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

				<div id="google-sign-in-button" class="mt-10">
				</div>

				<!--
        <div class="mt-10">
          <button
              type="button"
              @click="google_signin"
              class="flex w-full justify-center rounded-md bg-indigo-500 px-3 py-1.5 text-sm/6 font-semibold text-white hover:bg-indigo-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" class="main-grid-item-icon" fill="none" {...props}>
              <path d="M24 12.276c0-.816-.067-1.636-.211-2.438H12.242v4.62h6.612a5.549 5.549 0 0 1-2.447 3.647v2.998h3.945C22.669 19.013 24 15.927 24 12.276Z" fill="#4285F4" />
              <path d="M12.241 24c3.302 0 6.086-1.063 8.115-2.897l-3.945-2.998c-1.097.732-2.514 1.146-4.165 1.146-3.194 0-5.902-2.112-6.873-4.951H1.302v3.09C3.38 21.444 7.612 24 12.242 24Z" fill="#34A853" />
              <path d="M5.369 14.3a7.053 7.053 0 0 1 0-4.595v-3.09H1.302a11.798 11.798 0 0 0 0 10.776L5.369 14.3Z" fill="#FBBC04" />
              <path d="M12.241 4.75a6.727 6.727 0 0 1 4.696 1.798l3.495-3.425A11.898 11.898 0 0 0 12.243 0C7.611 0 3.38 2.558 1.301 6.615l4.067 3.09C6.336 6.862 9.048 4.75 12.24 4.75Z" fill="#EA4335" />
            </svg>
            <span class="ml-4">
              Sign in with Google
            </span>

          </button>
        </div>
        -->
      </div>
    </div>
  </main>
</template>

<style scoped>

</style>