<script>
import found_devices from "../stores/found_devices.js";
import Button from "./Button.svelte";

const ngrok_url = "https://1873-164-52-144-80.ngrok-free.app"
let devices = [];


found_devices.subscribe(data => devices = data)
async function update_devices()
{
    const url = `${ngrok_url}/update_devices`


    const request = new Request(url);

    try{
        const response = await fetch(request);
        const responseData = await response.json();
        found_devices.set(responseData);
    } catch(error) {
        console.log(error);
    }
}
</script>

<Button on:click={update_devices}>Update List</Button>