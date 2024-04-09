<script>
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	import EloTable from '../../components/EloTable.svelte';
    export let data

	// Call refreshUsers when the component mounts
	onMount(() => {
		const interval = setInterval(() => {
			invalidate('data:users');
		}, 5000);

		return () => {
			clearInterval(interval);
		};
	});

	// Set interval to refresh users data every 0.5 seconds
</script>

<main>
	<div>
		<EloTable users = {data.users}/>
	</div>
</main>
