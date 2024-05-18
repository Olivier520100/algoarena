<script lang="ts">
	// These values are bound to properties of the video
	//@ts-nocheck
	import photo from "$lib/assets/castles.png"
	import linus from "$lib/assets/iu.png"
	import {IconArrowLeft,IconArrowRight} from "@tabler/icons-svelte"
	export let data;
	
	// export let data;

	let time = 0;
	let duration;
	let paused = true;
	
	
	let showControls = true;
	let showControlsTimeout;

	// Used to track time of last mouse down event
	let lastMouseDown;

	function handleMove(e) {
		// Make the controls visible, but fade out after
		// 2.5 seconds of inactivity
		clearTimeout(showControlsTimeout);
		showControlsTimeout = setTimeout(() => (showControls = false), 2500);
		showControls = true;

		if (!duration) return; // video not loaded yet
		if (e.type !== 'touchmove' && !(e.buttons & 1)) return; // mouse not down

		const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
		const { left, right } = this.getBoundingClientRect();
		time = (duration * (clientX - left)) / (right - left);
	}

	// we can't rely on the built-in click event, because it fires
	// after a drag — we have to listen for clicks ourselves
	function handleMousedown(e) {
		lastMouseDown = new Date();
	}

	function handleMouseup(e) {
		if (new Date() - lastMouseDown < 300) {
			if (paused) e.target.play();
			else e.target.pause();
		}
	}

	function handleClick(e) {
		console.log(e);
	}
	function addOneSecond() {
		time += 0.2;
	}
	function removeOneSecond() {
		time -= 0.2;
	}
	function format(seconds) {
		if (isNaN(seconds)) return '...';

		const minutes = Math.floor(seconds / 60);
		seconds = Math.floor(seconds % 60);
		if (seconds < 10) seconds = '0' + seconds;

		return `${minutes}:${seconds}`;
	}


</script>

<main>
	{#if data.url}
	<div class="absolute -z-80 triangle-background"></div>

	<div class="absolute z-80 left-1/4 top-40">
		<div class="flex flex-row justify-center justify-items-center">
			<button class="btn" on:click={removeOneSecond}><IconArrowLeft/></button>
			<button class="btn" on:click={addOneSecond}><IconArrowRight/></button>
		</div>
		<div class="mx-auto my-auto">
			<video
				class="mx-auto mt-2"
				poster={photo}
				height="400"
				width="800"
				src={data.url}
				on:mousemove={handleMove}
				on:touchmove|preventDefault={handleMove}
				on:mousedown={handleMousedown}
				on:mouseup={handleMouseup}
				on:keydown={handleClick}
				on:key
				bind:currentTime={time}
				bind:duration
				bind:paused
			>
				<track kind="captions" />
			</video>
			<progress class="mx-auto" value={time / duration || 0} />

			<div class="info">
				<span class="time">{format(time)}</span>
				<span>click anywhere to {paused ? 'play' : 'pause'} / drag to seek</span>
				<span class="time">{format(duration)}</span>
			</div>
		</div>
	</div>
	{:else}
	<img alt="linus" src={linus} class="h-full w-full"/>

	{/if}
</main>
