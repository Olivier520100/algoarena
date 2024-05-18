import { getXataClient } from '../../xata';
import type { PageServerLoad } from './$types';
import { superValidate, fail, message } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { error, redirect } from '@sveltejs/kit';
import { pyUploadSchema } from './schema';
import {withFiles} from 'sveltekit-superforms';

export const load: PageServerLoad = async ({ locals, depends }) => {
	let session = await locals.auth();
	depends('data:users');

	if (!session?.user?.email) {
		redirect(302, '/');
	}

	const users = await getXataClient()
		.db.Users.select(['id', 'elo', 'email', 'name'])
		.sort('elo')
		.getAll();
	users.reverse();

	// Return the initial list of users
	return {
		users: users,
		form: await superValidate(zod(pyUploadSchema), { allowFiles: true })
	};
};

export const actions = {
	default: async ({ locals, request }) => {
		let session = await locals.auth();
		if (!session?.user?.email) throw error(401);
		const form = await superValidate(request, zod(pyUploadSchema));

		if (!form.valid) {
			return fail(400, { form });
		}
		const file = form.data.pyFile;
		console.log(file);



		const user = await getXataClient()
			.db.Users.filter({
				email: session?.user?.email
			})
			.getFirst(); // Use getFirst() to attempt to fetch a single user record

		if (!user) {
			return fail(400, withFiles({ form }));
		}
	

		const zimzum = await getXataClient().files.upload(
			{ table: 'Users', column: 'file', record: user.id },
			await file.arrayBuffer()
		);

		const record = await xata.db.Users.update(user.id, {
			fileChecked: false,
		});
		

		return withFiles({ form });
	}
};
