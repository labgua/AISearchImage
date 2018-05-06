//search_result.js

function doSearchResult(){
	
	id_request = result_request["result"]["id_request"]
	action = result_request["result"]["action"]
	
	$.get("/api/search/"+id_request+"?action="+action)
	.done(function(resp){
		console.log(resp)
	
		$("#box_result_loader").hide()
		
		if( resp["type_result"] != "REDIRECT" ){
			
			if( resp["data"].length == 0 ){
				$("#box_result_status p").text("No results found!")
				return
			}
			else{
				$("#box_result_status p").text("Found "+ resp["data"].length +" results!")
			}
			
			html = ""
			
			for( i in resp["data"] ){
				
				link = resp["data"][i]["link"]
				url_img = resp["data"][i]["url_img"]
				
				html += formatItem(link, url_img)
	
			}
			
			$("#box_result").html(html)
			
			
		}
		else{
			window.open( resp["data"] ,'_self',false)
		}
		
	})
}

function formatItem(link, url_img){
	return '<div class="col-md-4">\
              <div class="card mb-4 box-shadow">\
                <img class="card-img-top" alt="Thumbnail [100%x225]" style="height: 225px; width: 100%; display: block;" src="'+ url_img +'" data-holder-rendered="true">\
                <div class="card-body">\
                  <div class="d-flex justify-content-between align-items-center">\
                    <div class="btn-group">\
                      <a href="'+ link +'" class="btn btn-sm btn-outline-secondary">View</a>\
                    </div>\
                  </div>\
                </div>\
              </div>\
            </div>'
}