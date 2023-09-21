<script>
    import Button from "./Button.svelte";
    export let device;
    let supported_device_types = ["Switch", "Router"];

</script>

<main>

        <div class="automatic-devices">
           <p>IP:</p> <div class="label"><p>{device.ip}</p></div>
            <p>Vendor: </p><div class="label"><p>{device.vendor}</p></div>
        </div>




</main>

<style>

    .automatic-devices
    {
        padding-left: 15px;
        border: #141418 4px solid;
        color: white;
        display: flex;
        margin-top: 5px;
    }

    .label
    {
        border: #00789D solid 2px;
        background: #00789D;
        width: 100px;
        height: 20px;
        margin: auto;
        display: flex; /* Center text using flexbox */
        align-items: center; /* Vertically center text */
        justify-content: center; /* Horizontally center text */
    }


</style>