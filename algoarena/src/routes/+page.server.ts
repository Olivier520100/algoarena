import type { PageServerLoad } from './$types';
import { getXataClient } from '../xata';
import { redirect } from '@sveltejs/kit';


export const load: PageServerLoad = async ({ locals }) => {
	let session = await locals.auth();
	// if (session?.user?.email) {
	// 	redirect(302, '/dashboard');
	// }

	// Check if the user already exists in the database
	const existingUser = await getXataClient()
		.db.Users.filter({
			email: session?.user?.email
		})
		.getFirst(); // Use getFirst() to attempt to fetch a single user record
	
	const user = await getXataClient().db.Users.filter().getFirst()
	
	// If the user doesn't exist, create a new user record
	if (!existingUser) {
		await getXataClient().db.Users.create({
			name: session?.user?.name ?? '',
			email: session?.user?.email,
			elo: 700
		});
	}
// url: user.video.url;
	return { };
};

