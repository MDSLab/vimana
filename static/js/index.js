$(document).ready(function() {
    $("#commit").click(function(event){
        console.log("commiting to tendermint")
        // event.preventDefault();
        var fu1 = document.getElementById("fileOutput");
        res = fu1.value.slice(12, );
        // alert("You selected " + res);
        $.ajax({
            type:"POST",
            url:"http://localhost:8000/commit/",
            data:  {
                'file': res
            },
            success: function(data){
                console.log(data);
                $('#result').append(data+'<br>');
               console.log("Test Model")
            }
       });
       return true; //<---- move it here
    
    })
    
    $("#test").click(function(event){
        // event.preventDefault();
        var fu1 = document.getElementById("fileOutput");
        res = fu1.value.slice(12, );
        console.log("Sending ")
        // alert("You selected " + res);
        $.ajax({
            type:"POST",
            url:"http://localhost:8000/test/",
            data:  {
                'file': res
            },
            success: function(data){
                console.log(data);
                $('#result').append(data+'<br>');
               console.log("Test Model")
            }
       });
       return true; //<---- move it here
    
    })

   

    // $("#train").click(function(event){
    //     event.preventDefault();
       
    //     $.ajax({
    //         type:"POST",
    //         url:"http://localhost:8000/train/",
    //         data: true,
    //         success: function(){
    //            console.log("Train Model")
    //         }
    //    });
    //    return true; //<---- move it here
    
    // })
});