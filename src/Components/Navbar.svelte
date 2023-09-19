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
    <div class="logo">EarthNet</div>
    <div class=tabs>
        {#each tabs as tab}
        <div class="nav-button {current_tab === tab ? 'highlighted' : ''}" id="dash" on:click={() => handleTabClick(tab)}>
            <p style="pointer-events: none;">{tab}</p>
        </div>
        {/each}
    </div>
</div>


<style>
/*.bar{*/
/*    color: #aeaeae;*/
/*    position: sticky;*/
/*    background-color: #162B3F;*/
/*    padding: 0;*/
/*    height: 75px;*/
/*    width: 100%;*/
/*    display: flex;*/
/*    justify-content: flex-end;*/
/*    border-top: solid 0.5px black;*/
/*    */
/*}*/
/*.tabs{*/
/*    width: 600px;*/
/*    display: grid;*/
/*    grid-template-columns: repeat(3, 1fr);*/
/*}*/

.bar{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
}

.tabs{
    display: flex;
    gap: 10px;
}

.logo{
    color: white;
    font-size: 36px;
    margin-right: auto;
}

.nav-button{
    margin-top: 12.5px;
    text-align: center;
    width: 150px;
    height: 50px;
    pointer-events: auto;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    font-size: 18px;
}

.highlighted{
    background-color: #00789D;
    border: none;
    transition: all 0.5s ease-out;
}





</style>