import { getXataClient } from '../xata';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({locals}) => {


	const user = await locals.auth();
	console.log(user);

   
			
	
	
	return {
        user,
		loggedIn: !!user,
		email: user?.user?.email,
		avatar: user?.user?.image,
		name: user?.user?.name,
        
	};
};
