<script>
import Button from "./Button.svelte";
export let has_image = true;
export let image_src = ''
</script>


<div class="card">
    {#if has_image}
        <div class="image"><img src="{image_src}" alt="Card Image">
        </div>
    {/if}
    <div class="title">
        <slot name="title">

        </slot>
    </div>
    <div class="card-desc">
        <slot name="description">

        </slot>
    </div>
    <div class="button-div">
        <Button>Go</Button>
    </div>

</div>


<style>

    .image{
        width: 400px;
        height: 250px;
        border: solid 1px black;
        background-color: #D7F9AB;
    }

    .title {
        font-size: 48;
    }

    .card{
        width: 400px;
        height: 600px;
        background-color: #7c8b69;
        justify-content: center;
    }

    .button-div{
        border: solid 1px black;
        width: 400px;
        display: flex;
        justify-content: flex-end;
    }

</style>