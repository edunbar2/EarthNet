<script>
import Card from "./Parts/card.svelte";

</script>


<main>
<Card has_image={false}>
   <div slot=title> <h1>Information</h1></div> 

    <div slot=description>
        <p>
            Lorem ipsum dolor sit, amet consectetur adipisicing elit. Illum animi ullam dolor itaque voluptas quidem in laudantium placeat, minima nostrum sit architecto eveniet laborum quibusdam aspernatur neque, sequi natus eum.
        </p>
    </div>
</Card>

<Card has_image={false}>
    <div slot=title> <h1>Statistics</h1></div> 
 
     <div slot=description>
         <p>
             Lorem ipsum dolor sit, amet consectetur adipisicing elit. Illum animi ullam dolor itaque voluptas quidem in laudantium placeat, minima nostrum sit architecto eveniet laborum quibusdam aspernatur neque, sequi natus eum.
         </p>
     </div>
 </Card>

 <Card has_image={false}>
    <div slot=title> <h1>Statistics</h1></div> 
 
     <div slot=description>
         <p>
             Lorem ipsum dolor sit, amet consectetur adipisicing elit. Illum animi ullam dolor itaque voluptas quidem in laudantium placeat, minima nostrum sit architecto eveniet laborum quibusdam aspernatur neque, sequi natus eum.
         </p>
     </div>
 </Card>

 <Card has_image={false}>
    <div slot=title> <h1>Information</h1></div> 
 
     <div slot=description>
         <p>
             Lorem ipsum dolor sit, amet consectetur adipisicing elit. Illum animi ullam dolor itaque voluptas quidem in laudantium placeat, minima nostrum sit architecto eveniet laborum quibusdam aspernatur neque, sequi natus eum.
         </p>
     </div>
 </Card>
 
 <Card has_image={false}>
     <div slot=title> <h1>Statistics</h1></div> 
  
      <div slot=description>
          <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Illum animi ullam dolor itaque voluptas quidem in laudantium placeat, minima nostrum sit architecto eveniet laborum quibusdam aspernatur neque, sequi natus eum.
          </p>
      </div>
  </Card>
 
  <Card has_image={false}>
     <div slot=title> <h1>Statistics</h1></div> 
  
      <div slot=description>
          <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Illum animi ullam dolor itaque voluptas quidem in laudantium placeat, minima nostrum sit architecto eveniet laborum quibusdam aspernatur neque, sequi natus eum.
          </p>
      </div>
  </Card>
 

</main>


<style>
main{
    margin: 0 5%;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
}

@media screen and (max-width: 1100px){
    main{
        grid-template-columns: 1fr 1fr;
    }
    
}

@media screen and (max-width: 700px){
    main{
        padding-left: 20%;
        grid-template-columns: 1fr;
    }
    
}

</style>