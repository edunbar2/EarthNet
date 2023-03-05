<script>
import {createEventDispatcher } from 'svelte';

let dispatch = createEventDispatcher();

export let tabs = [];
export let current_tab = "";

const  handleTabClick = (tab) => {
    dispatch('tabClicked', tab)
  }

</script>



<div class=bar>
    <div class=tabs>
        {#each tabs as tab}
        <div class="nav-button {current_tab === tab ? 'highlighted' : ''}" id="dash" on:click={() => handleTabClick(tab)}>
            <p style="pointer-events: none;">{tab}</p>
        </div>
        {/each}
    </div>
</div>


<style>
.bar{
    position: sticky;
    background-color: #7c8b69;
    padding: 0;
    height: 75px;
    width: 100%;
    display: flex;
    justify-content: flex-end;
    border-top: solid 0.5px black;
    
}
.tabs{
    width: 600px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
}

.nav-button{
    margin-top: 12.5px;
    text-align: center;
    width: 150px;
    height: 50px;
    pointer-events: auto;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    font-size: 18;
}

.highlighted{
    background-color: #D7F9AB;
    border: none;
    transition: all 0.5s ease-out;
}




</style>