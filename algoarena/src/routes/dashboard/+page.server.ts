import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals }) => {
	let session = await locals.auth();
	if (!session?.user?.email) {
		redirect(302, '/');
	}

	
	return {};
};
