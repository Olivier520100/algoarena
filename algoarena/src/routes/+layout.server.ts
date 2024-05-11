import { redirect } from '@sveltejs/kit';
import { getXataClient } from '../xata';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({locals,depends}) => {


	const session = await locals.auth();
	depends('data:elo');

	console.log(session);


	const existingUser = await getXataClient()
	.db.Users.filter({
		email: session?.user?.email
	})
	.getFirst(); // Use getFirst() to attempt to fetch a single user record
	
	
	return {
		user: session,
		loggedIn: !!session,
		email: session?.user?.email,
		avatar: session?.user?.image,
		name: session?.user?.name,
		elo: existingUser?.elo
	};
};

