<script lang="ts">
	import '../app.postcss';
	export let data;
	import { IconQuestionMark } from '@tabler/icons-svelte';
	import { IconCrown } from '@tabler/icons-svelte';
	import { SignIn, SignOut } from '@auth/sveltekit/components';
	import { popup, type PopupOptions } from '$lib/popup';
	import { onMount } from 'svelte';
	import { invalidate } from '$app/navigation';
	const popupSettings: PopupOptions = {
		popupId: 'popupNavIcon',
		placement: 'bottom'
	};

	onMount(() => {
		const interval = setInterval(() => {
			invalidate('data:elo');
		}, 5000);

		return () => {
			clearInterval(interval);
		};
	});
</script>

<div class="flex justify-between border-2 main px-4 py-2 h-[10vh]">
	<a class="flex items-center gap-2" href="/dashboard">
		<h1 class="h1 mt-4 text-main-blue">AlgoArena</h1>
	</a>
	<div class="flex items-center gap-2">
		<!-- <a class="btn" href="/rankings"> Rankings </a> -->
		<a class="mr-2" href="/matches">
			<h1 class="text-main-blue">Classement</h1>
		</a>
		{#if data.user}
			{#if data.elo}
				<IconCrown />
				<p>{data.elo}</p>
			{/if}
			<button class="btn btn-flat ml-2 h-10 w-10 p-0" use:popup={popupSettings}>
				<img src={data.avatar} class="object-cover" alt="your user avatar" />
			</button>
		{:else}
			<SignIn provider="">Sign in</SignIn>
			<div class="btn btn-flat h-10 w-10 p-0">
				<IconQuestionMark />
			</div>
		{/if}
	</div>
</div>

<div class="popup" id={popupSettings.popupId}>
	<div class="popup-arrow" id="arrow" />

	<div class="card flex w-40 flex-row items-stretch bg-background py-2 mx-auto">
		<SignOut>
			<div slot="submitButton" class="">Sign out</div>
		</SignOut>
	</div>
</div>

<slot />
