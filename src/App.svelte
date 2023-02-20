<script>
 import Navbar from "./Components/Navbar.svelte";
 import Header from "./Components/Header.svelte";
 let tabs = ["Dashboard", "Configure"];
</script>



<Navbar {tabs}/>
<main>
  <p>This is a temporary tag for effect</p>
</main>

<style>
main{
  background-color: #6B7361;
  height: 95%;
  width: 90%;
  margin: 2.5% 10%;
  position: absolute;
}
</style>
