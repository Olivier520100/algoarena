<script lang="ts">
	export let users: { name: string|undefined|null; elo: number|undefined|null; email: string|undefined|null; }[];
</script>

<table class="table w-full ">
	<tr class="tr">
		<th class="th">Name</th>
		<th class="th">Elo</th>
	</tr>
	{#each users as user}
		<tr class="tr">
			<td class="td">{user.name}</td>
			<td class="td">{user.elo}</td>
		</tr>
	{/each}
</table>
