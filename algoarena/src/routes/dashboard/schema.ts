import { z } from 'zod';

export const pyUploadSchema = z.object({
	pyFile: z
		.custom<File>()
		.refine((f) => f && f instanceof File, 'Start by uploading a Python file.')
		.refine((f) => f instanceof File && f.type === 'text/x-python', 'Must be a Python file.')
		.refine((f) => f instanceof File && f.size < 1_000, 'Max 1Kb upload size.')
});
