<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	import { superForm } from 'sveltekit-superforms';
	import { Control, Field } from 'formsnap';
	import photo from '$lib/assets/castles.png';
	import CodeMirror from 'svelte-codemirror-editor';
	import { EditorView } from '@codemirror/view';

	export let data;
	let value = '';

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

<div class="relative z-4 grid grid-cols-3">
	<div class="absolute top-10 left-10 col-span-1 card"><img src={photo} alt="castle"/></div>

	<div class="absolute right-10  top-10 col-span-2 items-center">
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
		<CodeMirror bind:value />
	</div>
</div>
