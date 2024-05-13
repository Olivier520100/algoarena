import { z } from 'zod';

export const pyUploadSchema = z.object({
	pyFile: z
		.custom<File>()
		.refine((f) => f && f instanceof File, 'Start by uploading a Python file.')
		.refine((f) => f instanceof File && f.name.endsWith(".py"), 'Must be a Python file.')
		.refine((f) => f instanceof File && f.size < 100_000, 'Max 10Kb upload size.')
});
