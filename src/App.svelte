<script>
 import Navbar from "./Components/Navbar.svelte";
 import Header from "./Components/Header.svelte";
 import Dashboard from "./Components/Dashboard.svelte";
 import Configuration from "./Components/Configuration.svelte";
 import Admin from "./Components/Admin.svelte";
 
 let tabs = ["Dashboard", "Configure", "Admin"];
 let current_tab = "Dashboard";


 const changeTab = (event) => {
    current_tab = event.detail;
  }


</script>

<meta name="viewport" content="width=device-width, initial-scale=1.0">
<main>
  <Header />
  <Navbar {tabs} {current_tab} on:tabClicked={changeTab}/>

  {#if current_tab === "Dashboard"}
    <Dashboard />
  {:else if current_tab === "Configure"}
  <Configuration />
  {:else if current_tab === "Admin"}
  <Admin />
  {/if}
  
</main>

<style>
  main{

    background-color: #6B7361;
    height: 100%;
    width:100%;
    position: absolute;

  }
.body{
  background-color: #6B7361;
  width: 100%;
  border: solid 1px black;
}
</style>
