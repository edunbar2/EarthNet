<script>
    import { each } from "svelte/internal";
    import Admin from "./Admin.svelte";
    import Button from "./Parts/Button.svelte";

    // constants
    const maxInputs = 3;


    // variables
    let window = 0; // determine which window to display to the user
    let devices = [{ip: "", type: "", vendor: "", os: ""}]; // Stores objects contianing the device information
    let supported_device_types = ["Switch", "Router"];
    let number_of_devices = 3;
    let supported_vendors = [{name:"Cisco", operatingSystems:["IOS", "NX-OS", "IOS-XR"]}, {name:"Juniper", operatingSystems:["1", "2", "3"]}];
    let toggleManual = true;
    let manual_script = "";

    // stores data from the configuration tool to be handled by the python script

    let tool_config_script; 
    let config_type = "";
    let interface_to_add = "";
    let untagged_interface_to_add

    let config_map = 
    {
        'interface config': {interface_name: '', ip_address: 'Switch', subnet_mask: '', description: ''},
       'static routing': {destination_network: '', next_hop: '', subnet_mask: ''},
       'dynamic routing': {routing_protocol: '', network: '', subnet_mask: '', interface: '', areas: '', ospf_leader: false},
       'vlan config': {vlan_id: '', vlan_name: '', vlan_description: '', delete: false, vlan_state: true, vlan_mtu: '', vlan_ip_address: '', vlan_ip_mask: '', vlan_tagged_interfaces: [], vlan_untagged_interfaces: []},
       'vtp config': {vtp_domain: '', vtp_password: ''},

    }

    const handle_config_type = (event) => {
        tool_config_script = config_map[event.target.value];
        config_type = event.target.value;
    }

    const add_tagged_interface = () => {
        console.log("Adding interface" + interface_to_add);
        if(interface_to_add !== "") tool_config_script.vlan_tagged_interfaces = [...tool_config_script.vlan_tagged_interfaces,interface_to_add];
    }

    const add_untagged_interface = () => {
        if(untagged_interface_to_add !== "") tool_config_script.vlan_untagged_interfaces = [...tool_config_script.vlan_untagged_interfaces, untagged_interface_to_add];
    }

    $: scrollable = devices.length > maxInputs;

    // functions for form
    const addDevice = () => {
    devices = [...devices, {ip: "", type: devices[0].type, vendor: "", os: ""}];
}

const removeDevice = (index) => {
    console.log(`Device removed: Device IP: ${devices[index].ip} Type: ${devices[index].type} Vendor: ${devices[index].vendor} OS: ${devices[index].os}`);
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
    console.log(`Submitted; ${devices} will be configured with: ${toggleManual ? manual_script : tool_config_script}`);
}

const logClick = () => {
    toggleManual = !toggleManual;
    console.log("Field is now: " + toggleManual);
}

const logInput = () => {
    console.log(manual_script);
}

// functions for handling configuration tool

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
                        Device IP:
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
                        <select name="type" id="type" bind:value={devices[0].type}>
                            {#each supported_device_types as device}
                            <option value="{device}">{device}</option>
                            {/each}
                        </select>
                    </label>
                    <!-- Prompt router configuration options -->
                    {#if devices[0].type === 'Router'} 
                    <p>Routing</p>
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

                    <p>Switching</p>
                    <label for="config-type">
                        Conifiguration type:
                        <select name="config-type" id="switch-config-type" on:change={handle_config_type}>
                            <option  value="interface config">Interface Configuration</option>
                            <option value="vlan config">VLAN Configuration</option>
                            <option value="vtp config">VTP Configuration</option>
                        </select>
                    </label>
                    <!-- Interface configuration -->
                    {#if config_type === "interface config"}
                        <p>Interface</p>
                        <!-- VLAN configuration -->
                    {:else if config_type === "vlan config"}
                    <p>VLAN</p>
                    <!-- Deleting? -->
                    <p>Delete VLAN?</p> <input type="checkbox" bind:checked={tool_config_script.delete}>

                        <!-- vlan_id: '', vlan_name: '', vlan_description: '', delete: false, vlan_state: true, vlan_mtu: '', vlan_ip_address: '', vlan_ip_mask: '', vlan_tagged_interfaces: [], vlan_untagged_interfaces: [] -->

                    <!-- VLAN ID -->
                    <label for="VLAN-ID">VLAN ID
                        VLAN ID:
                        <input type="number" bind:value={tool_config_script.vlan_id}>
                    </label>
                    <label for="VLAN-Name">VLAN Name
                        VLAN Name:
                        <input type="text" bind:value={tool_config_script.vlan_name}>
                    </label>
                    <label for="VLAN-Description">VLAN Description
                        VLAN Description:
                        <input type="number" bind:value={tool_config_script.vlan_description}>
                    </label>
                    <label for="VLAN-State">VLAN State
                        Active or Suspended state?:
                        <input type="checkbox" bind:value={tool_config_script.vlan_state}>
                    </label>
                    <label for="VLAN-MTU">VLAN MTU
                        VLAN MTU:
                        <input type="number" bind:value={tool_config_script.vlan_mtu} placeholder="-1">
                    </label>
                    <label for="VLAN-IP">VLAN IP
                        VLAN IP:
                        <input type="number" bind:value={tool_config_script.vlan_ip_address}>
                    </label>
                    <label for="VLAN-Mask">VLAN Mask
                        VLAN Mask:
                        <input type="number" bind:value={tool_config_script.vlan_ip_mask}>
                    </label>
                    <label for="VLAN-ID">VLAN ID
                        VLAN ID:
                        <input type="number" bind:value={tool_config_script.vlan_id}>
                    </label>
                    <br><br>
                    <p>Tagged Interfaces:</p>
                    <ul>
                        {#each tool_config_script.vlan_tagged_interfaces as face}
                            <li>{face}</li>
                        {/each}

                    </ul>
                    <label for="VLAN-Tagged-Interfaces">VLAN Tagged Interfaces
                        Add Tagged Interface:
                        <input type="text" bind:value={interface_to_add}>
                        <button type="button" on:click={add_tagged_interface}>Add Interface</button>
                    </label>
                    <br><br>
                    <p>Untagged Interfaces:</p>
                    <ul>
                        {#each tool_config_script.vlan_untagged_interfaces as face}
                            <li>{face}</li>
                        {/each}

                    </ul>
                    <label for="VLAN-Untagged-Interfaces">VLAN Untagged Interfaces
                        Add Untagged Interface:
                        <input type="text" bind:value={untagged_interface_to_add}>
                        <button type="button" on:click={add_untagged_interface}>Add Interface</button>
                    </label>
        
                    <!-- VTP configuration -->
                    {:else if config_type === "vtp config"}
                    <p>VTP</p>
                        
                    {/if}



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