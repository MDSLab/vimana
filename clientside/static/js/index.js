$(document).ready(function() {
    $("#query").click(function(event){
        console.log("Quering result for given input")
        // event.preventDefault();
        var fu1 = document.getElementById("fileOutput");
        res = fu1.value.slice(12, );
        model_name = document.getElementById('modelname').value;
        
        $.ajax({
            type:"POST",
            url:"http://localhost:8000/commit/",
            data:  {
                'file': res,
                'model': model_name
            },
            success: function(data){
                console.log(data);
                $('#result').append(
                    ' <article class="message"> \
                    <div class="message-body">' +
                     data +
                   ' </div> \
                 <br>');
            }
       });
       return true; 
    
    })
    

    // $("#query").click(function(event){
    //     console.log("Query from tendermint")
    //     // event.preventDefault();
    //     var fu1 = document.getElementById("fileOutput");
    //     res = fu1.value.slice(12, );
    //     // alert("You selected " + res);
    //     $.ajax({
    //         type:"POST",
    //         url:"http://localhost:8000/query/",
    //         data:  {
    //             'file': res
    //         },
    //         success: function(data){
    //             console.log(data);
    //             $('#result').append(
    //                 ' <article class="message"> \
    //                 <div class="message-header"> \
    //                   <p>Reply from Nodes</p> \
    //                 </div> \
    //                 <div class="message-body">' +
    //                  data +
    //                ' </div> \
    //               </article> <br>');
    //         }
    //    });
    //    return true; //<---- move it here
    
    // })
    
    // $("#test").click(function(event){
    //     // event.preventDefault();
    //     var fu1 = document.getElementById("fileOutput");
    //     res = fu1.value.slice(12, );
    //     console.log("Sending ")
    //     // alert("You selected " + res);
    //     $.ajax({
    //         type:"POST",
    //         url:"http://localhost:8000/test/",
    //         data:  {
    //             'file': res
    //         },
    //         success: function(data){
    //             console.log(data);
    //             $('#result').append(
    //                 ' <article class="message is-info"> \
    //                 <div class="message-header"> \
    //                   <p>Result on Test</p> \
    //                 </div> \
    //                 <div class="message-body">' +
    //                  data +
    //                ' </div> \
    //               </article> <br>');
    //            console.log("Test Model")
    //         }
    //    });
    //    return true; //<---- move it here
    
    // })

});

