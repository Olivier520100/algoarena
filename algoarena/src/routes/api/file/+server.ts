import { error, json } from '@sveltejs/kit';
import { getXataClient } from '../../../xata';

export const POST = async ({ locals, request }) => {
	const session = await locals.auth();

	if (!session) error(401);

	const user = await getXataClient()
		.db.Users.filter({
			email: session?.user?.email
		})
		.getFirst();
	const text = await request.text();
	console.log(text);
	const wazambambi = await getXataClient().files.upload(
		{ table: 'Users', column: 'file', record: user.id },
		text
	);
	const record = await xata.db.Users.update(user.id, {
		fileChecked: false,
	});
	

	return new Response(true);
};
