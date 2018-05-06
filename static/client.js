
var pos = null
var api_key = "AIzaSyB9vDKdHI_ri_L_w7fyPVd2WEfHc-iYxmU"

function toService(param){
	console.log("toService : " + param)
}

function selectImg(){
	$('#file-input').trigger('click');
}

function onSelectedImg(){
	console.log("onSelectedImg")
	
    var file_data = $('#file-input').prop('files')[0];
	
    var form_data = new FormData();                  
    form_data.append('img', file_data);
    form_data.append('lat', pos['lat']);
    form_data.append('lng', pos['lng']);
    form_data.append('cap', pos['cap']);
    
    console.log(form_data);
    $("#info-status p").text("")
    $(".loader").show();
	
    $.ajax({
		url: 'api/search/',
		dataType: 'text',
		cache: false,
		contentType: false,
		processData: false,
		data: form_data,
		type: 'post',
		success: function(data){
			response = JSON.parse(data)
			console.log(response)
			id_request = response["id_request"]
			window.open('search/'+id_request ,'_self',false)
		},
		error: function(err){
			$("#info-status p").text("Something was wrong.")
			$(".loader").hide()
		}
     });
	
}



function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(handlePosition, error, options);
    } else {
        console.log("Geolocation is not supported by this browser.")
    }
}


var options = {
		  enableHighAccuracy: true,
		  timeout: 15000,
		  maximumAge: 0
};

function handlePosition(position){
	
	pos = {
			"lat" : position.coords.latitude,
			"lng" : position.coords.longitude,
			"cap" : null
	}
	
	console.log(pos)
	
	$.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+ pos["lat"] +","+ pos["lng"] +"&key=" + api_key )
	.done(function(data){
		
		//console.log(data)
		
		tmp_results = data["results"][0]["address_components"]
		//console.log("tmp_results!! ", tmp_results )
		
		for( i in tmp_results ){
			if( tmp_results[i]["types"][0] == "postal_code" ){
				//console.log("FOUND!! " + tmp_results[i]["long_name"] )
				pos["cap"] = tmp_results[i]["long_name"]
			}
		}
		
		console.log("pos", pos)
		//$("#pos").val(pos["cap"])
		//$("#lat").val(pos["lat"])
		//$("#lng").val(pos["lng"])
		
	})
	
}

function error(err) {
	console.warn(`ERROR(${err.code}): ${err.message}`);
	pos = {
		"lat" : null,
		"lng" : null,
		"cap" : null
	}
};



getLocation()
