<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	import EloTable from '../../components/EloTable.svelte';
	import { superForm } from 'sveltekit-superforms';
	import { Control, Field } from 'formsnap';
	export let data;

	// Call refreshUsers when the component mounts
	onMount(() => {
		const interval = setInterval(() => {
			invalidate('data:users');
		}, 5000);

		return () => {
			clearInterval(interval);
		};
	});

	const form = superForm(data.form, {
		dataType: 'form'
	});
	const { form: formData, enhance } = form;

	let files: FileList;

	$: console.log(files);

	// Set interval to refresh users data every 0.5 seconds
</script>

<main class="overflow-hidden">
	<div class="absolute triangle-background -z-4"></div>
</main>

<div class="relative z-4">
	<div class="absolute top-10 card">
		<form use:enhance method="POST" enctype="multipart/form-data">
			<Field {form} name="pyFile">
				<Control let:attrs>
					<input {...attrs} bind:files type="file" />
				</Control>
			</Field>
			<button
				class="btn"
				on:click={() => {
					console.log($formData);
				}}>Envoyer</button
			>
		</form>
	</div>
</div>

<div class="relative z-4">
	<div class="absolute right-1/4 card">
		<EloTable users={data.users} />
	</div>
</div>
