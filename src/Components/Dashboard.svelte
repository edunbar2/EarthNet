<script>
import Card from "./Parts/card.svelte";
import found_devices from "./stores/found_devices.js";
import AutomaticDevice from "./Parts/AutomaticDevice.svelte";
import Button from "./Parts/Button.svelte";
import UpdateDevices from "./Parts/UpdateDevices.svelte";

let devices_found = []
found_devices.subscribe(data => {devices_found = data})
const maxInputs = 6;
$: numDevices = devices_found.length;
$: scrollable = numDevices > maxInputs;

</script>


<main>
<div id="left-block">
<!--This will display the discovered devices-->
    <h1>Devices Found</h1>
    <div class={scrollable ? "scroll" : ""}>

    {#if devices_found.length > 0}
        {#each devices_found as device}
            <AutomaticDevice {device}/>
        {/each}
    {:else}
        <p>No devices found!</p>
    {/if}
    </div>
    <UpdateDevices />
</div>

    <div id="right-block">
        <h1> Welcome to Orchestrate</h1><br>
        <p>Orchestrate is a network automation tool focused on small businesses.
            With Orchestrate it is easy to make changes on your network efficiently and safely.
            You no longer have to worry about whether you picked the right IP address or VLAN, Orchestrate will handle that for you. </p>
    </div>


</main>


<style>
    *
    {
        color: white;

    }
main{

    margin: 0 5%;
    display: flex;
}


    #left-block{
        margin-top: 5%;
        padding: 20px;
        min-width: 40%;
        min-height: 40em;
        background-color: #162B3F;
        align-content: center;
    }
    #left-block h1
{
    margin-left: 25%;
    width: 8em
}

#right-block
{
    padding: 0 5% 0 5%;
    background: #162B3F;
    margin: 5% auto;
    width: 30%;
    height: 30em;
    align-content: center;
}


@media screen and (max-width: 1100px){
}

@media screen and (max-width: 700px){

    
}

    .scroll{
        width: 100%;
        max-height: 465px;
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 16px;
    }

</style>
