<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { Control, Field } from 'formsnap';

	import tuto1 from '$lib/assets/gifs/tuto1.gif';
	import tuto2 from '$lib/assets/gifs/tuto2.gif';
	import tuto3 from '$lib/assets/gifs/tuto3.gif';

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
	import "@splidejs/svelte-splide/css";


	import { browser } from '$app/environment';

	// Set interval to refresh users data every 0.5 seconds
</script>

<main class="overflow-hidden">
	<div class="absolute triangle-background -z-4"></div>
</main>

<div class="relative z-4">
	<div class="grid grid-cols-3">
		<div class="col-span-2 m-8">
			<Splide
				hasTrack={false}
				aria-label="My Favorite Images"
				options={{
					rewind: true,
					gap: '1rem',
					type: 'loop',
					perPage: 1,
					autoplay: true
				}}
			>
				<SplideTrack class="img-slider">
					<SplideSlide>
						<a href="#target-1"><img src={tuto1} class="object-cover" alt="Neighborhood" /> </a>
					</SplideSlide>
					<SplideSlide>
						<a href="#target-2">
							<img src={tuto2} class="object-cover" alt="Business" />
						</a>
					</SplideSlide>
					<SplideSlide>
						<a href="#target-3">
							<img src={tuto3} class="object-cover" alt="Restaurant" />
						</a>
					</SplideSlide>
				</SplideTrack>

				<div class="splide__progress h-4">
					<div class="splide__progress__bar" />
				</div>

				<div class="splide__arrows">
					<button class="splide__arrow splide__arrow--prev"><IconMathGreater /></button>
					<button class="splide__arrow splide__arrow--next"><IconMathGreater /></button>
				</div>
			</Splide>
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

	<div class="absolute flex flex-col">
		<div>
			<h1 id="target-1" class="h1">1. Collectez vos ressources</h1>
			<p >
				Vous commencerez la partie avec un Travailleur. Celui-ci vous permettera de collectionner les ressources (Arbre) sur la carte. Rammenez ces ressources dans votre chateau pour les ajouter à votre inventaire.
			</p>
			
		</div>

		<div>
			<h1 id="target-2" class="h1">Intertitre 2</h1>
			<p>
				Lorem ipsum, dolor sit amet consectetur adipisicing elit. Numquam necessitatibus mollitia
				iste pariatur. Quo consequatur neque dolor quisquam possimus consequuntur, cumque ducimus
				sint? Officiis totam voluptates veritatis delectus exercitationem molestiae?
			</p>
		</div>

		<div>
			<h1 id="target-3" class="h1">Intertitre 3</h1>
			<p>
				Lorem ipsum, dolor sit amet consectetur adipisicing elit. Numquam necessitatibus mollitia
				iste pariatur. Quo consequatur neque dolor quisquam possimus consequuntur, cumque ducimus
				sint? Officiis totam voluptates veritatis delectus exercitationem molestiae?
			</p>
		</div>
	</div>
</div>
