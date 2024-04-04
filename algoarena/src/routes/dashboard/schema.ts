import { z } from "zod";


const cvUploadSchema = z.object({
	ai_file: z
		.custom<File>()
		.refine((f) => f && f instanceof File, 'Start by uploading your AI as a python file.')
		.refine((f) => f instanceof File && f.type === 'application/py', 'Must be a Python File.')
		.refine((f) => f instanceof File && f.size < 1_000, 'Max 1Kb upload size.'),
});
