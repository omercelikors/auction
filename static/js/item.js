$(document).ready(function(){
    api_get_filtered_items()
    $("#search_item_input").val('')
    $("#search_form").submit(function(e){
      e.preventDefault();
    });
});

function render_items(results){
      for (let i = 0; i < results.length; i++) {
                $("#item_container").append(
                                            `<div class="col-xl-2dot4 col-lg-4 col-md-6 mb-4" id="${results[i].id}">
                                                <div class="bg-white rounded shadow-sm">
                                                  <img src="${results[i].image_path}" alt="${results[i].name}" class="item_img img-fluid card-img-top">
                                                  <div class="p-4">
                                                    <h5 class="name_content"> <a href="#" class="text-dark">${results[i].name.length > 90 ? results[i].name.substring(0,90) +"..." : results[i].name}</a></h5>
                                                    <p class="description_content small text-muted mb-0">${results[i].description.length > 150 ? results[i].description.substring(0,150) +"..." : results[i].description}</p>
                                                    <div class="badge ${results[i].auction_badge_color} px-3 rounded-pill font-weight-normal">${results[i].auction_badge}</div>
                                                    <div class="d-flex align-items-center justify-content-between rounded-pill bg-light px-3 py-2 mt-4">
                                                      <p class="small mb-0"><span class="font-weight-bold">$${results[i].last_price}</span></p>
                                                      <div><a class="btn btn-outline-primary" href="${results[i].url}" role="button">Bid Now</a></div>
                                                    </div>
                                                  </div>
                                              </div>`
                                            );
      }
}

function request_and_paginate(query="", order_type=1){
        $('#pagination_container').pagination({
            dataSource: 'http://127.0.0.1:8000/catalog/api/get/items?query='+query+'&order_type='+order_type,
            locator: 'data.results',
            totalNumberLocator: function(response) {
              return response.total_item_number;
            },
            pageSize: 10,
            pageNumber:1,
            pageRange : 2,
            autoHidePrevious: true,
            autoHideNext: true,
            showNavigator: true,
            formatNavigator: '<span style="color: #f00"><%= currentPage %></span> / <%= totalPage %> pages, <%= totalNumber %> items',
            className: 'paginationjs-theme-blue',
            // ajax: {
            //   beforeSend: function() {
            //     $("#item_container").html('Loading data from flickr.com ...');
            //   }
            // },
            callback: function(data, pagination) {
              $("#item_container div").remove();
              render_items(data);
            }
        })
}

function api_get_filtered_items(){
    request_and_paginate($("#search_item_input").val(), $( "#order_type" ).val())
}