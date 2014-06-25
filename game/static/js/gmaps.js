var initialLocation;
var ottawa = new google.maps.LatLng(45.411572, -75.698194);
var browserSupportFlag =  new Boolean();
var map;
var geocoder;

$(function() {

    $(document).ready(function(){
        geocoder = new google.maps.Geocoder();
        var myOptions = {
            center: ottawa,
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.ROADMAP
          };
        map = new google.maps.Map(document.getElementById("map"), myOptions);

        geolocateUser();
    });
        
    var geolocateUser = function(){
          // Try W3C Geolocation method (Preferred)
          if(navigator.geolocation) {
            browserSupportFlag = true;
            navigator.geolocation.getCurrentPosition(function(position) {
              initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
              map.setCenter(initialLocation);
            }, function() {
              handleNoGeolocation(browserSupportFlag);
            });
          } else if (google.gears) {
            // Try Google Gears Geolocation
            browserSupportFlag = true;
            var geo = google.gears.factory.create('beta.geolocation');
            geo.getCurrentPosition(function(position) {
              initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
              map.setCenter(initialLocation);
            }, function() {
              handleNoGeolocation(browserSupportFlag);
            });
          } else {
            // Browser doesn't support Geolocation
            browserSupportFlag = false;
            handleNoGeolocation(browserSupportFlag);
          }
    };

    function handleNoGeolocation(errorFlag) {
      if (errorFlag == true) {
        initialLocation = null;
      }
      map.setCenter(ottawa);
    }
	
});

function codeAddress() {
	$("#not_found").remove();
    var address = document.getElementById("search").value;
    if (initialLocation) {
        var latitude = initialLocation.lat();
        var longitude = initialLocation.lng();
        var lower = new google.maps.LatLng(latitude-0.05, longitude-0.05);
        var upper = new google.maps.LatLng(latitude+0.05, longitude+0.05);
        var bounds = new google.maps.LatLngBounds(lower, upper);
    } else {
        var bounds = null
    }
    geocoder.geocode( { 'address': address, 'bounds' : bounds }, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
      } else {
        $("#search_map").append('<p style="color:red;" id="not_found">We could not find the specified address.</p>');
      }
    });
}