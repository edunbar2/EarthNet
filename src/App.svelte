<script>
 import Navbar from "./Components/Navbar.svelte";
 import Header from "./Components/Header.svelte";
 let tabs = ["Dashboard", "Configure"];
</script>

<meta name="viewport" content="width=device-width, initial-scale=1.0">
<main>
  <Header />
  <Navbar {tabs}/>
  <div class=body>
    <p>This is a temporary tag for effect</p>
  </div>
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
  height: 95%;
  width: 90%;
  margin-left:10%;
  margin-top: 5%;
  border: solid 1px black;
}
</style>
