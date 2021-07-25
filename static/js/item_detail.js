    
    url_splitted = window.location.href.replace("#", "").split('/')
    item_id = url_splitted[url_splitted.length - 1]

    $(document).ready(function(){
        $("#search_form").remove();
        get_item(item_id)
    });

   function get_item(item_id){
        var api_get_item_url = 'http://127.0.0.1:8000/catalog/api/get/item'
        $.ajax({
            url: api_get_item_url,
            type: "get",
            data:{"item_id":item_id},
            dataType: "json",
            success: function (data) {
                // Handle success here
                //console.log(data.result)
                render_item(data.result.item)
                if(data.result.item_bid_amounts.length > 0){
                    render_bid_history(data.result.item_bid_amounts)
                }
                
                if (data.result.item.auto_bidding_status == 1){
                    $('#auto_bidding').prop('checked', true);
                }else{
                    $('#auto_bidding').prop('checked', false);
                }
                countdown_timer(data.result.item.auction_finish_date_time)
            },
            cache: false
          }).fail(function (jqXHR, textStatus, error) {
              // Handle error here
              console.log(error)
          });
   }

   function render_bid_history(item_bid_amounts){
        $("#right_side").append(
            `<div class="yScroll project-info-box" id="bid_history">
                <h5>History</h5>
            </div>`
        )
        for (let i = 0; i < item_bid_amounts.length; i++){
            $("#bid_history").append(
                                        `
                                        <p>
                                        <b>Amout: $${item_bid_amounts[i].bid_amount} ->></b> Bidding Date: ${item_bid_amounts[i].created_at}
                                        </p>`
                                    )
        }
   }

   function render_item(result){
        $("#item_container").append(
                                    `<div class="container">
                                          <div class="row">
                                              <div class="col-md-5">
                                                  <div class="project-info-box mt-0">
                                                      <h5>${result.name}</h5>
                                                      <p class="mb-0">${result.description}</p>
                                                  </div><!-- / project-info-box -->
                                              
                                                  <div class="project-info-box">
                                                      <p><b>Starting Price:</b> $${result.min_price}</p>
                                                      <p><b>Last Audiction Price:</b> <span id="last_price">${result.last_auction_price ? "$"+result.last_auction_price : "Not Bidded"}</span></p>
                                                      <p><b>Auction Start Date-Time:</b> ${result.auction_start_date_time}</p>
                                                      <p><b>Auction End Date-Time:</b> ${result.auction_finish_date_time}</p>
                                                      <p class="mb-0"><b>Left Time: <span class="text-danger" id="countdown_timer"></span></b></p>
                                                  </div><!-- / project-info-box -->
                                              
                                                  <div class="project-info-box mt-0 mb-0" id="bid_button_box">
                                                        <div class="form-check-inline">
                                                            <a onclick="bid_now(${item_id});" class="btn btn-outline-primary" href="#" role="button" id="bid_now">Bid Now</a>
                                                        </div>
                                                        <div class="form-check-inline">
                                                          <label class="form-check-label">
                                                            <input onclick="auto_bidding(${item_id});" type="checkbox" class="form-check-input" value="1" name="auto_bidding" id="auto_bidding">Auto Bidding
                                                          </label>
                                                        </div>
                                                  </div><!-- / project-info-box -->
                                              </div><!-- / column -->
                                          
                                              <div class="col-md-7" id="right_side">
                                                  <img src="${result.image_path}" alt="${result.name}" class="item_detail_img rounded">
                                                  <!-- / project-info-box -->
                                              </div><!-- / column -->
                                          </div>
                                      </div>`
                                    );
        
    }

    function countdown_timer(auction_finish_date_time){
        var auction_finish_date_time = new Date(auction_finish_date_time);

        // Set the date we're counting down to
        var countDownDate = new Date(auction_finish_date_time).getTime();

        // Update the count down every 1 second
        var x = setInterval(function() {
        
            // Get today's date and time
            var now = new Date().getTime();
            
            // Find the distance between now and the count down date
            var distance = countDownDate - now;
            
            // Time calculations for days, hours, minutes and seconds
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            // Output the result in an element with id="demo"
            document.getElementById("countdown_timer").innerHTML = days + "d " + hours + "h "
            + minutes + "m " + seconds + "s ";
            
            // If the count down is over, write some text 
            if (distance < 0) {
                clearInterval(x);
                document.getElementById("countdown_timer").innerHTML = "AUCTION END";
            }
        }, 1000);
    }

    function bid_now(item_id){
        swal({
            title: "Are you sure?",
            text: "Once submitted, you will bid for this item!",
            icon: "warning",
            buttons: true,
            dangerMode: true,
          })
          .then((submit) => {
            if (submit) {
                var api_bid_now_url = 'http://127.0.0.1:8000/catalog/api/bid/now'
                $.ajax({
                    url: api_bid_now_url,
                    type: "get",
                    data:{"item_id":item_id},
                    dataType: "json",
                    success: function (data,textStatus, xhr) {
                        // Handle success here
                        //console.log(xhr.status)
                        get_bid_history(item_id)
                        if(xhr.status == 200){
                            swal({
                                title: "Good job!",
                                text: data.message,
                                icon: "success",
                                button: "OK",
                              });
                        } else{
                            swal({
                                title: "Warning!",
                                text: data.message,
                                icon: "warning",
                                button: "OK",
                              });
                        }
                    },
                    cache: false
                  }).fail(function (jqXHR, textStatus, error) {
                      // Handle error here
                      swal({
                        title: "Error!",
                        text: error,
                        icon: "error",
                        button: "OK",
                      });
                  });
            } else {
              swal("No bidding made");
            }
          });
        
    }

    function auto_bidding(item_id){
        var api_auto_bidding_url = 'http://127.0.0.1:8000/catalog/api/auto/bidding'
        
        if ($('#auto_bidding').is(":checked"))
        {
            var auto_bidding_status = 1;
        } else{
            var auto_bidding_status = 0;
        }

        $.ajax({
            url: api_auto_bidding_url,
            type: "get",
            data:{"item_id":item_id, "auto_bidding_status":auto_bidding_status},
            dataType: "json",
            success: function (data) {
                // Handle success here
                //console.log(data.result)
                
            },
            cache: false
          }).fail(function (jqXHR, textStatus, error) {
              // Handle error here
              console.log(error)
          });
    }

    function get_bid_history(item_id){
        var api_get_bid_history = 'http://127.0.0.1:8000/catalog/api/get/bid/history'
        $.ajax({
            url: api_get_bid_history,
            type: "get",
            data:{"item_id":item_id},
            dataType: "json",
            success: function (data) {
                // Handle success here
                //console.log(data.result)
                $("#bid_history").remove();
                render_bid_history(data.result.item_bid_amounts)
                $("#last_price").text('$' + data.result.last_auction_price);
            },
            cache: false
          }).fail(function (jqXHR, textStatus, error) {
              // Handle error here
              console.log(error)
          });
    }
