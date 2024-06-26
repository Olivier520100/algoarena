import { getXataClient } from '$xata';
import type { PageServerLoad } from './$types';
import { error, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals, depends }) => {
	let session = await locals.auth();
	depends('data:matches');
	depends('data:users');

	if (!session?.user?.email) {
		redirect(302, '/');
	}

	const matches = await getXataClient()
		.db.Matches.select(['User1.name', 'User2.name', 'User1.elo', 'User2.elo', 'hasVideo','winner', 'id'])
		.getAll();

	const users = await getXataClient()
		.db.Users.select(['id', 'elo', 'email', 'name'])
		.sort('elo')
		.getAll();
	users.reverse();

	// Return the initial list of users
	return {
		matches,
		users
	};
};
