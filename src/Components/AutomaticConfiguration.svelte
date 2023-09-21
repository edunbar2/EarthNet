<script>
import LoginInformationPrompt from "./Parts/LoginInformationPrompt.svelte";
import found_devices from "./stores/found_devices.js";

let foundDevices = [];
found_devices.subscribe(data => foundDevices = data);



</script>

<main>
    <LoginInformationPrompt/>

    <div class="devices">


    </div>

    <div class="toolbar">

    </div>


</main>



<style>


</style>