<script>
import found_devices from "../stores/found_devices.js";
import Button from "./Button.svelte";

const ngrok_url = "https://29b2-38-110-15-66.ngrok-free.app"
let devices = [];


found_devices.subscribe(data => devices = data)
async function update_devices()
{
    console.log("Updating Devices...");
    const url = `http://10.11.12.26:5000/update_device_list`;
    console.log(url);


    const request = new Request(url, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    });
    try{
        
        const response = await fetch(url);
        console.log("Request has returned from server");

        const responseData = await response.json();
	console.log("Update Successful! Updating store.");
    console.log(responseData["data"]);
        found_devices.set(responseData["data"]);
    } catch(error) {
        console.log("Did not work: printing error:");
        console.log(error);
    }
}
</script>

<Button on:click={update_devices}>Update List</Button>
