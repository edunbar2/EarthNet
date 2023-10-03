<script>
import LoginInformation from "../stores/LoginInformation.js";
import Button from "./Button.svelte";

let storeInformation = {};
LoginInformation.subscribe(data => storeInformation = data);

let login_information = {"username": "", "password": "", "secret":""};
function updateLoginInformation()
{
    LoginInformation.set({"username": login_information.username, "password": login_information.password, "secret": login_information.secret});
}

</script>
<main>
<div class=login-information>
    <p>Login Information</p><br>
    <input type="text" placeholder="username" bind:value={login_information.username}>
    <input type="password" placeholder="password" bind:value={login_information.password}>
    <input type="password" placeholder="secret" bind:value={login_information.secret}>
    <Button small="{true}" on:click={updateLoginInformation}>Store Login</Button>
</div>
</main>

<style>

    .login-information{
        color: white;
        width: 100%;
        background-color: #162B3F;
    }
</style>