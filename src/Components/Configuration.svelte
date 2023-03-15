<script>
    import { each } from "svelte/internal";
    import Button from "./Parts/Button.svelte";

    // constants
    const maxInputs = 3;


    // variables
    let window = 0; // determine which window to display to the user
    let devices = [{ip: "", type: "", vendor: "", os: "", }]; // Stores objects contianing the device information
    let supported_device_types = ["Switch", "Router"];
    let number_of_devices = 3;
    let supported_vendors = [{name:"Cisco", operatingSystems:["IOS", "NX-OS", "IOS-XR"]}, {name:"Juniper", operatingSystems:["1", "2", "3"]}];
    let toggleManual = true;
    let manual_script = "";
    let tool_config_info = {type: '', config_type: ''};
    let tool_config_script = []; // stores data from the configuration tool to be handled by the python script
    

    $: scrollable = devices.length > maxInputs;

    // functions
    const addDevice = () => {
    devices = [...devices, {ip: "", type: "", vendor: "", os: ""}];
}

const removeDevice = (index) => {
    console.log(`Device removed: ${devices[index]}`);
    // if(devices.length > 1)
     devices = devices.filter((_, i) => i !== index);
}

const handleVendorChange = (selectedVendorName) => {
    selectedVendor = supported_vendors.find(vendor => vendor.name === selectedVendorName);
}

const validateIP = (ip) => {
    const regex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
     return regex.test(ip);

}


    //validate fields are correct and send to python script for implementation
const submitHandler = () => {
    console.log("Submitted");
}

const logClick = () => {
    toggleManual = !toggleManual;
    console.log("Field is now: " + toggleManual);
}

const logInput = () => {
    console.log(manual_script);
}

let selectedVendor = supported_vendors[0];
</script>

<main>
    <div class=info-div>
        <p>Please input the devices you wish to configure</p>
    </div>
        <div class=devices>
            <form on:submit|preventDefault={submitHandler}>
            <div class={scrollable ? "container" : ""}>
                {#each devices as device, i}
                <div class="input">
                    <label for="address">
                        Device Name:
                        <input type="text" bind:value={device.ip} placeholder="IP Address">
                        {#if validateIP(device.ip)}
                        <p style="color: green;" class="ip-valid">Valid IP</p>
                        {:else}
                        <p style="color: red;" class="ip-valid">Invalid IP</p>
                        {/if}
                    </label>
                    <label for="type">
                        Device Type: 
                        <select name="type" id="type" bind:value={device.type}>
                            {#each supported_device_types as device}
                            <option value="{device}">{device}</option>
                            {/each}
                        </select>
                    </label>
                    <label for="vendor">
                        Device Vendor:
                        <select name="vendor" id="vendor" bind:value={device.vendor} on:change={() => handleVendorChange(device.vendor)}>
                            {#each supported_vendors as vendor}
                            <option value="{vendor.name}">{vendor.name}</option>
                            {/each}
                        </select>
                    </label>
                    <label for="os">
                        Operating System: 
                        <select name="operatingSystem" id="operatingSystem" bind:value={device.os}>
                            {#each selectedVendor.operatingSystems as os}
                            <option value="{os}">{os}</option>
                            {/each}
                            
                        </select>
                        
                    </label>
                    <Button on:click={() => removeDevice(i)} small={true} >Remove Device</Button>
                    
                </div>
                {/each}
            </div>
            <Button on:click={addDevice}>Add Device</Button>
            <label for="tool">
                Manual
                <input type="checkbox" bind:checked={toggleManual}>
            </label>
            <br>
            {#if toggleManual}
                <textarea name="script" id="manual_script" bind:value={manual_script} placeholder="Input configuration script here"></textarea>
            {:else}
                <div class=tool-div>
                    <h2>Configuration Tool</h2>
                    <label for="type">
                        Device Type:<br>
                        <select name="type" id="type" bind:value={tool_config_info.type}>
                            {#each supported_device_types as device}
                            <option value="{device}">{device}</option>
                            {/each}
                        </select>
                    </label>
                    <!-- Prompt router configuration options -->
                    {#if tool_config_info.type === 'Router'} 
                    <p>routing</p>
                    <!-- Interface configuration -->

                        <!-- Routing -->

                        <!-- static routing -->

                        <!-- dynamic routing -->

                        <!-- protocol -->

                        <!-- interface -->

                        <!-- network -->

                        <!-- subnet mask or wildcard mask -->


                    <!-- Promp switch configuration options -->
                    {:else}
                    <p>switching</p>
                    <label for="config-type">
                        Conifiguration type:
                        <select name="config-type" id="switch-config-type" bind:value={tool_config_info.config_type}>
                            <option  value="Interface">Interface Configuration</option>
                            <option value="VLAN">VLAN Configuration</option>
                            <option value="VTP">VTP Configuration</option>
                        </select>
                    </label>
                    <!-- Interface configuration -->
                    {#if tool_config_info.config_type === "Interface"}
                        <p>Interface</p>
                    {:else if tool_config_info.config_type === "VLAN"}
                    <p>VLAN</p>
                    {:else if tool_config_info.config_type === "VTP"}
                    <p>VTP</p>
                        
                    {/if}

                    <!-- VLAN configuration -->

                    <!-- VTP configuration -->

                    {/if}
                </div>   
            
            {/if}
            <div class="button-wrapper">
                <Button  on:click={submitHandler} end={true}>Configure!</Button>
            </div>
            </form>
        </div>

</main>


<style>
*{
    font-family: Verdana, Geneva, Tahoma, sans-serif;
}

h1 h2 h3 h4{
    font-family: Georgia, 'Times New Roman', Times, serif;
}

main{
    justify-content: center;
}

button{
    background-color: #D7F9AB;
    border: none;
    border-radius: 10px;
}

.info-div{
    text-align: center;
}

.devices{
    display: flex;
    justify-content: center;
    align-items: center;
}

.input{
    display: flex;
    height: 50px;
    background-color: #7c8b69;
    margin: 10px;
    padding-top: 15px;
    width: 100%;
}


.ip-valid{
    transform: translate(120px, -12px);
}

.input button{
    margin-right: 5px;
    height: 20px;
}
.input label{
    margin: 0 5px;
}

@media screen and (max-width: 1125px){
    .input{
        flex-direction: column;
        height: 200px;
        margin-bottom: 5%;

    }
    .input button{
        width: 6em;
        height: 35px;
        padding-top: 0;
        margin: 15px;
    }
}

.button-wrapper{
    margin: 20px 10px;
    text-align: end;
}

#manual_script{
    resize: none;
    width: 100%;
    height: 40rem;
    align-self: center;
    background-color: #7c8b69;
    border: none;
    caret-color: #D7F9AB;
    cursor: pointer;
}

.container{
    width: 100%;
    max-height: 250px;
    overflow-y: auto;
    overflow-x: none;
    padding-right: 16px;
}

.tool-div{
    border: solid 1px black;
    text-align: center;
}
</style>