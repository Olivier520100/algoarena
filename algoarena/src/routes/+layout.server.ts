import { redirect } from '@sveltejs/kit';
import { getXataClient } from '../xata';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({locals}) => {


	const session = await locals.auth();
	console.log(session);
	
	

   
			
	
	
	return {
        user: session,
		loggedIn: !!session,
		email: session?.user?.email,
		avatar: session?.user?.image,
		name: session?.user?.name,
        
	};
};
