
$(document).ready(function(){
    $("#search_form").remove();
    get_config()
});

function render_config(result){
    $("#config_container").append(
        `<form action="" id="config_form"  method="post">
           <div class="form-group">
             <label for="fund">*Fund(only integer):</label>
             <input type="text" class="form-control" placeholder="Enter fund amount" value="${result.fund}" id="fund" name="fund">
           </div>
           <div class="form-group">
             <label for="max_bid_amount">*Max Bid Amount(only integer):</label>
             <input type="text" class="form-control" placeholder="Enter max bid amount" value="${result.max_bid_amount}" id="max_bid_amount" name="max_bid_amount">
           </div>
           <button type="submit" class="btn btn-primary">Submit</button>
         </form> `
    )
    $("#config_form").submit(function(e){
        e.preventDefault();
        update_config();
    });
}

function get_config(){
    var api_get_config_url = 'http://127.0.0.1:8000/catalog/api/get/config'
        $.ajax({
            url: api_get_config_url,
            type: "get",
            success: function (data) {
                // Handle success here
                //console.log(data.result)
                render_config(data.result.user_config)
            },
            cache: false
          }).fail(function (jqXHR, textStatus, error) {
              // Handle error here
              console.log(error)
          });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendHttpAsync(path, method, body) {
    let props = {
        method: method,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        mode: "same-origin",
    }

    if (body !== null && body !== undefined) {
        props.body = JSON.stringify(body);
    }

    return fetch(path, props)
        .then(response => {
            return response.json()
                .then(result => {
                    return {
                        ok: response.ok,
                        body: result
                    }
                });
        })
        .then(resultObj => {    
            return resultObj;
        })
        .catch(error => {
            return error;
        });
}



function update_config(){
    var api_update_config_url = 'http://127.0.0.1:8000/catalog/api/update/config'
    
    let fund = $('#fund').val();
    let max_bid_amount = $('#max_bid_amount').val();
    let requestBody = {
        "fund": fund,
        "max_bid_amount": max_bid_amount
    };

    sendHttpAsync(api_update_config_url, "POST", requestBody)
        .then(response => {
            //console.log(response.ok)
            if (response.ok == true){
                swal({
                    title: "Good job!",
                    text: "You configuration is updated",
                    icon: "success",
                  });
            }else{
                var messages = response.body.messages.join()
                swal({
                    title: "Warning!",
                    text: messages,
                    icon: "warning",
                  });
            }
        });
}