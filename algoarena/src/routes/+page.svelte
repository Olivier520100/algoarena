<script lang="ts">
    import { signIn, signOut } from "@auth/sveltekit/client"
	import { SignIn } from "@auth/sveltekit/components";
</script>

<main>


    <div>
        <SignIn provider="github">SignIn</SignIn>
    </div>
</main>
