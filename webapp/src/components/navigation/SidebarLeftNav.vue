<script setup lang="ts">
import { Badge, PanelMenu } from "primevue";
import {ref} from "vue";
import { useRouter, RouterLink } from "vue-router";
import {isNil} from "lodash";
import TokenService from "@services/token.service.ts";
import AppRoutes from "@navigation/app.routes.ts";

const router  = useRouter();
const tokenService = TokenService.getInstance();



const items = ref([
	{
		label : "Accueil",
		icon : "pi pi-home",
		command : () => router.push({ name : "home" }),
	},
	{
		label: 'Réservations',
		icon: 'pi pi-calendar',
		badge: 5,
		items: [
			{
				label: 'Liste des réservations',
				icon: 'pi pi-calendar-times',
				route: "/reservations",
			},
			{
				label: 'Mes réservations',
				icon: 'pi pi-calendar-plus',
				badge: 5,
				route: "/reservations/me",
			}
		]
	},
	{
		label: 'Événements',
		icon: 'pi pi-calendar-clock',
		// utilisation du table spread pour ajouter les éléments à afficher seulement pour les administrateurs
		items: [
			...(tokenService.isAdmin.value ?
				[
					{
						label: 'Gestion des événements',
						icon: 'pi pi-trophy',
						badge: 6,
						route: "/events",
					}
				]
				: []
			)
		]
	},
	{
		label: 'Terrains',
		icon: 'pi pi-objects-column',
		items: [
			{
				label : 'Réservation par terrain',
				icon : 'pi pi-map',
				route : '/courts/reservations'
			},
			...(tokenService.isAdmin.value
					? [
						{
							label : 'Gestion des terrains',
							icon : 'pi pi-flag',
							route : '/courts'
						},

					]
					: []
			)
		]
	},
	{
		label: 'Membres',
		icon: 'pi pi-users',
		items: [
			{
				label: 'Liste des membres',
				icon: 'pi pi-users',
				route: AppRoutes.MemberList,
			},
			...(tokenService.isAdmin.value
				? [
						{
							label: 'Ajouter un membre',
							icon: 'pi pi-user-plus',
							route: AppRoutes.MemberCreate,
						}
					]
				: []
			)

		]
	},
	{
		label: 'Abonnements',
		icon: 'pi pi-chart-line',
		items: [
			{
				label:"S'abonner",
				icon: 'pi pi-dollar',
				route : "/subscribe",
			},
			...(tokenService.isAdmin.value
				? [
						{
							label: 'Liste des abonnements',
							icon: 'pi pi-money-bill',
							route : "/subscriptions",
							adminOnly: true,
						},
						{
							label: 'Valider un abonnement',
							icon: 'pi pi-check-circle',
							route : "/subscriptions/add",
							adminOnly: true,
						}
					]
				: []
			)

		]
	},
	{
		label: 'Profil',
		icon: 'pi pi-user',
		items: [
			{
				label: 'Mettre à jour son profil',
				icon: 'pi pi-pencil',
				route: "/profile/update"
			},
			{
				label: 'Changer son mot de passe',
				icon: 'pi pi-shield',
				route : "/profile/change_password"
			}
		]
	}
]);


</script>

<template>
	<div class="h-full flex flex-col">
		<div id="logo" class="h-14 w-full flex flex-row bg-lime-500 p-2 mb-4">
			<img src="/src/assets/img/tsc_logo.png" alt="TCR - Réservations" class="w-10 rounded-sm mr-2"/>
			<p class="h-8 mt-2 flex text-md font-semibold text-white-100 text-center align-middle">TCR - Réservations</p>
		</div>
		<div id="sidebar-left-menu" class="h-full card flex-1 justify-content-center bg-lime-500">
			<PanelMenu :model="items" class="w-full md:w-20rem bg-lime-500">
				<template #item="{ item }">
					<router-link
						v-if="item.route"
						:to="item.route"
						v-slot="{ href, navigate }"
						custom
					>
						<a
							v-ripple
							class="flex items-center px-3 py-2 cursor-pointer hover:text-lime-800"
							:href="href"
							@click="navigate"
						>
							<span :class="[item.icon, 'text-white']" style="font-size: 1.25rem" />
							<span :class="['ml-2', 'text-xs', { 'text-white' : true, 'font-semibold': !isNil(item.items) }]">{{ item.label }}</span>
							<Badge v-if="item.badge" class="ml-auto" :value="item.badge" />
						</a>
					</router-link>
					<a v-else v-ripple class="flex items-center cursor-pointer text-color px-3 py-2 hover:text-lime-800" :href="item.url" :target="item.target">
						<span :class="[item.icon,'text-white','text-lg']"  style="font-size: 1.25rem" />
						<span class="ml-2 text-white">{{ item.label }}</span>
						<Badge v-if="item.badge" class="ml-auto" :value="item.badge" />
						<!--
						<span v-if="item.shortcut" class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1">{{ item.shortcut }}</span>
						-->
						<span v-if="item.items" class="pi pi-angle-down text-primary ml-auto" />
					</a>
				</template>
			</PanelMenu>
		</div>
	</div>

</template>

<style lang="scss">
#sidebar-left-menu .p-panelmenu-panel {
	background: oklch(76.8% 0.233 130.85) !important;
	border-color: oklch(76.8% 0.233 130.85) !important;

	&:hover{
		background: oklch(89.7% 0.196 126.665) !important;
		color: oklch(27.4% 0.072 132.109) !important;

		span{
			color: oklch(27.4% 0.072 132.109) !important;
		}
	}

	a:hover{
		background: oklch(93.8% 0.127 124.321) !important;
		color: inherit;
	}


}
</style>

<style scoped>

</style>