<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { number } from 'zod';
	import { IconCrown } from '@tabler/icons-svelte';
	import { IconEqual } from '@tabler/icons-svelte';

	import EloTable from '../../components/EloTable.svelte';

	import { onMount } from 'svelte';
	onMount(() => {
		const interval = setInterval(() => {
			invalidate('data:matches');
			invalidate('data:users');
		}, 5000);

		return () => {
			clearInterval(interval);
		};
	});

	export let data;
</script>

<main class="overflow-hidden">
	<div class="absolute triangle-background -z-10"></div>
</main>

<div class="grid grid-cols-4 pimpoum overflow-hidden">
	<div class="col-span-3 grid grid-cols-3 mr-2 h-full overflow-y-scroll">
		{#each data.matches as match, index}
			{#if match.hasVideo == true}
				<div class="card text-center m-2">
					<a class="mx-auto " href="/matches/{match.id}">
						<h1 class="h1">Match {index + 1}</h1>
					</a>
					<div class="flex flex-row gap-2 m-2">
						<div>
							<h1 class="h1">{match.User1?.name}</h1>
							<p>
								{#if match.winner == 1}
									<IconCrown class="mx-auto"></IconCrown>
								{/if}{match.User1?.elo}
							</p>
						</div>
						<div class="flex flex-col">
							<h1 class="h1 my-auto mx-auto">VS</h1>
						{#if match.winner == 0}
							<IconEqual class="mt-auto mx-auto"></IconEqual>
						{/if}

						</div>
						
						<div>
							<h1 class="h1">{match.User2?.name}</h1>
							<p>
								{#if match.winner == 2}
									<IconCrown class="mx-auto"></IconCrown>
								{/if}{match.User2?.elo}
							</p>
						</div>
					</div>
				</div>
			{/if}
		{/each}
	</div>

	<div class="m-2 col-span-1 card h-fit">
		<EloTable users={data.users} />
	</div>
</div>
