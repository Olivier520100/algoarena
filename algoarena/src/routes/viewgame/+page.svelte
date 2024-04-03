<script>
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';

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
		<table class="table">
			<tr class="tr">
				<th class="th">Name</th>
				<th class="th">Email</th>
				<th class="th">Elo</th>
			</tr>
			{#each data.users as user}
				<tr class="tr">
					<td class="td">{user.name}</td>
					<td class="td">{user.email}</td>
					<td class="td">{user.elo}</td>
				</tr>
			{/each}
		</table>
	</div>
</main>
