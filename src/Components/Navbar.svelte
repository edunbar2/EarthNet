<script>
import {createEventDispatcher } from 'svelte';

let dispatch = createEventDispatcher();

export let tabs = [];
export let current_tab = "";

const  handleTabClick = (tab) => {
    dispatch('tabClicked', tab)
  }

</script>


<main>
<div class=bar>
    <div class=tabs>
        {#each tabs as tab}
        <div class="nav-button {current_tab === tab ? 'highlighted' : ''}" id="dash" on:click={() => handleTabClick(tab)}>
            <p style="pointer-events: none;">{tab}</p>
        </div>
        {/each}
    </div>
</div>
</main>

<style>
.bar{
    position: sticky;
    background-color: #7c8b69;
    padding: 0;
    height: 75px;
    width: 100%;
    display: flex;
    justify-content: flex-end;
    
}

.tabs{
    width: 800px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
}

.nav-button{
    margin-top: 12.5px;
    text-align: center;
    width: 150px;
    height: 50px;
    border: solid 2px black;
    pointer-events: auto;
}

.highlighted{
    background-color: #D7F9AB;
    border: none;
}




</style>