import type { PageServerLoad } from './$types';
import { getXataClient } from '$xata';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals,params }) => {
	let session = await locals.auth();
    if (!session?.user?.email) {
	 	redirect(302, '/');
	}
	let url;
	const match = await getXataClient().db.Matches.filter({id:params.id}).getFirst();
	

	
	return {  url:match?.video.url };
};
