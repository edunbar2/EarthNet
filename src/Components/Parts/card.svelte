<script>
import Button from "./Button.svelte";
export let has_image = true;
export let image_src = ''
</script>


<div class="card {has_image ? "image-card" : "statistics-card"}">
    {#if has_image}
        <div class="image highlight"><img src="{image_src}" alt="Card Image">
        </div>
     {:else}
     <div class="statistics highlight"></div>

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
    *{
        color: #aeaeae;
    }

    .highlight{
        background-color: #162B3F;
    }

    .image{
        width: 100%;
        height: 40%;
        border: solid 1px black;
    }

    .statistics{
        width: 100%;
        height: 60%;
    }

    .title {
        text-align: center;
        font-size: 16px;
    }

    .card{
        background-color: #162B3F;
        justify-content: center;
        margin-top: 40px;
    }

    .image-card{
        width: 300px;
        height: 400px;
    }

    .statistics-card{
        width: 300px;
        height: 600px;
    }


    .button-div{
        width: 90%;
        padding: 5px;
        display: flex;
        justify-content: flex-end;
    }

</style>