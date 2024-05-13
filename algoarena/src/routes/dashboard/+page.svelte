<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { Control, Field } from 'formsnap';

	import tuto1 from '$lib/assets/gifs/tuto1.gif';
	import tuto2 from '$lib/assets/gifs/tuto2.gif';
	import tuto3 from '$lib/assets/gifs/tuto3.gif';
	import tuto3_1 from '$lib/assets/gifs/tuto3_1.gif';
	import tuto3_2 from '$lib/assets/gifs/tuto3_2.gif';
	import tuto3_3 from '$lib/assets/gifs/tuto3_3.gif';
	import tuto3_4 from '$lib/assets/gifs/tuto3_4.gif';
	import tuto4 from '$lib/assets/gifs/tuto4.gif';

	import CodeMirror from 'svelte-codemirror-editor';
	import { oneDark } from '@codemirror/theme-one-dark';
	import { python } from '@codemirror/lang-python';

	async function sendCode() {
		// Write the Python code to a file
		try {
			let response = await fetch('/api/file', {
				method: 'POST',
				body: value
			});

			if (response.ok) {
				const responseData = response;
				console.log(responseData);
			} else {
				console.error('Failed to process string');
			}
		} catch (error) {
			console.error('Error processing string:', error);
		}
	}

	export let data;
	let value = '';

	const form = superForm(data.form, {
		dataType: 'form'
	});
	const { form: formData, enhance } = form;

	let files: FileList;

	$: console.log(files);

	import { Splide, SplideSlide, SplideTrack } from '@splidejs/svelte-splide';
	import { IconMathGreater } from '@tabler/icons-svelte';
	import '@splidejs/svelte-splide/css';

	import { browser } from '$app/environment';

	let isCode = true;
	function setPage() {
		if (isCode) {
			isCode = false;
		} else {
			isCode = true;
		}
	}

	// Set interval to refresh users data every 0.5 seconds
</script>

<main class="overflow-hidden">
	<div class="absolute triangle-background -z-4"></div>
</main>

