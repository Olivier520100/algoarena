<script lang="ts">
	import '../app.postcss';
	export let data;
	import { IconQuestionMark } from '@tabler/icons-svelte';
	// @ts-ignore

	import { SignOut } from '@auth/sveltekit/components';

	import { popup, type PopupOptions } from '$lib/popup';

	const popupSettings: PopupOptions = {
		popupId: 'popupNavIcon',
		placement: 'bottom'
	};
</script>

<div class="flex justify-between rounded-2xl border-2 main px-4 py-2">
	<a class="flex items-center gap-2" href="/">
		<h1 class="h1 mt-4">AlgoArena</h1>
	</a>

	<div class="flex items-center gap-4">
		<a class="btn" href="/rankings"> Rankings </a>

		{#if data.user}
			<button class="btn btn-flat h-10 w-10 p-0" use:popup={popupSettings}>
				<img src={data.avatar} class="object-cover" alt="your user avatar" />
			</button>
		{:else}
			<div class="btn btn-flat h-10 w-10 p-0">
				<IconQuestionMark />
			</div>
		{/if}
	</div>
</div>

<div class="popup" id={popupSettings.popupId}>
	<div class="popup-arrow" id="arrow" />

	<div class="card flex w-40 flex-col items-stretch bg-background py-2">
		<SignOut>
			<div slot="submitButton" class="">Sign out</div>
		</SignOut>
	</div>
</div>

<slot />
