<script>

    export let users;
</script>


<table class="table">
    <tr class="tr">
        <th class="th">Email</th>
        <th class="th">Elo</th>
    </tr>
    {#each users as user}
        <tr class="tr">
            <td class="td">{user.name}</td>
            <td class="td">{user.elo}</td>
        </tr>
    {/each}
</table>