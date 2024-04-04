import type { PageServerLoad } from './$types';
import { getXataClient } from '../../xata';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals,depends }) => {
    depends('data:users')
	let session = await locals.auth();
	if (!session?.user?.email) {
		redirect(302, '/');
	}

   

	// Function to fetch users at intervals
	const users=await getXataClient().db.Users.sort('elo').getAll();
	users.reverse();

	

	// Return the initial list of users
	return { users:users };
};
