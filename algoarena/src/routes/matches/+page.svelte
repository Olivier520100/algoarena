<script lang="ts">
	import { invalidate } from '$app/navigation';
	import EloTable from '../../components/EloTable.svelte';

	import { onMount } from 'svelte';

	export let data;

    
</script>

<table class="table overflow-hidden">
	<tr class="tr">
		<th class="th">Player 1</th>
		<th class="th">Elo</th>
        <th class="th">Player 2</th>
		<th class="th">Elo</th>
        <th class="th">Result</th>
	</tr>
	{#each data.matches as match}
		<tr class="tr">
			<a href="/matches/{match.id}"><td class="td">{match.User1?.name}</td></a>
			<td class="td">{match.User1?.elo}</td>
			<td class="td">{match.User2?.name}</td>
			<td class="td">{match.User2?.elo}</td>
            <td class="td">Win </td>
		</tr>
	{/each}
</table>

<div class="relative z-4">
	<div class="absolute right-1/4 card">
		<EloTable users={data.users} />
	</div>
</div>