<div class="relative z-4">
	<div class="absolute left-0 top-4 flex flex-col">
		<button
			class="card"
			on:click={() => {
				setPage();
			}}>Code</button
		>
		<button
			class="card"
			on:click={() => {
				setPage();
			}}>Manuel</button
		>
	</div>
	{#if isCode}
		<div class="mt-10 mx-auto text-center">
			<h1 class="h1">Veuillez coder ici ou upload votre AI</h1>
		</div>
		<div class="grid grid-cols-3 -mt-24">
			<div class="col-span-2 m-32">
				<CodeMirror
					bind:value
					styles={{
						'&': {
							width: '100%',
							maxWidth: '100%',
							height: '25em'
						}
					}}
					theme={oneDark}
					placeholder={'Start coding here..'}
				/>
				<button
					class="card btn m-1"
					on:click={() => {
						sendCode();
					}}>Envoyer</button
				>
			</div>
			<div class="col-span-1 items-center mx-auto my-auto">
				<form use:enhance method="POST" enctype="multipart/form-data">
					<Field {form} name="pyFile">
						<Control let:attrs>
							<input {...attrs} bind:files type="file" />
						</Control>
					</Field>
					<button
						class="btn mt-2"
						on:click={() => {
							console.log($formData);
						}}>Envoyer</button
					>
				</form>
			</div>
		</div>
	{:else}
		<div class="">
			<p class="ml-1 mb-1">*Sélectionne une vidéo pour sa description</p>

			<Splide
				class=""
				hasTrack={false}
				aria-label="Game Rules"
				options={{
					gap: '1rem',
					type: 'loop',
					perPage: 1,
					autoplay: true
				}}
			>
				<SplideTrack class="img-slider">
					<SplideSlide>
						<a href="#target-1"><img src={tuto1} class="object-cover" alt="Collectez" /> </a>
					</SplideSlide>
					<SplideSlide>
						<a href="#target-2">
							<img src={tuto3} class="object-cover" alt="Attaquez" />
						</a>
					</SplideSlide>
					<SplideSlide>
						<a href="#target-3">
							<img src={tuto3_1} class="object-cover" alt="Melee" />
						</a>
					</SplideSlide>
					<SplideSlide>
						<a href="#target-4">
							<img src={tuto3_2} class="object-cover" alt="Archer" />
						</a>
					</SplideSlide>
					<SplideSlide>
						<a href="#target-5">
							<img src={tuto3_3} class="object-cover" alt="Tank" />
						</a>
					</SplideSlide>
					<SplideSlide>
						<a href="#target-6">
							<img src={tuto3_4} class="object-cover" alt="Cannon" />
						</a>
					</SplideSlide>
					<SplideSlide>
						<a href="#target-7">
							<img src={tuto4} class="object-cover" alt="Victoire" />
						</a>
					</SplideSlide>
				</SplideTrack>

				<div class="splide__progress h-7">
					<div class="splide__progress__bar" />
				</div>

				<div class="splide__arrows">
					<button class="splide__arrow splide__arrow--prev"><IconMathGreater /></button>
					<button class="splide__arrow splide__arrow--next"><IconMathGreater /></button>
				</div>
			</Splide>
		</div>

	<div class="absolute flex flex-col m-20 gap-40">
		<div class="justify-center items-center mx-auto text-center flex flex-col gap-10">
			<h1 id="target-1" class="h1">1. Ramassez vos ressources</h1>
			<p>
				Vous commencez la partie avec un Travailleur. Celui-ci vous permettera de collecter
				les ressources (Arbre) sur la carte. Rammenez ces ressources dans votre chateau pour les
				ajouter à votre stock.
			</p>
			<p>Code</p>
		</div>

		<div class="justify-center items-center mx-auto text-center flex flex-col gap-10">
			<h1 id="target-2" class="h1">3. Rassemblez votre armée</h1>
			<p>
				Maintenant que vous avez amasser des ressources et vous connaissez le plan de votre
				adversaire, c'est le temps d'attaquer. Construisez les unités de combat nécessaires pour
				contrez la stratégie opposante et obtenir la victoire.
			</p>

				<p>Code</p>
			</div>

		<div class="justify-center items-center mx-auto text-center flex flex-col gap-10">
			<h1 id="target-3" class="h1">3.1. Unité Mélée </h1>
			<p>
				Polyvalente et peu couteuse, cette unité est très utile au début du jeu pour défendre ou attaquer.
			</p>

			<p>Code</p>
		</div>

		<div class="justify-center items-center mx-auto text-center flex flex-col gap-10">
			<h1 id="target-4" class="h1">3.2. Unité Archer </h1>
			<p>
				Cette unité attaque à distance et fonctionne mieux lorsque protégée par d'autres unités ou dans des goulots d'étouffement.
			</p>

			<p>Code</p>
		</div>

		<div class="justify-center items-center mx-auto text-center flex flex-col gap-10">
			<h1 id="target-5" class="h1">3.3. Unité Tank </h1>
			<p>
				Comme son nom l'indique, 
				cette unité peux absorber beaucoup de dégat avant de se faire détruire. 
				En retour, elle ne fait pas beaucoup de dégat et est très couteuse.
			</p>

			<p>Code</p>
		</div>
		
		<div class="justify-center items-center mx-auto text-center flex flex-col gap-10">
			<h1 id="target-6" class="h1">3.4. Unité Cannon </h1>
			<p>
				Cette unité est la plus couteuse en ressources et celle qui a le moins de vie. 
				En échange, elle fait beaucoup plus de dégat à distance aux unités et aux structures adverses. 
				Très important pour garantir une victoire en fin de jeu.
			</p>

			<p>Code</p>
		</div>

		<div class="justify-center items-center mx-auto text-center flex flex-col gap-10">
			<h1 id="target-7" class="h1">4. Conditions de victoire</h1>
			<p>
				Pour gagner la partie, il faut avoir détruit le chateau adverse, ou avoir détruit toutes les
				unitées adverses. Attention, car votre adversaire essayera aussi de faire la même chose!
			</p>

				<p>Code</p>
			</div>
		</div>
	{/if}
</div>
